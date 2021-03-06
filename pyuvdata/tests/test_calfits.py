"""Tests for calfits object"""
import nose.tools as nt
import os
import astropy
from astropy.io import fits
from pyuvdata.uvcal import UVCal
import pyuvdata.tests as uvtest
from pyuvdata.data import DATA_PATH
import pyuvdata.utils as uvutils
import numpy as np


def test_readwriteread():
    """
    Omnical fits loopback test.

    Read in uvfits file, write out new uvfits file, read back in and check for
    object equality.
    """
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    write_file = os.path.join(DATA_PATH, 'test/outtest_omnical.fits')
    message = testfile + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message)
    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)

    # test without freq_range parameter
    cal_in.freq_range = None
    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)


def test_readwriteread_delays():
    """
    Read-Write-Read test with a fits calibration files containing delays.

    Read in uvfits file, write out new uvfits file, read back in and check for
    object equality
    """
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.HH.uvc.fits')
    write_file = os.path.join(DATA_PATH, 'test/outtest_firstcal.fits')
    message = [testfile + ' appears to be an old calfits format which',
               testfile + ' appears to be an old calfits format for delay files']
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message,
                         nwarnings=2)
    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)
    del(cal_in)
    del(cal_out)


def test_errors():
    """
    Test for various errors.

    """
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.HH.uvc.fits')
    write_file = os.path.join(DATA_PATH, 'test/outtest_firstcal.fits')
    message = [testfile + ' appears to be an old calfits format which',
               testfile + ' appears to be an old calfits format for delay files']
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message,
                         nwarnings=2)

    cal_in.set_unknown_cal_type()
    nt.assert_raises(ValueError, cal_in.write_calfits, write_file, run_check=False, clobber=True)

    # change values for various axes in flag and total quality hdus to not match primary hdu
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message,
                         nwarnings=2)
    # Create filler jones info
    cal_in.jones_array = np.array([-5, -6, -7, -8])
    cal_in.Njones = 4
    cal_in.flag_array = np.zeros(cal_in._flag_array.expected_shape(cal_in), dtype=bool)
    cal_in.delay_array = np.ones(cal_in._delay_array.expected_shape(cal_in), dtype=np.float64)
    cal_in.quality_array = np.zeros(cal_in._quality_array.expected_shape(cal_in))

    # add total_quality_array so that can be tested as well
    cal_in.total_quality_array = np.zeros(cal_in._total_quality_array.expected_shape(cal_in))

    header_vals_to_double = [{'flag': 'CDELT2'}, {'flag': 'CDELT3'},
                             {'flag': 'CRVAL5'}, {'totqual': 'CDELT1'},
                             {'totqual': 'CDELT2'}, {'totqual': 'CRVAL4'}]
    for i, hdr_dict in enumerate(header_vals_to_double):
        cal_in.write_calfits(write_file, clobber=True)

        unit = hdr_dict.keys()[0]
        keyword = hdr_dict[unit]

        F = fits.open(write_file)
        data = F[0].data
        primary_hdr = F[0].header
        hdunames = uvutils.fits_indexhdus(F)
        ant_hdu = F[hdunames['ANTENNAS']]
        flag_hdu = F[hdunames['FLAGS']]
        flag_hdr = flag_hdu.header
        totqualhdu = F[hdunames['TOTQLTY']]
        totqualhdr = totqualhdu.header

        if unit == 'flag':
            flag_hdr[keyword] *= 2
        elif unit == 'totqual':
            totqualhdr[keyword] *= 2

        prihdu = fits.PrimaryHDU(data=data, header=primary_hdr)
        hdulist = fits.HDUList([prihdu, ant_hdu])
        flag_hdu = fits.ImageHDU(data=flag_hdu.data, header=flag_hdr)
        hdulist.append(flag_hdu)
        totqualhdu = fits.ImageHDU(data=totqualhdu.data, header=totqualhdr)
        hdulist.append(totqualhdu)

        if float(astropy.__version__[0:3]) < 1.3:
            hdulist.writeto(write_file, clobber=True)
        else:
            hdulist.writeto(write_file, overwrite=True)

        nt.assert_raises(ValueError, cal_out.read_calfits, write_file, strict_fits=True)

    # repeat for gain type file
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    write_file = os.path.join(DATA_PATH, 'test/outtest_omnical.fits')
    message = testfile + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message)

    # Create filler jones info
    cal_in.jones_array = np.array([-5, -6, -7, -8])
    cal_in.Njones = 4
    cal_in.flag_array = np.zeros(cal_in._flag_array.expected_shape(cal_in), dtype=bool)
    cal_in.gain_array = np.ones(cal_in._gain_array.expected_shape(cal_in), dtype=np.complex64)
    cal_in.quality_array = np.zeros(cal_in._quality_array.expected_shape(cal_in))

    # add total_quality_array so that can be tested as well
    cal_in.total_quality_array = np.zeros(cal_in._total_quality_array.expected_shape(cal_in))

    header_vals_to_double = [{'totqual': 'CDELT1'}, {'totqual': 'CDELT2'},
                             {'totqual': 'CDELT3'}, {'totqual': 'CRVAL4'}]

    for i, hdr_dict in enumerate(header_vals_to_double):
        cal_in.write_calfits(write_file, clobber=True)

        unit = hdr_dict.keys()[0]
        keyword = hdr_dict[unit]

        F = fits.open(write_file)
        data = F[0].data
        primary_hdr = F[0].header
        hdunames = uvutils.fits_indexhdus(F)
        ant_hdu = F[hdunames['ANTENNAS']]
        totqualhdu = F[hdunames['TOTQLTY']]
        totqualhdr = totqualhdu.header

        if unit == 'totqual':
            totqualhdr[keyword] *= 2

        prihdu = fits.PrimaryHDU(data=data, header=primary_hdr)
        hdulist = fits.HDUList([prihdu, ant_hdu])
        totqualhdu = fits.ImageHDU(data=totqualhdu.data, header=totqualhdr)
        hdulist.append(totqualhdu)

        if float(astropy.__version__[0:3]) < 1.3:
            hdulist.writeto(write_file, clobber=True)
        else:
            hdulist.writeto(write_file, overwrite=True)

        nt.assert_raises(ValueError, cal_out.read_calfits, write_file, strict_fits=True)


