"""Tests for UVFITS object."""
import numpy as np
import copy
import os
import nose.tools as nt
import astropy
from astropy.io import fits
from pyuvdata import UVData
import pyuvdata.utils as uvutils
import pyuvdata.tests as uvtest
from pyuvdata.data import DATA_PATH


def test_ReadNRAO():
    """Test reading in a CASA tutorial uvfits file."""
    UV = UVData()
    testfile = os.path.join(DATA_PATH, 'day2_TDEM0003_10s_norx_1src_1spw.uvfits')
    expected_extra_keywords = ['OBSERVER', 'SORTORD', 'SPECSYS',
                               'RESTFREQ', 'ORIGIN']
    uvtest.checkWarnings(UV.read_uvfits, [testfile], message='Telescope EVLA is not')
    nt.assert_equal(expected_extra_keywords.sort(),
                    UV.extra_keywords.keys().sort())

    # test reading in header data first, then metadata and then data
    UV2 = UVData()
    uvtest.checkWarnings(UV2.read_uvfits, [testfile], {'read_data': False, 'read_metadata': False},
                         message='Telescope EVLA is not')
    nt.assert_equal(expected_extra_keywords.sort(),
                    UV2.extra_keywords.keys().sort())
    nt.assert_raises(ValueError, UV2.check)
    UV2.read_uvfits_metadata(testfile)
    nt.assert_raises(ValueError, UV2.check)
    UV2.read_uvfits_data(testfile)
    nt.assert_equal(UV, UV2)

    # test reading in header data first, then metadata & data
    UV2 = UVData()
    uvtest.checkWarnings(UV2.read_uvfits, [testfile], {'read_data': False, 'read_metadata': False},
                         message='Telescope EVLA is not')
    nt.assert_equal(expected_extra_keywords.sort(),
                    UV2.extra_keywords.keys().sort())
    nt.assert_raises(ValueError, UV2.check)
    UV2.read_uvfits_data(testfile)
    nt.assert_equal(UV, UV2)

    del(UV)


def test_noSPW():
    """Test reading in a PAPER uvfits file with no spw axis."""
    UV = UVData()
    testfile_no_spw = os.path.join(DATA_PATH, 'zen.2456865.60537.xy.uvcRREAAM.uvfits')
    uvtest.checkWarnings(UV.read_uvfits, [testfile_no_spw], known_warning='paper_uvfits')
    del(UV)


# this test commented out because the file is too large to include in the repo
# def test_readRTS():
#    """Test reading in an RTS UVFITS file."""
#     UV = UVData()
#     testfile = os.path.join(DATA_PATH, 'pumav2_SelfCal300_Peel300_01.uvfits')
#     test = UV.read_uvfits(testfile)
#     nt.assert_true(test)

def test_breakReadUVFits():
    """Test errors on reading in a uvfits file with subarrays and other problems."""
    UV = UVData()
    multi_subarray_file = os.path.join(DATA_PATH, 'multi_subarray.uvfits')
    uvtest.checkWarnings(nt.assert_raises, [ValueError, UV.read_uvfits, multi_subarray_file],
                         message='Telescope EVLA is not')

    del(UV)


def test_spwnotsupported():
    """Test errors on reading in a uvfits file with multiple spws."""
    UV = UVData()
    testfile = os.path.join(DATA_PATH, 'day2_TDEM0003_10s_norx_1scan.uvfits')
    nt.assert_raises(ValueError, UV.read_uvfits, testfile)
    del(UV)


