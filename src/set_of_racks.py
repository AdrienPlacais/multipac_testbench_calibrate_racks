#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Load and store all rack data in the same object."""
import os
from pathlib import Path
from src.rack import Rack


class SetOfRacks(list):
    """Save all racks data in a single object."""

    def __init__(self,
                 base_folder: Path,
                 ) -> None:
        """Create all the racks."""
        folders = [x for x in base_folder.iterdir() if x.is_dir()]

        racks = [Rack(name=folder.name,
                      folder=folder.absolute())
                 for folder in folders]
        racks = sorted(racks, key=lambda r: int(r.name[1]))
        super().__init__(racks)

    def plot_as_measured(self) -> None:
        """Plot all measured data."""
        _ = [rack.plot_as_measured() for rack in self]

    def plot_fit(self) -> None:
        """Plot all fitted data."""
        _ = [rack.plot_fit() for rack in self]

    def save_as_file(self,
                     filepath: str,
                     delimiter: str = '\t') -> None:
        """Save the output in a single file.

        Rack | Freq [MHz] | a | b

        """
        wrote_header = False
        with open(filepath, 'w', encoding='utf-8') as f:
            for rack in self:
                for measurement in rack.measurements:
                    if not wrote_header:
                        f.write(measurement.to_write(delimiter,
                                                     header=True))
                        wrote_header = True

                    f.write(measurement.to_write(delimiter))