def test_extra_keywords():
    cal_in = UVCal()
    cal_out = UVCal()
    calfits_file = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    testfile = os.path.join(DATA_PATH, 'test/outtest_omnical.fits')
    message = calfits_file + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [calfits_file], message=message)

    # check for warnings & errors with extra_keywords that are dicts, lists or arrays
    cal_in.extra_keywords['testdict'] = {'testkey': 23}
    uvtest.checkWarnings(cal_in.check, message=['testdict in extra_keywords is a '
                                                'list, array or dict'])
    nt.assert_raises(TypeError, cal_in.write_calfits, testfile, run_check=False)
    cal_in.extra_keywords.pop('testdict')

    cal_in.extra_keywords['testlist'] = [12, 14, 90]
    uvtest.checkWarnings(cal_in.check, message=['testlist in extra_keywords is a '
                                                'list, array or dict'])
    nt.assert_raises(TypeError, cal_in.write_calfits, testfile, run_check=False)
    cal_in.extra_keywords.pop('testlist')

    cal_in.extra_keywords['testarr'] = np.array([12, 14, 90])
    uvtest.checkWarnings(cal_in.check, message=['testarr in extra_keywords is a '
                                                'list, array or dict'])
    nt.assert_raises(TypeError, cal_in.write_calfits, testfile, run_check=False)
    cal_in.extra_keywords.pop('testarr')

    # check for warnings with extra_keywords keys that are too long
    cal_in.extra_keywords['test_long_key'] = True
    uvtest.checkWarnings(cal_in.check, message=['key test_long_key in extra_keywords '
                                                'is longer than 8 characters'])
    uvtest.checkWarnings(cal_in.write_calfits, [testfile], {'run_check': False,
                                                            'clobber': True},
                         message=['key test_long_key in extra_keywords is longer than 8 characters'])
    cal_in.extra_keywords.pop('test_long_key')

    # check handling of boolean keywords
    cal_in.extra_keywords['bool'] = True
    cal_in.extra_keywords['bool2'] = False
    cal_in.write_calfits(testfile, clobber=True)
    cal_out.read_calfits(testfile)

    nt.assert_equal(cal_in, cal_out)
    cal_in.extra_keywords.pop('bool')
    cal_in.extra_keywords.pop('bool2')

    # check handling of int-like keywords
    cal_in.extra_keywords['int1'] = np.int(5)
    cal_in.extra_keywords['int2'] = 7
    cal_in.write_calfits(testfile, clobber=True)
    cal_out.read_calfits(testfile)

    nt.assert_equal(cal_in, cal_out)
    cal_in.extra_keywords.pop('int1')
    cal_in.extra_keywords.pop('int2')

    # check handling of float-like keywords
    cal_in.extra_keywords['float1'] = np.int64(5.3)
    cal_in.extra_keywords['float2'] = 6.9
    cal_in.write_calfits(testfile, clobber=True)
    cal_out.read_calfits(testfile)

    nt.assert_equal(cal_in, cal_out)
    cal_in.extra_keywords.pop('float1')
    cal_in.extra_keywords.pop('float2')

    # check handling of complex-like keywords
    cal_in.extra_keywords['complex1'] = np.complex64(5.3 + 1.2j)
    cal_in.extra_keywords['complex2'] = 6.9 + 4.6j
    cal_in.write_calfits(testfile, clobber=True)
    cal_out.read_calfits(testfile)

    nt.assert_equal(cal_in, cal_out)
    cal_in.extra_keywords.pop('complex1')
    cal_in.extra_keywords.pop('complex2')

    # check handling of comment keywords
    cal_in.extra_keywords['comment'] = ('this is a very long comment that will '
                                        'be broken into several lines\nif '
                                        'everything works properly.')
    cal_in.write_calfits(testfile, clobber=True)
    cal_out.read_calfits(testfile)

    nt.assert_equal(cal_in, cal_out)