def test_readwriteread():
    """
    CASA tutorial uvfits loopback test.

    Read in uvfits file, write out new uvfits file, read back in and check for
    object equality.
    """
    uv_in = UVData()
    uv_out = UVData()
    testfile = os.path.join(DATA_PATH, 'day2_TDEM0003_10s_norx_1src_1spw.uvfits')
    write_file = os.path.join(DATA_PATH, 'test/outtest_casa.uvfits')
    uvtest.checkWarnings(uv_in.read_uvfits, [testfile], message='Telescope EVLA is not')
    uv_in.write_uvfits(write_file)
    uvtest.checkWarnings(uv_out.read_uvfits, [write_file], message='Telescope EVLA is not')
    nt.assert_equal(uv_in, uv_out)

    # check that if x_orientation is set, it's read back out properly
    uv_in.x_orientation = 'east'
    uv_in.write_uvfits(write_file)
    uvtest.checkWarnings(uv_out.read_uvfits, [write_file], message='Telescope EVLA is not')
    nt.assert_equal(uv_in, uv_out)

    # check that if antenna_diameters is set, it's read back out properly
    uvtest.checkWarnings(uv_in.read_uvfits, [testfile], message='Telescope EVLA is not')
    uv_in.antenna_diameters = np.zeros((uv_in.Nants_telescope,), dtype=np.float) + 14.0
    uv_in.write_uvfits(write_file)
    uvtest.checkWarnings(uv_out.read_uvfits, [write_file], message='Telescope EVLA is not')
    nt.assert_equal(uv_in, uv_out)

    # check error if timesys is 'IAT'
    uv_in.timesys = 'IAT'
    nt.assert_raises(ValueError, uv_in.write_uvfits, write_file)
    uv_in.timesys = 'UTC'

    # check that unflagged data with nsample = 0 will cause warnings
    uv_in.nsample_array[range(11, 22)] = 0
    uv_in.flag_array[range(11, 22)] = False
    uvtest.checkWarnings(uv_in.write_uvfits, [write_file], message='Some unflagged data has nsample = 0')

    del(uv_in)
    del(uv_out)


def test_extra_keywords():
    uv_in = UVData()
    uv_out = UVData()
    uvfits_file = os.path.join(DATA_PATH, 'day2_TDEM0003_10s_norx_1src_1spw.uvfits')
    testfile = os.path.join(DATA_PATH, 'test/outtest_casa.uvfits')
    uvtest.checkWarnings(uv_in.read_uvfits, [uvfits_file], message='Telescope EVLA is not')

    # check for warnings & errors with extra_keywords that are dicts, lists or arrays
    uv_in.extra_keywords['testdict'] = {'testkey': 23}
    uvtest.checkWarnings(uv_in.check, message=['testdict in extra_keywords is a '
                                               'list, array or dict'])
    nt.assert_raises(TypeError, uv_in.write_uvfits, testfile, run_check=False)
    uv_in.extra_keywords.pop('testdict')

    uv_in.extra_keywords['testlist'] = [12, 14, 90]
    uvtest.checkWarnings(uv_in.check, message=['testlist in extra_keywords is a '
                                               'list, array or dict'])
    nt.assert_raises(TypeError, uv_in.write_uvfits, testfile, run_check=False)
    uv_in.extra_keywords.pop('testlist')

    uv_in.extra_keywords['testarr'] = np.array([12, 14, 90])
    uvtest.checkWarnings(uv_in.check, message=['testarr in extra_keywords is a '
                                               'list, array or dict'])
    nt.assert_raises(TypeError, uv_in.write_uvfits, testfile, run_check=False)
    uv_in.extra_keywords.pop('testarr')

    # check for warnings with extra_keywords keys that are too long
    uv_in.extra_keywords['test_long_key'] = True
    uvtest.checkWarnings(uv_in.check, message=['key test_long_key in extra_keywords '
                                               'is longer than 8 characters'])
    uvtest.checkWarnings(uv_in.write_uvfits, [testfile], {'run_check': False},
                         message=['key test_long_key in extra_keywords is longer than 8 characters'])
    uv_in.extra_keywords.pop('test_long_key')

    # check handling of boolean keywords
    uv_in.extra_keywords['bool'] = True
    uv_in.extra_keywords['bool2'] = False
    uv_in.write_uvfits(testfile)
    uvtest.checkWarnings(uv_out.read_uvfits, [testfile], message='Telescope EVLA is not')

    nt.assert_equal(uv_in, uv_out)
    uv_in.extra_keywords.pop('bool')
    uv_in.extra_keywords.pop('bool2')

    # check handling of int-like keywords
    uv_in.extra_keywords['int1'] = np.int(5)
    uv_in.extra_keywords['int2'] = 7
    uv_in.write_uvfits(testfile)
    uvtest.checkWarnings(uv_out.read_uvfits, [testfile], message='Telescope EVLA is not')

    nt.assert_equal(uv_in, uv_out)
    uv_in.extra_keywords.pop('int1')
    uv_in.extra_keywords.pop('int2')

    # check handling of float-like keywords
    uv_in.extra_keywords['float1'] = np.int64(5.3)
    uv_in.extra_keywords['float2'] = 6.9
    uv_in.write_uvfits(testfile)
    uvtest.checkWarnings(uv_out.read_uvfits, [testfile], message='Telescope EVLA is not')

    nt.assert_equal(uv_in, uv_out)
    uv_in.extra_keywords.pop('float1')
    uv_in.extra_keywords.pop('float2')

    # check handling of complex-like keywords
    uv_in.extra_keywords['complex1'] = np.complex64(5.3 + 1.2j)
    uv_in.extra_keywords['complex2'] = 6.9 + 4.6j
    uv_in.write_uvfits(testfile)
    uvtest.checkWarnings(uv_out.read_uvfits, [testfile], message='Telescope EVLA is not')

    nt.assert_equal(uv_in, uv_out)
    uv_in.extra_keywords.pop('complex1')
    uv_in.extra_keywords.pop('complex2')

    # check handling of comment keywords
    uv_in.extra_keywords['comment'] = ('this is a very long comment that will '
                                       'be broken into several lines\nif '
                                       'everything works properly.')
    uv_in.write_uvfits(testfile)
    uvtest.checkWarnings(uv_out.read_uvfits, [testfile], message='Telescope EVLA is not')

    nt.assert_equal(uv_in, uv_out)


