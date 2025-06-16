"""Hold the measurements at all frequencies of a rack."""

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from multipac_testbench_calibrate_racks.single_measurement import Measurement
from numpy.typing import NDArray


@dataclass
class Rack:
    """Hold measured voltage for power ramps at every frequency."""

    name: str
    folder: Path
    out_folder: Path

    def __post_init__(self) -> None:
        """Auto load and fit."""
        self.fitting_constants: NDArray
        self.measurements: list[Measurement]

        self._number = int(self.name[1])

        self.load_files()

    def load_files(self) -> None:
        """Load all the files from the folder."""
        files = os.listdir(self.folder)
        files = [x for x in self.folder.iterdir() if x.is_file()]

        measurements = [Measurement(filepath, self.name) for filepath in files]
        self.measurements = sorted(measurements, key=lambda m: m.frequency_mhz)
        self.fitting_constants = self.get_fitting_constants(self.measurements)

    def get_fitting_constants(
        self, measurements: list[Measurement]
    ) -> NDArray:
        """Get all fitting constants for a single rack."""
        a_opti = [measure.a_opti for measure in measurements]
        b_opti = [measure.b_opti for measure in measurements]
        fitting_constants = np.vstack((a_opti, b_opti))
        return fitting_constants

    def plot_as_measured(self, save_fig: bool = True) -> None:
        """Plot measured voltage, what was taken for fit."""
        fignum = self._number * 10
        fig = plt.figure(fignum)
        axe = fig.add_subplot(111)

        axe.set_xlabel("Sample index")
        axe.set_ylabel(r"Voltage $[V]$")
        axe.grid(True)
        for measurement in self.measurements:
            measurement.plot_as_measured(axe)
        axe.legend()
        fig.suptitle(self.name)

        if save_fig:
            file_name = Path(self.out_folder, f"{self.name}_measured.png")
            fig.set_size_inches(8, 6)
            fig.savefig(file_name, dpi=100)

    def plot_fit(self, save_fig: bool = True) -> None:
        """Plot the fit results."""
        fignum = self._number * 10 + 1
        fig = plt.figure(fignum)
        axe = fig.add_subplot(111)

        axe.set_xlabel(r"Measured voltage $[V]$")
        axe.set_ylabel(r"RF power $[dBm]$")
        axe.grid(True)
        for measurement in self.measurements:
            measurement.plot_fit(axe)
        axe.legend()
        fig.suptitle(self.name)

        if save_fig:
            file_name = Path(self.out_folder, f"{self.name}_fit.png")
            fig.set_size_inches(8, 6)
            fig.savefig(file_name, dpi=100)

    def save_as_file(self, delimiter: str = "\t") -> None:
        """Save the fitting parameters.

        Rack | Freq [MHz] | a | b

        """
        wrote_header = False
        filepath = Path(self.out_folder, f"{self.name}_fit_calibration.csv")
        with open(filepath, "w", encoding="utf-8") as f:
            for measurement in self.measurements:
                if not wrote_header:
                    f.write(Rack._header_for_file())
                    f.write(measurement.to_write(delimiter, header=True))
                    wrote_header = True
                f.write(measurement.to_write(delimiter))

    @classmethod
    def _header_for_file(cls) -> str:
        """Generate a header."""
        header = f"""# File created on {datetime.now()}.
# Created with "multipac_testbench_calibrate_rf_racks" Python script, available at:
# https://gitlab.in2p3.fr/multipactor/calibrate_rf_racks.git
# https://github.com/AdrienPlacais/multipac_testbench_calibrate_racks
#
# For any question/remark: placais@lpsc.in2p3.fr
#
"""
        return header
