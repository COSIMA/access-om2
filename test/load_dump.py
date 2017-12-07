
import netCDF4 as nc


def load(exp, routine, input_names, output_names):
    """
    Load the input and output data for a particular unit test.
    """

    inputs = {}
    outputs = {}

    for i in input_names:
        with nc.Dataset(routine + '-' + i) as f:
            inputs[i] = f.variables[i].data

    for o in output_names:
        with nc.Dataset(routine + '-' + o) as f:
            outputs[o] = f.variables[o].data

    return inputs, outputs


def load_coupling_fields(exp, field_names):
    """

    """