def test_select_read():
    uvfits_uv = UVData()
    uvfits_uv2 = UVData()
    uvfits_file = os.path.join(DATA_PATH, 'day2_TDEM0003_10s_norx_1src_1spw.uvfits')

    # select on antennas
    ants_to_keep = np.array([0, 19, 11, 24, 3, 23, 1, 20, 21])
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfits_file],
                         {'antenna_nums': ants_to_keep},
                         message='Telescope EVLA is not')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [uvfits_file],
                         message='Telescope EVLA is not')
    uvfits_uv2.select(antenna_nums=ants_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)

    # select on frequency channels
    chans_to_keep = np.arange(12, 22)
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfits_file],
                         {'freq_chans': chans_to_keep},
                         message='Telescope EVLA is not')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [uvfits_file],
                         message='Telescope EVLA is not')
    uvfits_uv2.select(freq_chans=chans_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)

    # select on pols
    pols_to_keep = [-1, -2]
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfits_file],
                         {'polarizations': pols_to_keep},
                         message='Telescope EVLA is not')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [uvfits_file],
                         message='Telescope EVLA is not')
    uvfits_uv2.select(polarizations=pols_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)

    # now test selecting on multiple axes
    # frequencies first
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfits_file],
                         {'antenna_nums': ants_to_keep,
                          'freq_chans': chans_to_keep,
                          'polarizations': pols_to_keep},
                         message='Telescope EVLA is not')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [uvfits_file],
                         message='Telescope EVLA is not')
    uvfits_uv2.select(antenna_nums=ants_to_keep, freq_chans=chans_to_keep,
                      polarizations=pols_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)

    # baselines first
    ants_to_keep = np.array([0, 1])
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfits_file],
                         {'antenna_nums': ants_to_keep,
                          'freq_chans': chans_to_keep,
                          'polarizations': pols_to_keep},
                         message='Telescope EVLA is not')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [uvfits_file],
                         message='Telescope EVLA is not')
    uvfits_uv2.select(antenna_nums=ants_to_keep, freq_chans=chans_to_keep,
                      polarizations=pols_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)

    # polarizations first
    ants_to_keep = np.array([0, 1, 2, 3, 6, 7, 8, 11, 14, 18, 19, 20, 21, 22])
    chans_to_keep = np.arange(12, 64)
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfits_file],
                         {'antenna_nums': ants_to_keep,
                          'freq_chans': chans_to_keep,
                          'polarizations': pols_to_keep},
                         message='Telescope EVLA is not')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [uvfits_file],
                         message='Telescope EVLA is not')
    uvfits_uv2.select(antenna_nums=ants_to_keep, freq_chans=chans_to_keep,
                      polarizations=pols_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)

    # repeat with no spw file
    uvfitsfile_no_spw = os.path.join(DATA_PATH, 'zen.2456865.60537.xy.uvcRREAAM.uvfits')

    # select on antennas
    ants_to_keep = np.array([2, 4, 5])
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfitsfile_no_spw],
                         {'antenna_nums': ants_to_keep},
                         known_warning='paper_uvfits')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [uvfitsfile_no_spw],
                         known_warning='paper_uvfits')
    uvfits_uv2.select(antenna_nums=ants_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)

    # select on frequency channels
    chans_to_keep = np.arange(4, 8)
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfitsfile_no_spw],
                         {'freq_chans': chans_to_keep},
                         known_warning='paper_uvfits')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [uvfitsfile_no_spw],
                         known_warning='paper_uvfits')
    uvfits_uv2.select(freq_chans=chans_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)

    # select on pols
    # this requires writing a new file because the no spw file we have has only 1 pol
    hdu_list = fits.open(uvfits_file)
    hdunames = uvutils.fits_indexhdus(hdu_list)
    vis_hdu = hdu_list[0]
    vis_hdr = vis_hdu.header.copy()
    raw_data_array = vis_hdu.data.data
    raw_data_array = raw_data_array[:, :, :, 0, :, :, :]

    vis_hdr['NAXIS'] = 6

    vis_hdr['NAXIS5'] = vis_hdr['NAXIS6']
    vis_hdr['CTYPE5'] = vis_hdr['CTYPE6']
    vis_hdr['CRVAL5'] = vis_hdr['CRVAL6']
    vis_hdr['CDELT5'] = vis_hdr['CDELT6']
    vis_hdr['CRPIX5'] = vis_hdr['CRPIX6']
    vis_hdr['CROTA5'] = vis_hdr['CROTA6']

    vis_hdr['NAXIS6'] = vis_hdr['NAXIS7']
    vis_hdr['CTYPE6'] = vis_hdr['CTYPE7']
    vis_hdr['CRVAL6'] = vis_hdr['CRVAL7']
    vis_hdr['CDELT6'] = vis_hdr['CDELT7']
    vis_hdr['CRPIX6'] = vis_hdr['CRPIX7']
    vis_hdr['CROTA6'] = vis_hdr['CROTA7']

    vis_hdr.pop('NAXIS7')
    vis_hdr.pop('CTYPE7')
    vis_hdr.pop('CRVAL7')
    vis_hdr.pop('CDELT7')
    vis_hdr.pop('CRPIX7')
    vis_hdr.pop('CROTA7')

    par_names = vis_hdu.data.parnames

    group_parameter_list = [vis_hdu.data.par(ind) for
                            ind in range(len(par_names))]

    vis_hdu = fits.GroupData(raw_data_array, parnames=par_names,
                             pardata=group_parameter_list, bitpix=-32)
    vis_hdu = fits.GroupsHDU(vis_hdu)
    vis_hdu.header = vis_hdr

    ant_hdu = hdu_list[hdunames['AIPS AN']]

    write_file = os.path.join(DATA_PATH, 'test/outtest_casa.uvfits')
    hdulist = fits.HDUList(hdus=[vis_hdu, ant_hdu])
    if float(astropy.__version__[0:3]) < 1.3:
        hdulist.writeto(write_file, clobber=True)
    else:
        hdulist.writeto(write_file, overwrite=True)

    pols_to_keep = [-1, -2]
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [write_file],
                         {'polarizations': pols_to_keep},
                         message='Telescope EVLA is not')
    uvtest.checkWarnings(uvfits_uv2.read_uvfits, [write_file],
                         message='Telescope EVLA is not')
    uvfits_uv2.select(polarizations=pols_to_keep)
    nt.assert_equal(uvfits_uv, uvfits_uv2)


