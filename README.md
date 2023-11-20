# RF rack calibrator
This small script calibrates the rf racks for the Multipac test bench @LPSC, Grenoble, France.

# How to use
All the measure files produced by LabView must be stored in `data`, in a subdirectory which name is the same as the tested rack: `E1`, `E2`, ... `E8`. 
The measure files must be named: `MesureE<i>-<freq>MHz.csv`, with `<i>` the number of the rack and `<freq>` the frequency in MHz.
The measured voltage is expected to be in the `'NI9205_Arc2'` column, but this can be changed.

From the folder where `main.py` is stored, just run `python main.py` and you should be good.
If you want the plots to appear, you must run the script from your IDE (Spyder, VSCode, ...)
