# ADIOS2ReadPython

Example of reading bp file "fs.bp" with python.

Run
$ python bpReadEx.py

To print out all variables found in file "fs.bp" such as...

Reading variable a of type float
  value: 7.0
  min/max:  7 / 7

Reading variable b of type string
  value: width

Reading variable c of type int32_t
  shape:  
  min/max:  -6 / 6

Reading variable d of type double
  shape:  200, 400
  min/max:  -1.43949e-16 / 1.65552e-16
  
...


Or, choose a specific variable (for example, variable "varx") to read by running
$ python bpReadEx.py varx

The output will depend on what varx is. For example if varx is..

A scalar:
Variable varx is SingleValue with value 3.14159

A global variable:
Reading global var varx with shape (150, 500)
 Reading from index (0, 0) to (0, 3): -1.234567890123456e-12 -2.345678901234567e-13 -3.456789012345678e-14 ...
 index (1, 0) to (1, 3): -4.567890123456789e-13 -5.678901234567890e-15 -6.789012345678901e-14 ...
 index (2, 0) to (2, 3): -7.890123456789012e-16 -8.901234567890123e-15 -9.012345678901234e-15 ...
 index (3, 0) ...

A local variable:
Reading local var varx
step 0 block 0 shape (150,)
 Reading from index 0 to 3: 1.0 -2.0 3.0 ...


This program only supports 1D and 2D variables, even though local and global variables can be of any dimensionality. The shape of local variables is not printed when all variables are printed since the shape could be different per block.