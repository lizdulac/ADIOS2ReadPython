import numpy
import sys
from adios2 import Stream, FileReader

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
                shape = inqrd_varInfo["Shape"]
                print(f"Reading global var {var_name} with shape {shape}")
                #for i in range(0, inqrd_var.shape[1]):
                #    print(str(inqrd_var[i]))
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
                        print(f"step {step} block {block_id} shape {data.shape}")
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
