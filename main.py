#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Treat all the rack data."""
from pathlib import Path
import matplotlib.pyplot as plt

from src.set_of_racks import SetOfRacks
plt.close('all')

# Must contain all measurement files, in folders named "E1", "E2", etc
base_folder = Path('data', 'measurements')
out_folder = Path('data', 'results')
all_racks = SetOfRacks(base_folder, out_folder)

# To plot the measurements, with an highlight on the data retained for the
# linear curve fitting
all_racks.plot_as_measured()

# To plot the P_dBm vs Voltage, as measured and with the fitted line
all_racks.plot_fit()

# To save data
all_racks.save_as_file()