def test_ReadUVFitsWriteMiriad():
    """
    read uvfits, write miriad test.
    Read in uvfits file, write out as miriad, read back in and check for
    object equality.
    """
    uvfits_uv = UVData()
    miriad_uv = UVData()
    uvfits_file = os.path.join(DATA_PATH, 'day2_TDEM0003_10s_norx_1src_1spw.uvfits')
    testfile = os.path.join(DATA_PATH, 'test/outtest_miriad')
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [uvfits_file], message='Telescope EVLA is not')
    uvfits_uv.write_miriad(testfile, clobber=True)
    uvtest.checkWarnings(miriad_uv.read_miriad, [testfile], message='Telescope EVLA is not')

    nt.assert_equal(miriad_uv, uvfits_uv)

    # check that setting the phase_type keyword also works
    uvtest.checkWarnings(miriad_uv.read_miriad, [testfile], {'phase_type': 'phased'},
                         message='Telescope EVLA is not')

    # check that setting the phase_type to drift raises an error
    nt.assert_raises(ValueError, miriad_uv.read_miriad, testfile, phase_type='drift'),

    # check that setting it works after selecting a single time
    uvfits_uv.select(times=uvfits_uv.time_array[0])
    uvfits_uv.write_miriad(testfile, clobber=True)
    uvtest.checkWarnings(miriad_uv.read_miriad, [testfile],
                         message='Telescope EVLA is not')

    nt.assert_equal(miriad_uv, uvfits_uv)

    del(uvfits_uv)
    del(miriad_uv)


