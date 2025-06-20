"""A class to store a measurement for one frequency, one rack."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.axes._axes import Axes
from multipac_testbench_calibrate_racks.helper import printc
from numpy.typing import NDArray
from scipy.optimize import curve_fit


def model(xdata: NDArray, a: float, b: float) -> np.ndarray:
    """Compute forward power in dBm for given acquisition voltage in [0, 10V].

    Parameters
    ----------
    xdata :
        Acquisition voltage at the output of the RF rack, in [0, 10V].
    a :
        Fitting slope in dBm / V.
    b :
        Fitting offset in dBm.

    Returns
    -------
    NDArray :
        Power at the entry of the RF rack, in dBm.

    """
    ydata = a * xdata + b
    return ydata


@dataclass
class Measurement:
    """Hold measured voltage for a power ramp at given frequency and rack."""

    filepath: Path
    rack_name: str

    p_dbm_start: float = -30.0
    p_dbm_end: float = 6.0
    n_p_dbm_points: int = 37
    sep: str = "\t"
    decimal: str = ","

    def __post_init__(self):
        """Auto load and fit."""
        self.frequency_mhz = self._frequency_from_filename()

        self.p_dbm = np.linspace(
            self.p_dbm_start, self.p_dbm_end, self.n_p_dbm_points
        )
        self._full_voltage: NDArray
        self._full_sample: NDArray
        self._sample: NDArray
        self.voltage: NDArray

        # for debug
        # self._print_out_filename_and_info()

        self._load()
        self.a_opti, self.b_opti, self.r_squared = self.fit()

    def __str__(self) -> str:
        """Print the current object."""
        return f"{self.rack_name} @ {self.frequency_mhz:3.0f}MHz"

    def _frequency_from_filename(self) -> float:
        """Get frequency in MHz from file name."""
        filename = self.filepath.name
        after_tiret = filename.split("-")[1]
        before_unit = after_tiret.split("M")[0]
        frequency_mhz = float(before_unit)
        return frequency_mhz

    def _print_out_filename_and_info(self) -> None:
        """Print info for debug."""
        print(f"Loading file {self.filepath}, for rack {str(self)}.")

    def _output(self) -> list[str]:
        """Return information to write in output file."""
        out = [
            f"{self.rack_name}",
            f"{self.frequency_mhz}",
            f"{self.a_opti}",
            f"{self.b_opti}\n",
        ]
        return out

    @classmethod
    def _output_header(cls) -> list[str]:
        """Return header corresponding to ``_output``."""
        out = [
            "Probe",
            "Frequency [MHz]",
            "a [dBm / V]",
            "b [dBm]\n",
        ]
        return out

    def to_write(self, delimiter: str, header: bool = False) -> str:
        """Return formated info to write in output file."""
        if not header:
            return delimiter.join(self._output())
        return delimiter.join(Measurement._output_header())

    def _load(self, column_name: str = "NI9205_Arc2") -> None:
        """Load the file."""
        printc(f"Loading {self.frequency_mhz}")
        data = pd.read_csv(
            self.filepath,
            sep=self.sep,
            decimal=self.decimal,
            usecols=["Sample index", column_name],
        )
        self._full_voltage = data[column_name].to_numpy()
        self._full_sample = data["Sample index"].to_numpy()
        self._exclude_useless()
        self._exclude_first_point_if_level_was_stuck_at_20dbm()

    def _exclude_useless(self) -> None:
        """Exclude data that is not interesting."""
        indexes_to_keep = self._useful_indexes()
        self.voltage = self._full_voltage[indexes_to_keep]
        self._sample = self._full_sample[indexes_to_keep]

    def _exclude_first_point_if_level_was_stuck_at_20dbm(
        self, tol_percent: float = 10.0
    ) -> None:
        """Exclude the first point from the fit if it is incorrect.

        Sometimes, the first measure point is at -20dBm instead of the default
        -30dBm. If first measured voltage is ``tol_percent`` higher (or more)
        than the second, we consider that this error happened.

        """
        threshold_value = self.voltage[1] * (1.0 + 1e-2 * tol_percent)
        if self.voltage[0] < threshold_value:
            return

        printc(
            f"Warning in {str(self)}: measure point @ 30dBm too high, "
            "so we ignore it for the fit. More info in "
            "src/single_measurement.py, "
            "exclude_first_point_if_level_was_stuck_at_20dbm method.",
            color="cyan",
        )
        self.voltage = self.voltage[1:]
        self._sample = self._sample[1:]
        self.p_dbm = self.p_dbm[1:]
        return

    def _useful_indexes(self) -> range:
        """Determine what are the measurements we need."""
        idx_end = np.argmax(self._full_voltage)
        idx_start = idx_end - self.n_p_dbm_points
        return range(idx_start + 1, idx_end + 1)

    def fit(self) -> tuple[float, float, float]:
        """Perform the fit."""
        xdata, ydata = self.voltage, self.p_dbm
        popt, _ = curve_fit(model, xdata=xdata, ydata=ydata)
        a_opti, b_opti = popt
        residuals = ydata - model(xdata, *popt)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
        r_squared = 1.0 - (ss_res / ss_tot)
        return a_opti, b_opti, r_squared

    def plot_fit(self, axe: Axes) -> None:
        """Plot data."""
        (line1,) = axe.plot(
            self.voltage,
            self.p_dbm,
            label=f"{self.rack_name} @{self.frequency_mhz}MHz",
        )
        label = f"a = {self.a_opti:3.2f}, b = {self.b_opti:3.2f}, "
        label += f"R2 = {self.r_squared:3.4f}"
        axe.plot(
            self.voltage,
            model(self.voltage, self.a_opti, self.b_opti),
            color=line1.get_color(),
            ls="--",
            label=label,
            alpha=0.5,
            lw=7.0,
        )

    def plot_as_measured(self, axe: Axes) -> None:
        """Plot what was measured."""
        (line1,) = axe.plot(
            self._full_sample,
            self._full_voltage,
            label=f"{self.rack_name} @{self.frequency_mhz}MHz",
        )

        axe.plot(
            self._sample,
            self.voltage,
            label="For fit",
            color=line1.get_color(),
            lw=5.0,
            alpha=0.5,
        )