def test_read_oldcalfits():
    """
    Test for proper behavior with old calfits files.
    """
    # start with gain type files
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    write_file = os.path.join(DATA_PATH, 'test/outtest_omnical.fits')
    message = testfile + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message)

    # add total_quality_array so that can be tested as well
    cal_in.total_quality_array = np.zeros(cal_in._total_quality_array.expected_shape(cal_in))

    # now read in the file and remove various CRPIX and CRVAL keywords to
    # emulate old calfits files
    header_vals_to_remove = [{'primary': 'CRVAL5'}, {'primary': 'CRPIX4'},
                             {'totqual': 'CRVAL4'}]
    messages = [write_file, 'This file', write_file]
    messages = [m + ' appears to be an old calfits format' for m in messages]
    for i, hdr_dict in enumerate(header_vals_to_remove):
        cal_in.write_calfits(write_file, clobber=True)

        unit = hdr_dict.keys()[0]
        keyword = hdr_dict[unit]

        F = fits.open(write_file)
        data = F[0].data
        primary_hdr = F[0].header
        hdunames = uvutils.fits_indexhdus(F)
        ant_hdu = F[hdunames['ANTENNAS']]
        totqualhdu = F[hdunames['TOTQLTY']]
        totqualhdr = totqualhdu.header

        if unit == 'primary':
            primary_hdr.pop(keyword)
        elif unit == 'totqual':
            totqualhdr.pop(keyword)

        prihdu = fits.PrimaryHDU(data=data, header=primary_hdr)
        hdulist = fits.HDUList([prihdu, ant_hdu])
        totqualhdu = fits.ImageHDU(data=totqualhdu.data, header=totqualhdr)
        hdulist.append(totqualhdu)

        if float(astropy.__version__[0:3]) < 1.3:
            hdulist.writeto(write_file, clobber=True)
        else:
            hdulist.writeto(write_file, overwrite=True)

        uvtest.checkWarnings(cal_out.read_calfits, [write_file], message=messages[i])
        nt.assert_equal(cal_in, cal_out)
        nt.assert_raises(KeyError, cal_out.read_calfits, write_file, strict_fits=True)

    # now with delay type files
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.HH.uvc.fits')
    write_file = os.path.join(DATA_PATH, 'test/outtest_firstcal.fits')
    message = [testfile + ' appears to be an old calfits format which',
               testfile + ' appears to be an old calfits format for delay files']
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message,
                         nwarnings=2)

    # add total_quality_array so that can be tested as well
    cal_in.total_quality_array = np.zeros(cal_in._total_quality_array.expected_shape(cal_in))

    # now read in the file and remove various CRPIX and CRVAL keywords to
    # emulate old calfits files
    header_vals_to_remove = [{'primary': 'CRVAL5'}, {'flag': 'CRVAL5'},
                             {'flag': 'CRPIX4'}, {'totqual': 'CRVAL4'}]
    messages = [write_file, 'This file', 'This file', write_file]
    messages = [m + ' appears to be an old calfits format' for m in messages]
    for i, hdr_dict in enumerate(header_vals_to_remove):
        cal_in.write_calfits(write_file, clobber=True)

        unit = hdr_dict.keys()[0]
        keyword = hdr_dict[unit]

        F = fits.open(write_file)
        data = F[0].data
        primary_hdr = F[0].header
        hdunames = uvutils.fits_indexhdus(F)
        ant_hdu = F[hdunames['ANTENNAS']]
        flag_hdu = F[hdunames['FLAGS']]
        flag_hdr = flag_hdu.header
        totqualhdu = F[hdunames['TOTQLTY']]
        totqualhdr = totqualhdu.header

        if unit == 'primary':
            primary_hdr.pop(keyword)
        elif unit == 'flag':
            flag_hdr.pop(keyword)
        elif unit == 'totqual':
            totqualhdr.pop(keyword)

        prihdu = fits.PrimaryHDU(data=data, header=primary_hdr)
        hdulist = fits.HDUList([prihdu, ant_hdu])
        flag_hdu = fits.ImageHDU(data=flag_hdu.data, header=flag_hdr)
        hdulist.append(flag_hdu)
        totqualhdu = fits.ImageHDU(data=totqualhdu.data, header=totqualhdr)
        hdulist.append(totqualhdu)

        if float(astropy.__version__[0:3]) < 1.3:
            hdulist.writeto(write_file, clobber=True)
        else:
            hdulist.writeto(write_file, overwrite=True)

        uvtest.checkWarnings(cal_out.read_calfits, [write_file], message=messages[i])
        nt.assert_equal(cal_in, cal_out)
        nt.assert_raises(KeyError, cal_out.read_calfits, write_file, strict_fits=True)


