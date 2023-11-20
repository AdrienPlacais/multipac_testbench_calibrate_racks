#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hold the measurements at all frequencies of a rack."""
import matplotlib.pyplot as plt
import os
from dataclasses import dataclass
import numpy as np

from src.single_measurement import Measurement


@dataclass
class Rack:
    """Holds all measurements on a single rack."""

    name: str
    folder: str

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

        measurements = [Measurement(os.path.join(self.folder, filepath),
                                    self.name)
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

    def plot_as_measured(self) -> None:
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

    def plot_fit(self) -> None:
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