def test_multi_files():
    """
    Reading multiple files at once.
    """
    uv_full = UVData()
    uvfits_file = os.path.join(DATA_PATH, 'day2_TDEM0003_10s_norx_1src_1spw.uvfits')
    testfile1 = os.path.join(DATA_PATH, 'test/uv1.uvfits')
    testfile2 = os.path.join(DATA_PATH, 'test/uv2.uvfits')
    uvtest.checkWarnings(uv_full.read_uvfits, [uvfits_file], message='Telescope EVLA is not')
    uv1 = copy.deepcopy(uv_full)
    uv2 = copy.deepcopy(uv_full)
    uv1.select(freq_chans=np.arange(0, 32))
    uv2.select(freq_chans=np.arange(32, 64))
    uv1.write_uvfits(testfile1)
    uv2.write_uvfits(testfile2)
    uvtest.checkWarnings(uv1.read_uvfits, [[testfile1, testfile2]], nwarnings=2,
                         message=['Telescope EVLA is not'])
    # Check history is correct, before replacing and doing a full object check
    nt.assert_true(uvutils.check_histories(uv_full.history + '  Downselected to '
                                           'specific frequencies using pyuvdata. '
                                           'Combined data along frequency axis '
                                           'using pyuvdata.', uv1.history))

    uv1.history = uv_full.history
    nt.assert_equal(uv1, uv_full)

    # check raises error if read_data is False
    nt.assert_raises(ValueError, uv1.read_uvfits, [testfile1, testfile2],
                     read_data=False)

    # check raises error for read_uvfits_metadata
    nt.assert_raises(ValueError, uv1.read_uvfits_metadata, [testfile1, testfile2])

    # check raises error for read_uvfits_data
    nt.assert_raises(ValueError, uv1.read_uvfits_data, [testfile1, testfile2])


def test_readMSWriteUVFits_CASAHistory():
    """
    read in .ms file.
    Write to a uvfits file, read back in and check for casa_history parameter
    """
    ms_uv = UVData()
    uvfits_uv = UVData()
    ms_file = os.path.join(DATA_PATH, 'day2_TDEM0003_10s_norx_1src_1spw.ms')
    testfile = os.path.join(DATA_PATH, 'test/outtest_uvfits')
    ms_uv.read_ms(ms_file)
    ms_uv.write_uvfits(testfile, spoof_nonessential=True)
    uvtest.checkWarnings(uvfits_uv.read_uvfits, [testfile],
                         message='Telescope EVLA is not')
    nt.assert_equal(ms_uv, uvfits_uv)
    del(uvfits_uv)
    del(ms_uv)