def test_input_flag_array():
    """
    Test when data file has input flag array.

    Currently we do not have a testfile, so we will artifically create one
    and check for internal consistency.
    """
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    write_file = os.path.join(DATA_PATH, 'test/outtest_input_flags.fits')
    message = testfile + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message)
    cal_in.input_flag_array = np.zeros(cal_in._input_flag_array.expected_shape(cal_in), dtype=bool)
    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)

    # Repeat for delay version
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.HH.uvc.fits')
    message = [testfile + ' appears to be an old calfits format which',
               testfile + ' appears to be an old calfits format for delay files']
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message,
                         nwarnings=2)
    cal_in.input_flag_array = np.zeros(cal_in._input_flag_array.expected_shape(cal_in), dtype=bool)
    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)
    del(cal_in)
    del(cal_out)


def test_jones():
    """
    Test when data file has more than one element in Jones matrix.

    Currently we do not have a testfile, so we will artifically create one
    and check for internal consistency.
    """
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    write_file = os.path.join(DATA_PATH, 'test/outtest_jones.fits')
    message = testfile + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message)

    # Create filler jones info
    cal_in.jones_array = np.array([-5, -6, -7, -8])
    cal_in.Njones = 4
    cal_in.flag_array = np.zeros(cal_in._flag_array.expected_shape(cal_in), dtype=bool)
    cal_in.gain_array = np.ones(cal_in._gain_array.expected_shape(cal_in), dtype=np.complex64)
    cal_in.quality_array = np.zeros(cal_in._quality_array.expected_shape(cal_in))

    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)

    # Repeat for delay version
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.HH.uvc.fits')
    message = [testfile + ' appears to be an old calfits format which',
               testfile + ' appears to be an old calfits format for delay files']
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message,
                         nwarnings=2)

    # Create filler jones info
    cal_in.jones_array = np.array([-5, -6, -7, -8])
    cal_in.Njones = 4
    cal_in.flag_array = np.zeros(cal_in._flag_array.expected_shape(cal_in), dtype=bool)
    cal_in.delay_array = np.ones(cal_in._delay_array.expected_shape(cal_in), dtype=np.float64)
    cal_in.quality_array = np.zeros(cal_in._quality_array.expected_shape(cal_in))

    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)
    del(cal_in)
    del(cal_out)


