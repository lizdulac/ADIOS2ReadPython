import numpy
import sys
from adios2 import Stream, FileReader

# What subset of data to print if a variable is specified
num_read = 3

var_specified = False
if len(sys.argv) > 1:
    var_specified = True
    var_name = sys.argv[1]

with Stream("fs.bp", "rra") as ibpFile:
    varInfo = ibpFile.available_variables()
    if var_specified:
        inqrd_varInfo = varInfo[var_name]
        if inqrd_varInfo is not None:
            inqrd_var = ibpFile.read(var_name)
            if inqrd_varInfo["SingleValue"] == "true":
                # Scalar Value
                print(f"Variable {var_name} is SingleValue with value {inqrd_var}")
            elif inqrd_varInfo["Shape"] != "":
                # Global Array
                var = ibpFile.inquire_variable(var_name)
                data = ibpFile.read(var)
                shape = data.shape
                print(f"Reading global var {var_name} with shape {shape}")
                # Access Data from 1D Global Array
                if len(shape) == 1:
                    print(f" Reading from index 0 to {num_read}:", end=" ")
                    for i in range(0, num_read):
                        print(str(inqrd_var[i]), end=" ")
                    print(f"...")
                # Access Data from 2D Global Array
                elif len(shape) == 2:
                    print(f" Reading from", end="")
                    for i in range(0, num_read):
                        print(f" index ({i}, 0) to ({i}, {num_read}):", end=" ")
                        for j in range(0, num_read):
                            print(str(inqrd_var[i][j]), end=" ")
                        print(f"...")
                    print(f" index ({num_read}, 0) ...")
            else:
                # Local Array
                var = ibpFile.inquire_variable(var_name)
                blocks_info = ibpFile.all_blocks_info(var_name)
                print(f"Reading local var {var_name}") 
                for step in range(var.steps()):
                    for block_id in range(len(blocks_info[step])):
                        var.set_step_selection([step, 1])
                        var.set_block_selection(block_id)
                        data = ibpFile.read(var)
                        shape = data.shape
                        print(f"step {step} block {block_id} shape {shape}")
                        # Access Data from 1D Global Array
                        if len(shape) == 1:
                            print(f" Reading from index 0 to {num_read}:", end=" ")
                            for i in range(0, num_read):
                                print(str(data[i]), end=" ")
                            print(f"...")
                        # Access Data from 2D Global Array
                        elif len(shape) == 2:
                            print(f" Reading from", end="")
                            for i in range(0, num_read):
                                print(f" index ({i}, 0) to ({i}, {num_read}):", end=" ")
                                for j in range(0, num_read):
                                    print(str(data[i][j]), end=" ")
                                print(f"...")
                            print(f" index ({num_read}, 0) ...")

    else:
        for varName in varInfo:
            type = varInfo[varName]["Type"]
            print(f"Reading variable {varName} of type {type}")
            if varInfo[varName]["SingleValue"] == "true":
                value = ibpFile.read(varName)
                print(f"  value: {value}")
            else:
                shape = varInfo[varName]["Shape"]
                print(f"  shape:  {shape}")
            if varInfo[varName]["Type"] != "string":
                min = varInfo[varName]["Min"]
                max = varInfo[varName]["Max"]
                print(f"  min/max:  {min} / {max}")
            print(f"")
