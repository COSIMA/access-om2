
import netCDF4 as nc

def load(test_name, input_names, output_names):
    """
    Load the input and output data for a particular unit test. 
    """

    path = './output/'
    
    inputs = {}
    outputs = {}

    for i in input_names:
        with nc.Dataset(test_name + '-' i) as f:
            inputs[i] = f.variables[i].data

    for o in output_names:
        with nc.Dataset(test_name + '-' o) as f:
            outputs[o] = f.variables[o].data

    return inputs, outputs