def test_readwriteread_total_quality_array():
    """
    Test when data file has a total quality array.

    Currently we have no such file, so we will artificially create one and
    check for internal consistency.
    """
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    write_file = os.path.join(DATA_PATH, 'test/outtest_total_quality_array.fits')
    message = testfile + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message)

    # Create filler total quality array
    cal_in.total_quality_array = np.zeros(cal_in._total_quality_array.expected_shape(cal_in))

    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)
    del(cal_in)
    del(cal_out)

    # also test delay-type calibrations
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.HH.uvc.fits')
    write_file = os.path.join(DATA_PATH, 'test/outtest_total_quality_array_delays.fits')
    message = [testfile + ' appears to be an old calfits format which',
               testfile + ' appears to be an old calfits format for delay files']
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message,
                         nwarnings=2)

    cal_in.total_quality_array = np.zeros(cal_in._total_quality_array.expected_shape(cal_in))

    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)
    del(cal_in)
    del(cal_out)


def test_total_quality_array_size():
    """
    Test that total quality array defaults to the proper size
    """

    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    message = testfile + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message)

    # Create filler total quality array
    cal_in.total_quality_array = np.zeros(cal_in._total_quality_array.expected_shape(cal_in))

    proper_shape = (cal_in.Nspws, cal_in.Nfreqs, cal_in.Ntimes, cal_in.Njones)
    nt.assert_equal(cal_in.total_quality_array.shape, proper_shape)
    del(cal_in)

    # also test delay-type calibrations
    cal_in = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.HH.uvc.fits')
    message = [testfile + ' appears to be an old calfits format which',
               testfile + ' appears to be an old calfits format for delay files']
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message,
                         nwarnings=2)

    cal_in.total_quality_array = np.zeros(cal_in._total_quality_array.expected_shape(cal_in))

    proper_shape = (cal_in.Nspws, 1, cal_in.Ntimes, cal_in.Njones)
    nt.assert_equal(cal_in.total_quality_array.shape, proper_shape)
    del(cal_in)


def test_write_time_precision():
    """
    Test that times are being written to appropriate precision (see issue 311).
    """
    cal_in = UVCal()
    cal_out = UVCal()
    testfile = os.path.join(DATA_PATH, 'zen.2457698.40355.xx.fitsA')
    write_file = os.path.join(DATA_PATH, 'test/outtest_omnical.fits')
    message = testfile + ' appears to be an old calfits format which'
    uvtest.checkWarnings(cal_in.read_calfits, [testfile], message=message)
    # overwrite time array to break old code
    dt = cal_in.integration_time / (24. * 60. * 60.)
    cal_in.time_array = dt * np.arange(cal_in.Ntimes)
    cal_in.write_calfits(write_file, clobber=True)
    cal_out.read_calfits(write_file)
    nt.assert_equal(cal_in, cal_out)
