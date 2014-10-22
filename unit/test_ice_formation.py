
import load_dump

def ice_formation(temp, salt, thickness, frazil):
    """
    Calculate frazil ice formation and associated heat flux. 
    """

    return None, None


def test_ice_formation():
    """
    Test formation of frazil ice and associated heat flux. 
    """

    # Load in inputs and call model. 
    test_name = 'test_ice_formation'
    input_names = ['temp', 'salt', 'thickness', 'frazil']
    output_names = ['frazil', 'qice']
    inputs, outputs = load_dump.load(test_name, input_names, output_names) 

    frazil, qice = ice_formation(temp, salt, thickness, frazil)

    # Compare outputs to expected values. 
    self.assert_equal(frazil, outputs['frazil'])
    self.assert_equal(qice, outputs['qice'])
