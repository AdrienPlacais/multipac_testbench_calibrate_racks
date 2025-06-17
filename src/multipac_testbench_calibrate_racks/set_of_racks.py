"""Load and store all rack data in the same object."""

from pathlib import Path

from multipac_testbench_calibrate_racks.rack import Rack


class SetOfRacks(list):
    """Hold measured voltage for power ramps at every freq, every rack."""

    def __init__(self, base_folder: Path, out_folder: Path) -> None:
        """Create all the racks.

        Expected file stucture:
            base_folder/
            ├── E1
            │   ├── MesureE1-100MHz.txt   # holds measured in ``NI9205_Arc2``
            │   ├── MesureE1-120MHz.txt
            │   ├── MesureE1-140MHz.txt
            │   ├── MesureE1-160MHz.txt
            │   ├── MesureE1-180MHz.txt
            │   ├── MesureE1-80MHz.txt
            │   └── MesureE1-88MHz.txt
            ├── E2
            │   ├── MesureE2-100MHz.txt
            ... etc
                └── MesureE7-88MHz.txt

        """
        folders = [x for x in base_folder.iterdir() if x.is_dir()]

        racks = [
            Rack(
                name=folder.name,
                folder=folder.absolute(),
                out_folder=out_folder.absolute(),
            )
            for folder in folders
        ]
        racks = sorted(racks, key=lambda r: int(r.name[1]))
        super().__init__(racks)

    def plot_as_measured(self, save_fig: bool = True) -> None:
        """Plot all measured data."""
        _ = [rack.plot_as_measured(save_fig) for rack in self]

    def plot_fit(self, save_fig: bool = True) -> None:
        """Plot all fitted data."""
        _ = [rack.plot_fit(save_fig) for rack in self]

    def save_as_file(self, delimiter: str = "\t") -> None:
        """Save the fitting parameters."""
        for rack in self:
            rack.save_as_file(delimiter=delimiter)
