#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hold the measurements at all frequencies of a rack."""
from pathlib import Path
import matplotlib.pyplot as plt
import os
from dataclasses import dataclass
import numpy as np

from src.single_measurement import Measurement


@dataclass
class Rack:
    """Holds all measurements on a single rack."""

    name: str
    folder: Path

    def __post_init__(self) -> None:
        """Auto load and fit."""
        self.fitting_constants: np.ndarray
        self.measurements: list[Measurement]

        self._number = int(self.name[1])

        self.load_files()

    def load_files(self,
                   ) -> None:
        """Load all the files from the folder."""
        files = os.listdir(self.folder)
        files = [x for x in self.folder.iterdir() if x.is_file()]

        measurements = [Measurement(filepath, self.name)
                        for filepath in files]
        self.measurements = sorted(measurements, key=lambda m: m.frequency_mhz)
        self.fitting_constants = self.get_fitting_constants(self.measurements)

    def get_fitting_constants(self, measurements: list[Measurement]
                              ) -> np.ndarray:
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
            file_name = Path(self.folder.parent.parent,
                             f"{self.name}_measured.png")
            fig.set_size_inches(8, 6)
            fig.savefig(file_name, dpi=100)

    def plot_fit(self, save_fig: bool = True) -> None:
        """Plot the fit results."""
        fignum = self._number * 10 + 1
        fig = plt.figure(fignum)
        axe = fig.add_subplot(111)

        axe.set_xlabel(r"Voltage $[V]$")
        axe.set_ylabel(r"RF power $[dBm]$")
        axe.grid(True)
        for measurement in self.measurements:
            measurement.plot_fit(axe)
        axe.legend()
        fig.suptitle(self.name)

        if save_fig:
            file_name = Path(self.folder.parent.parent,
                             f"{self.name}_fit.png")
            fig.set_size_inches(8, 6)
            fig.savefig(file_name, dpi=100)
