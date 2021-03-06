"""Tests for telescope objects and functions."""
import numpy as np
import nose.tools as nt
import pyuvdata

required_parameters = ['_telescope_name', '_telescope_location']
required_properties = ['telescope_name', 'telescope_location']
extra_parameters = ['_antenna_diameters']
extra_properties = ['antenna_diameters']
other_attributes = ['citation', 'telescope_location_lat_lon_alt',
                    'telescope_location_lat_lon_alt_degrees',
                    'pyuvdata_version_str']
expected_known_telescopes = ['PAPER', 'HERA', 'MWA']


# Tests for Telescope object
def test_parameter_iter():
    "Test expected parameters."
    telescope_obj = pyuvdata.Telescope()
    all = []
    for prop in telescope_obj:
        all.append(prop)
    for a in required_parameters:
        nt.assert_true(a in all, msg='expected attribute ' + a
                       + ' not returned in object iterator')


def test_required_parameter_iter():
    "Test expected required parameters."
    telescope_obj = pyuvdata.Telescope()
    required = []
    for prop in telescope_obj.required():
        required.append(prop)
    for a in required_parameters:
        nt.assert_true(a in required, msg='expected attribute ' + a
                       + ' not returned in required iterator')


def test_extra_parameter_iter():
    "Test expected optional parameters."
    telescope_obj = pyuvdata.Telescope()
    extra = []
    for prop in telescope_obj.extra():
        extra.append(prop)
    for a in extra_parameters:
        nt.assert_true(a in extra, msg='expected attribute ' + a
                       + ' not returned in extra iterator')


def test_unexpected_parameters():
    "Test for extra parameters."
    telescope_obj = pyuvdata.Telescope()
    expected_parameters = required_parameters + extra_parameters
    attributes = [i for i in telescope_obj.__dict__.keys() if i[0] == '_']
    for a in attributes:
        nt.assert_true(a in expected_parameters,
                       msg='unexpected parameter ' + a + ' found in Telescope')


def test_unexpected_attributes():
    "Test for extra attributes."
    telescope_obj = pyuvdata.Telescope()
    expected_attributes = required_properties + other_attributes
    attributes = [i for i in telescope_obj.__dict__.keys() if i[0] != '_']
    for a in attributes:
        nt.assert_true(a in expected_attributes,
                       msg='unexpected attribute ' + a + ' found in Telescope')


def test_properties():
    "Test that properties can be get and set properly."
    telescope_obj = pyuvdata.Telescope()
    prop_dict = dict(zip(required_properties, required_parameters))
    for k, v in prop_dict.iteritems():
        rand_num = np.random.rand()
        setattr(telescope_obj, k, rand_num)
        this_param = getattr(telescope_obj, v)
        try:
            nt.assert_equal(rand_num, this_param.value)
        except(AssertionError):
            print('setting {prop_name} to a random number failed'.format(prop_name=k))
            raise


def test_known_telescopes():
    """Test known_telescopes function returns expected results."""
    nt.assert_equal(pyuvdata.known_telescopes().sort(), expected_known_telescopes.sort())
