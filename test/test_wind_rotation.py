
import load_dump


def test_wind_rotation():
    """
    Test that winds are being rotated correctly.

    Look particular geographic locations near the North pole in both the
    atmosphere, ice and ocean. Get the wind directly at these points and
    normalise. Make sure they are the same.
    """

    pass

    # load_dump.load_coupling_fields('om_360x300-unit_test', ['uwnd', 'vwnd'])
    # routine = 'atmo_boundar_layer'
    # inputs = ['uatm', 'vatm']
    # inputs, _ = load_dump.load('om_360x300-unit_test', routine, inputs, [])

    # Choose our point, should be a place where grid cells are going to have
    # different rotations.

    # lat = 1.22317
    # lon = -1.77761

    # Check that there is a non-zero angle at this point.

    # Get the atm and ice grid boxes that corresponds to this location.

    # U and V winds at this location in both atmos and ice.

    # The should not be the same, the ice should have been rotated.
