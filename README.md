# RF rack calibrator

This small script calibrates the rf racks for the Multipac test bench @LPSC,
Grenoble, France.

# How to use
All the measure file must be stored in `data`, in a subdirectory wich name is
the same as the tested rack: `E1`, `E2`, ... `E8`. The measured voltage is
expected to be in the `'NI9205_Arc2'` column, but this can be changed.

From the folder where `main.py` is stored, just run `python main.py` and you
should be good.
If you want the plots to appear, you must run the script from your IDE (Spyder, VSCode, ...)
