# RF rack calibrator
This small script calibrates the rf racks for the MULTIPAC test bench @LPSC, Grenoble, France.

## Installation
1. Clone the repository:
```bash
git clone git@github.com:AdrienPlacais/multipac_testbench_calibrate_racks.git
```
2. Create a dedicated Python environment, activate it.
3. Navigate to the main folder and install the library with all dependencies:
```bash
pip install -e .
```

> [!NOTE]
> If you are completely new to Python and these instructions are unclear, check [this tutorial](https://python-guide.readthedocs.io/en/latest/).
> In particular, you will want to:
> 1. [Install Python](https://python-guide.readthedocs.io/en/latest/starting/installation/) 3.11 or higher.
> 2. [Learn to use Python environments](https://python-guide.readthedocs.io/en/latest/dev/virtualenvs/), `pipenv` or `virtualenv`.
> 3. [Install a Python IDE](https://python-guide.readthedocs.io/en/latest/dev/env/#ides) such as Spyder or VSCode.


## How to use

Plug signal generator to input of RF rack, plug 0/10V output to the Arc2 output, perform power sweeps.

> [!INFO]
> In version 0.1.0 and earlier, power sweep had to be -30dBm to 6dBm, one point per dBm.
> In version 0.1.1 and later, power has to be stored in `NI9205_dBm` columns.

Expected file structure:

```bash
base_folder/
├── E1
│   ├── MesureE1-100MHz.txt   # holds measured voltage in ``NI9205_Arc2``
│   ├── MesureE1-120MHz.txt   # 0.1.1 and later, also input power in ``NI9205_dBm``
│   ├── MesureE1-140MHz.txt
│   ├── MesureE1-160MHz.txt
│   ├── MesureE1-180MHz.txt
│   ├── MesureE1-80MHz.txt
│   └── MesureE1-88MHz.txt
├── E2
│   ├── MesureE2-100MHz.txt
... etc
    └── MesureE7-88MHz.txt
```

Example data is provided in `data/measurements`.
An example script is provided in `src/multipac_testbench_calibrate_racks/main.py`.

# TODO
- [ ] Remove illegal quoting in results file
- [X] Cleaner installation instructions
- [ ] Complete documentation
