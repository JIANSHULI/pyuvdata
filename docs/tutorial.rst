Tutorial
========

------
UVData
------

UVData: File conversion
-----------------------
Converting between tested data formats

a) miriad (aipy) -> uvfits
**************************
::

  >>> from pyuvdata import UVData
  >>> UV = UVData()

  # This miriad file is known to be a drift scan
  >>> miriad_file = 'pyuvdata/data/new.uvA'
  >>> UV.read_miriad(miriad_file)

  # Write out the uvfits file
  >>> UV.write_uvfits('tutorial.uvfits', force_phase=True, spoof_nonessential=True)
  The data are in drift mode and do not have a defined phase center. Phasing to zenith of the first timestamp.

b) uvfits -> miriad (aipy)
**************************
::

  >>> from pyuvdata import UVData
  >>> import shutil, os
  >>> UV = UVData()
  >>> uvfits_file = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(uvfits_file)

  # Write out the miriad file
  >>> write_file = 'tutorial.uv'
  >>> if os.path.exists(write_file):
  ...    shutil.rmtree(write_file)
  >>> UV.write_miriad(write_file)

c) FHD -> uvfits
****************
When reading FHD format, we need to point to several files.
::

  >>> from pyuvdata import UVData
  >>> UV = UVData()

  # Construct the list of files
  >>> fhd_prefix = 'pyuvdata/data/fhd_vis_data/1061316296_'
  >>> fhd_files = [fhd_prefix + f for f in ['flags.sav', 'vis_XX.sav', 'params.sav',
  ...                                       'vis_YY.sav', 'vis_model_XX.sav',
  ...                                       'vis_model_YY.sav', 'settings.txt']]
  >>> UV.read_fhd(fhd_files)
  >>> UV.write_uvfits('tutorial.uvfits', spoof_nonessential=True)

d) FHD -> miriad (aipy)
************************
::

  >>> from pyuvdata import UVData
  >>> import shutil, os
  >>> UV = UVData()
  >>> fhd_prefix = 'pyuvdata/data/fhd_vis_data/1061316296_'

  # Construct the list of files
  >>> fhd_prefix = 'pyuvdata/data/fhd_vis_data/1061316296_'
  >>> fhd_files = [fhd_prefix + f for f in ['flags.sav', 'vis_XX.sav', 'params.sav',
  ...                                       'vis_YY.sav', 'vis_model_XX.sav',
  ...                                       'vis_model_YY.sav', 'settings.txt']]
  >>> UV.read_fhd(fhd_files)
  >>> write_file = 'tutorial.uv'
  >>> if os.path.exists(write_file):
  ...    shutil.rmtree(write_file)
  >>> UV.write_miriad(write_file)

e) CASA -> uvfits
******************
::

  >>> from pyuvdata import UVData
  >>> UV=UVData()
  >>> ms_file = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms'
  >>> UV.read_ms(ms_file)
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/SPECTRAL_WINDOW: 14 columns, 1 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms: 23 columns, 1360 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/POLARIZATION: 4 columns, 1 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/ANTENNA: 8 columns, 28 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/OBSERVATION: 9 columns, 1 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/FIELD: 9 columns, 1 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/HISTORY: 9 columns, 6 rows

  # Write out uvfits file
  >>> UV.write_uvfits('tutorial.uvfits', spoof_nonessential=True)

f) CASA -> miriad (aipy)
**************************
::

  >>> from pyuvdata import UVData
  >>> import shutil, os
  >>> UV=UVData()
  >>> ms_file = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms'
  >>> UV.read_ms(ms_file)
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/SPECTRAL_WINDOW: 14 columns, 1 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms: 23 columns, 1360 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/POLARIZATION: 4 columns, 1 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/ANTENNA: 8 columns, 28 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/OBSERVATION: 9 columns, 1 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/FIELD: 9 columns, 1 rows
  Successful readonly open of default-locked table pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.ms/HISTORY: 9 columns, 6 rows

  # Write out Miriad file
  >>> write_file = 'tutorial.uv'
  >>> if os.path.exists(write_file):
  ...    shutil.rmtree(write_file)
  >>> UV.write_miriad(write_file)

UVData: Quick data access
--------------------------
A small suite of functions are available to quickly access numpy arrays of data,
flags, and nsamples.

a) Data for single antenna pair / polarization combination.
************************************************************
::

  >>> from pyuvdata import UVData
  >>> import numpy as np
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)
  >>> data = UV.get_data(1, 2, 'rr')  # data for ant1=1, ant2=2, pol='rr'
  >>> times = UV.get_times(1, 2)  # times corresponding to 0th axis in data
  >>> print(data.shape)
  (9, 64)
  >>> print(times.shape)
  (9,)

  # One can equivalently make any of these calls with the input wrapped in a tuple.
  >>> data = UV.get_data((1, 2, 'rr'))
  >>> times = UV.get_times((1, 2))

b) Flags and nsamples for above data.
*********************************************
::

  >>> flags = UV.get_flags(1, 2, 'rr')
  >>> nsamples = UV.get_nsamples(1, 2, 'rr')
  >>> print(flags.shape)
  (9, 64)
  >>> print(nsamples.shape)
  (9, 64)

c) Data for single antenna pair, all polarizations.
************************************************************
::

  >>> data = UV.get_data(1, 2)
  >>> print(data.shape)
  (9, 64, 4)

  # Can also give baseline number
  >>> data2 = UV.get_data(UV.antnums_to_baseline(1, 2))
  >>> print(np.all(data == data2))
  True

d) Data for single polarization, all baselines.
************************************************************
::

  >>> data = UV.get_data('rr')
  >>> print(data.shape)
  (1360, 64)

e) Iterate over all antenna pair / polarizations.
************************************************************
::

  >>> for key, data in UV.antpairpol_iter():
  ...  flags = UV.get_flags(key)
  ...  nsamples = UV.get_nsamples(key)

    # Do something with the data, flags, nsamples

f) Convenience functions to ask what antennas, baselines, and pols are in the data.
******************************************************************************************
::

  # Get all unique antennas in data
  >>> print(UV.get_ants())
  [ 0  1  2  3  6  7  8 11 14 18 19 20 21 22 23 24 26 27]

  # Get all baseline nums in data, print first 10.
  >>> print(UV.get_baseline_nums()[0:10])
  [67586 67587 67588 67591 67592 67593 67596 67599 67603 67604]

  # Get all (ordered) antenna pairs in data (same info as baseline_nums), print first 10.
  >>> print(UV.get_antpairs()[0:10])
  [(0, 1), (0, 2), (0, 3), (0, 6), (0, 7), (0, 8), (0, 11), (0, 14), (0, 18), (0, 19)]

  # Get all antenna pairs and polariations, i.e. keys produced in UV.antpairpol_iter(), print first 5.
  >>> print(UV.get_antpairpols()[0:5])
  [(0, 1, 'RR'), (0, 1, 'LL'), (0, 1, 'RL'), (0, 1, 'LR'), (0, 2, 'RR')]

g) Quick access to file attributes of a UV* object (UVData, UVCal, UVFITS, etc)
******************************************************************************************
::

  ## in bash ##
  pyuvdata_inspect.py --attr=data_array.shape <uv*_file> # will print data_array.shape to stdout

  pyuvdata_inspect.py --attr=Ntimes,Nfreqs,Nbls <uv*_file> # will print Ntimes,Nfreqs,Nbls to stdout

  pyuvdata_inspect.py -i <uv*_file> # will load object to instance name "uv" and will remain in interpreter

UVData: Phasing
-----------------------
Phasing/unphasing data
::

  >>> from pyuvdata import UVData
  >>> import ephem
  >>> UV = UVData()
  >>> miriad_file = 'pyuvdata/data/new.uvA'
  >>> UV.read_miriad(miriad_file)
  >>> print(UV.phase_type)
  drift

  # Phase the data to the zenith at first time step
  >>> UV.phase_to_time(UV.time_array[0])
  >>> print(UV.phase_type)
  phased

  # Undo phasing to try another phase center
  >>> UV.unphase_to_drift()

  # Phase to a specific ra/dec/epoch (in radians)
  >>> UV.phase(5.23368, 0.710940, ephem.J2000)

UVData: Plotting
------------------
Making a simple waterfall plot.

Note: there is now support for reading in only part of a uvfits or miriad file
(see :ref:`UVData: Working with large files`), so you need not read in the
entire file to plot one waterfall.
::

  >>> from pyuvdata import UVData
  >>> import numpy as np
  >>> import matplotlib.pyplot as plt
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)
  >>> print(UV.data_array.shape)
  (1360, 1, 64, 4)
  >>> print(UV.Ntimes)
  15
  >>> print(UV.Nfreqs)
  64
  >>> bl = UV.antnums_to_baseline(1, 2)
  >>> print(bl)
  69635
  >>> bl_ind = np.where(UV.baseline_array == bl)[0]

  # Amplitude waterfall for 0th spectral window and 0th polarization
  >>> plt.imshow(np.abs(UV.data_array[bl_ind, 0, :, 0])) # doctest: +SKIP
  >>> plt.show() # doctest: +SKIP

  # Update: With new UI features, making waterfalls is easier than ever!
  >>> plt.imshow(np.abs(UV.get_data((1, 2, UV.polarization_array[0])))) # doctest: +SKIP
  >>> plt.show() # doctest: +SKIP


UVData: Location conversions
--------------------------------
A number of conversion methods exist to map between different coordinate systems
for locations on the earth.

a) Getting antenna positions in topocentric frame in units of meters
***************************************************************************
::

  # directly from UVData object
  >>> uvd = UVData()
  >>> uvd.read_miriad('pyuvdata/data/new.uvA')
  >>> antpos, ants = uvd.get_ENU_antpos()

  # using uvutils
  >>> from pyuvdata import uvutils, UVData
  >>> uvd = UVData()
  >>> uvd.read_miriad('pyuvdata/data/new.uvA')
  >>> antpos = uvd.antenna_positions + uvd.telescope_location # get antennas positions in ECEF
  >>> antpos = uvutils.ENU_from_ECEF(antpos.T, *uvd.telescope_location_lat_lon_alt).T # convert to topo (ENU) coords.


UVData: Selecting data
-----------------------
The select method lets you select specific antennas (by number or name),
antenna pairs, frequencies (in Hz or by channel number), times or polarizations
to keep in the object while removing others.

Note: The same select interface is now supported on the read for uvfits files
(see :ref:`UVData: Working with large files`), so you need not read in the
entire file before doing the select.

a) Select 3 antennas to keep using the antenna number.
********************************************************
::

  >>> from pyuvdata import UVData
  >>> import numpy as np
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)

  # print all the antennas numbers with data in the original file
  >>> print(np.unique(UV.ant_1_array.tolist() + UV.ant_2_array.tolist()))
  [ 0  1  2  3  6  7  8 11 14 18 19 20 21 22 23 24 26 27]
  >>> UV.select(antenna_nums=[0, 11, 20])

  # print all the antennas numbers with data after the select
  >>> print(np.unique(UV.ant_1_array.tolist() + UV.ant_2_array.tolist()))
  [ 0 11 20]

b) Select 3 antennas to keep using the antenna names, also select 5 frequencies to keep.
*****************************************************************************************
::

  >>> from pyuvdata import UVData
  >>> import numpy as np
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)

  # print all the antenna names with data in the original file
  >>> unique_ants = np.unique(UV.ant_1_array.tolist() + UV.ant_2_array.tolist())
  >>> print([UV.antenna_names[np.where(UV.antenna_numbers==a)[0][0]] for a in unique_ants])
  ['W09', 'E02', 'E09', 'W01', 'N06', 'N01', 'E06', 'E08', 'W06', 'W04', 'N05', 'E01', 'N04', 'E07', 'W05', 'N02', 'E03', 'N08']

  # print how many frequencies in the original file
  >>> print(UV.freq_array.size)
  64
  >>> UV.select(antenna_names=['N02', 'E09', 'W06'], frequencies=UV.freq_array[0,0:4])

  # print all the antenna names with data after the select
  >>> unique_ants = np.unique(UV.ant_1_array.tolist() + UV.ant_2_array.tolist())
  >>> print([UV.antenna_names[np.where(UV.antenna_numbers==a)[0][0]] for a in unique_ants])
  ['E09', 'W06', 'N02']

  # print all the frequencies after the select
  >>> print(UV.freq_array)
  [[3.6304542e+10 3.6304667e+10 3.6304792e+10 3.6304917e+10]]

c) Select a few antenna pairs to keep
******************************************
::

  >>> from pyuvdata import UVData
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)

  # print how many antenna pairs with data in the original file
  >>> print(len(set(zip(UV.ant_1_array, UV.ant_2_array))))
  153
  >>> UV.select(ant_pairs_nums=[(0, 2), (6, 0), (0, 21)])

  # note that order of the values in the pair does not matter
  # print all the antenna pairs after the select
  >>> print(set(zip(UV.ant_1_array, UV.ant_2_array)))
  set([(0, 6), (0, 21), (0, 2)])

d) Select antenna pairs and polarizations using ant_str argument
********************************************************************

Basic options are 'auto', 'cross', or 'all'. 'auto' returns just the
autocorrelations (all pols), while 'cross' returns just the cross-correlations
(all pols).  The ant_str can also contain:

1. Individual antenna number(s):
________________________________

- 1: returns all antenna pairs containing antenna number 1 (including the auto correlation)
- 1,2: returns all antenna pairs containing antennas 1 and/or 2

::

  >>> from pyuvdata import UVData
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)

  # Print the number of antenna pairs in the original file
  >>> print(len(UV.get_antpairs()))
  153

  # Apply select to UV object
  >>> UV.select(ant_str='1,2,3')

  # Print the number of antenna pairs after the select
  >>> print(len(UV.get_antpairs()))
  48

2. Individual baseline(s):
___________________________

- 1_2: returns only the antenna pair (1,2)
- 1_2,1_3,1_10: returns antenna pairs (1,2),(1,3),(1,10)
- (1,2)_3: returns antenna pairs (1,3),(2,3)
- 1_(2,3): returns antenna pairs (1,2),(1,3)

::

  >>> from pyuvdata import UVData
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)

  # Print the number of antenna pairs in the original file
  >>> print(len(UV.get_antpairs()))
  153

  # Apply select to UV object
  >>> UV.select(ant_str='(1,2)_(3,6)')

  # Print the antennas pairs with data after the select
  >>> print(UV.get_antpairs())
  [(1, 3), (1, 6), (2, 3), (2, 6)]

3. Antenna number(s) and polarization(s):
__________________________________________

When polarization information is passed with antenna numbers,
all antenna pairs kept in the object will retain data for each specified polarization

- 1x: returns all antenna pairs containing antenna number 1 and polarizations xx and xy
- 2x_3y: returns the antenna pair (2,3) and polarization xy
- 1r_2l,1l_3l,1r_4r: returns antenna pairs (1,2), (1,3), (1,4) and polarizations rr, ll, and rl.  This yields a complete list of baselines with polarizations of 1r_2l, 1l_2l, 1r_2r, 1r_3l, 1l_3l, 1r_3r, 1r_11l, 1l_11l, and 1r_11r.
- (1x,2y)_(3x,4y): returns antenna pairs (1,3),(1,4),(2,3),(2,4) and polarizations xx, yy, xy, and yx
- 2l_3: returns antenna pair (2,3) and polarizations ll and lr
- 2r_3: returns antenna pair (2,3) and polarizations rr and rl
- 1l_3,2x_3: returns antenna pairs (1,3), (2,3) and polarizations ll, lr, xx, and xy
- 1_3l,2_3x: returns antenna pairs (1,3), (2,3) and polarizations ll, rl, xx, and yx

::

  >>> from pyuvdata import UVData
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)

  # Print the number of antennas and polarizations with data in the original file
  >>> print(len(UV.get_antpairs()), UV.get_pols())
  (153, ['RR', 'LL', 'RL', 'LR'])

  # Apply select to UV object
  >>> UV.select(ant_str='1r_2l,1l_3l,1r_6r')

  # Print all the antennas numbers and polarizations with data after the select
  >>> print(UV.get_antpairs(), UV.get_pols())
  ([(1, 2), (1, 3), (1, 6)], ['RR', 'LL', 'RL'])

4. Stokes parameter(s):
________________________

Can be passed lowercase or uppercase

- i,I: keeps only Stokes I
- q,V: keeps both Stokes Q and V

5. Minus sign(s):
________________________

If a minus sign is present in front of an antenna number, it will not be kept in the data

- 1,-3: returns all antenna pairs containing antenna 1, but removes any containing antenna 3
- 1,-1_3: returns all antenna pairs containing antenna 1, except the antenna pair (1,3)
- 1x_(-3y,10x): returns antenna pair (1,10) and polarization xx

::

  >>> from pyuvdata import UVData
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)

  # Print the number of antenna pairs in the original file
  >>> print(len(UV.get_antpairs()))
  153

  # Apply select to UV object
  >>> UV.select(ant_str='1,-1_3')

  # Print the number of antenna pairs with data after the select
  >>> print(len(UV.get_antpairs()))
  16

e) Select data and return new object (leaving original intact).
********************************************************************
::

  >>> from pyuvdata import UVData
  >>> import numpy as np
  >>> UV = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> UV.read_uvfits(filename)
  >>> UV2 = UV.select(antenna_nums=[0, 11, 20], inplace=False)

  # print all the antennas numbers with data in the original file
  >>> print(np.unique(UV.ant_1_array.tolist() + UV.ant_2_array.tolist()))
  [ 0  1  2  3  6  7  8 11 14 18 19 20 21 22 23 24 26 27]

  # print all the antennas numbers with data after the select
  >>> print(np.unique(UV2.ant_1_array.tolist() + UV2.ant_2_array.tolist()))
  [ 0 11 20]

UVData: Adding data
-----------------------
The __add__ method lets you combine UVData objects along
the baseline-time, frequency, and/or polarization axis.

a) Add frequencies.
*********************
::

  >>> from pyuvdata import UVData
  >>> import numpy as np
  >>> import copy
  >>> uv1 = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> uv1.read_uvfits(filename)
  >>> uv2 = copy.deepcopy(uv1)

  # Downselect frequencies to recombine
  >>> uv1.select(freq_chans=np.arange(0, 32))
  >>> uv2.select(freq_chans=np.arange(32, 64))
  >>> uv3 = uv1 + uv2
  >>> print(uv1.Nfreqs, uv2.Nfreqs, uv3.Nfreqs)
  (32, 32, 64)

b) Add times.
****************
::

  >>> from pyuvdata import UVData
  >>> import numpy as np
  >>> import copy
  >>> uv1 = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> uv1.read_uvfits(filename)
  >>> uv2 = copy.deepcopy(uv1)

  # Downselect times to recombine
  >>> times = np.unique(uv1.time_array)
  >>> uv1.select(times=times[0:len(times) / 2])
  >>> uv2.select(times=times[len(times) / 2:])
  >>> uv3 = uv1 + uv2
  >>> print(uv1.Ntimes, uv2.Ntimes, uv3.Ntimes)
  (7, 8, 15)
  >>> print(uv1.Nblts, uv2.Nblts, uv3.Nblts)
  (459, 901, 1360)

c) Adding in place.
*******************
The following two commands are equivalent, and act on uv1
directly without creating a third uvdata object.
::

  >>> from pyuvdata import UVData
  >>> import numpy as np
  >>> import copy
  >>> uv1 = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> uv1.read_uvfits(filename)
  >>> uv2 = copy.deepcopy(uv1)
  >>> uv1.select(times=times[0:len(times) / 2])
  >>> uv2.select(times=times[len(times) / 2:])
  >>> uv1.__add__(uv2, inplace=True)

  >>> uv1.read_uvfits(filename)
  >>> uv2 = copy.deepcopy(uv1)
  >>> uv1.select(times=times[0:len(times) / 2])
  >>> uv2.select(times=times[len(times) / 2:])
  >>> uv1 += uv2

d) Reading multiple files.
****************************
If any of the read methods are given a list of files
(or list of lists in the case of read_fhd), each file will be read in succession
and added to the previous.
::

  >>> from pyuvdata import UVData
  >>> uv = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> uv.read_uvfits(filename)
  >>> uv1 = uv.select(freq_chans=np.arange(0, 20), inplace=False)
  >>> uv2 = uv.select(freq_chans=np.arange(20, 40), inplace=False)
  >>> uv3 = uv.select(freq_chans=np.arange(40, 64), inplace=False)
  >>> uv1.write_uvfits('tutorial1.uvfits')
  >>> uv2.write_uvfits('tutorial2.uvfits')
  >>> uv3.write_uvfits('tutorial3.uvfits')
  >>> filenames = ['tutorial1.uvfits', 'tutorial2.uvfits', 'tutorial3.uvfits']
  >>> uv.read_uvfits(filenames)

UVData: Working with large files
----------------------------------------------
To save on memory and time, pyuvdata supports reading only parts of uvfits and
miriad files.

a) Reading just the header of a uvfits file
****************************
When only the header info is read in, the UVData object is not fully specified,
so only some of the expected attributes are filled out
::

  >>> from pyuvdata import UVData
  >>> uv = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> uv.read_uvfits(filename, read_data=False, read_metadata=False)
  >>> print(uv.Nblts, uv.Nfreqs, uv.Npols)
  (1360, 64, 4)

  >>> print(uv.freq_array.size)
  64

  >>> print(uv.time_array)
  None

  >>> print(uv.data_array)
  None

b) Reading the header and metadata of a uvfits file
******************************************
The UVData object is still not fully specified, but every attribute except
the data_array, flag_array and nsample_array are filled out. Either read in the
metadata at the same time as the header (use read_metadata=True which is the default),
or read in the header followed by the metadata (both shown below)
::

  >>> from pyuvdata import UVData
  >>> uv = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'

  >>> uv.read_uvfits(filename, read_data=False)

  >>> uv.read_uvfits(filename, read_data=False, read_metadata=False)
  >>> uv.read_uvfits_metadata(filename)

  >>> print(uv.time_array.size)
  1360

  >>> print(uv.data_array)
  None

  # If the data_array, flag_array or nsample_array are needed later, they can be
  # read into the existing object:
  >>> uv.read_uvfits_data(filename)
  >>> print(uv.data_array.shape)
  (1360, 1, 64, 4)

c) Reading only parts of uvfits data
***************************************
The same options that are available for the select function can also be passed to
read_uvfits or read_uvfits_data to do the select on the read, saving memory and
time if only a portion of the data are needed.
::

  >>> import numpy as np
  >>> from pyuvdata import UVData
  >>> uv = UVData()
  >>> filename = 'pyuvdata/data/day2_TDEM0003_10s_norx_1src_1spw.uvfits'
  >>> uv.read_uvfits(filename, freq_chans=np.arange(32))
  >>> print(uv.data_array.shape)
  (1360, 1, 32, 4)

  # Reading in the header and metadata can help with specifying what data to read in
  >>> uv.read_uvfits(filename, read_data=False)
  >>> unique_times = np.unique(uv.time_array)
  >>> print(unique_times.shape)
  (15,)

  >>> times_to_keep = unique_times[[0, 2, 4]]
  >>> uv.read_uvfits_data(filename, times=times_to_keep)
  >>> print(uv.data_array.shape)
  (179, 1, 64, 4)

c) Reading only parts of miriad data
***************************************
Many of the same options that are available for the select function can also be
passed to read_miriad to do the select on the read, saving memory and
time if only a portion of the data are needed.
::
>>> from pyuvdata import UVData
>>> uv = UVData()
>>> filename = 'pyuvdata/data/zen.2457698.40355.xx.HH.uvcA'
>>> uv.read_miriad(filename, ant_pairs_nums=[(9, 10), (9, 20)])
>>> print(uv.get_antpairs())
[(9, 10), (9, 20)]

------
UVCal
------

UVCal: Reading/writing
-----------------------
Calibration files using UVCal.

a) Reading a gain calibration file.
*************************************
::

  >>> from pyuvdata import UVCal
  >>> import numpy as np
  >>> import matplotlib.pyplot as plt
  >>> cal = UVCal()
  >>> filename = 'pyuvdata/data/zen.2457698.40355.xx.fitsA'
  >>> cal.read_calfits(filename)

  # Cal type:
  >>> print(cal.cal_type)
  gain

  # number of antenna polarizations and polarization type.
  >>> print(cal.Njones, cal.jones_array)
  (1, array([-5]))

  # Number of antennas with data
  >>> print(cal.Nants_data)
  19

  # Number of frequencies
  >>> print(cal.Nfreqs)
  1024

  # Shape of the gain_array
  >>> print(cal.gain_array.shape)
  (19, 1, 1024, 56, 1)

  >>> for ant in range(cal.Nants_data): # doctest: +SKIP
  ...    plt.plot(cal.freq_array.flatten(), np.abs(cal.gain_array[ant, 0, :, 0, 0]))  # plot abs of all gains for first time and first jones polarization.
  >>> plt.xlabel('Frequency (Hz)') # doctest: +SKIP
  >>> plt.ylabel('Abs(gains)') # doctest: +SKIP
  >>> plt.show() # doctest: +SKIP


b) Writing a gain calibration file.
******************************************
::

  >>> from pyuvdata import UVCal
  >>> import os
  >>> import numpy as np
  >>> time_array = 2457698 + np.linspace(.2, .3, 16)  # time_array in JD
  >>> Ntimes = len(time_array)
  >>> freq_array = np.linspace(1e6, 2e6, 1024)  # frequency array in Hz
  >>> Nfreqs = len(freq_array)
  >>> jones_array = np.array([-5, -6])  #  only 2 jones parameters.
  >>> Njones = len(jones_array)
  >>> ant_array = np.arange(19)
  >>> Nants_data = len(ant_array)
  >>> antenna_names = np.array(['ant{0}.format(ant)' for ant in ant_array])
  >>> Nspws = 1  # only 1 spw is supported

  # Generate fake data
  >>> gains = (np.random.randn(Nants_data, Nspws, Nfreqs, Ntimes, Njones)
  ...         + 1j*np.random.randn(Nants_data, Nspws, Nfreqs, Ntimes, Njones))
  >>> flags = np.ones_like(gains, dtype=np.bool)
  >>> chisq = np.random.randn(Nants_data, Nspws, Nfreqs, Ntimes, Njones)

  >>> cal = UVCal()
  >>> cal.set_gain()
  >>> cal.set_redundant()
  >>> cal.Nfreqs = Nfreqs
  >>> cal.Njones = Njones
  >>> cal.Ntimes = Ntimes
  >>> cal.history = 'This is an example file generated from tutorial 5b of pycaldata.'
  >>> cal.Nspws = 1
  >>> cal.spw_array = [0]
  >>> cal.freq_array = freq_array.reshape(cal.Nspws, -1)
  >>> cal.freq_range = [freq_array[0], freq_array[-1]]  # valid frequencies for solutions.
  >>> cal.channel_width = np.diff(freq_array)[0]
  >>> cal.jones_array = jones_array
  >>> cal.time_array = time_array
  >>> cal.integration_time = np.diff(time_array)[0]
  >>> cal.gain_convention = 'divide'  # Use this operation to apply gain solution.
  >>> cal.x_orientation = 'east'  # orientation of 1st jones parameter.
  >>> cal.time_range = [time_array[0], time_array[-1]]
  >>> cal.telescope_name = 'Fake Telescope'
  >>> cal.Nants_data = Nants_data
  >>> cal.Nants_telescope = Nants_data  # have solutions for all antennas in array.
  >>> cal.ant_array = ant_array
  >>> cal.antenna_names = antenna_names
  >>> cal.antenna_numbers = ant_array
  >>> cal.flag_array = flags
  >>> cal.gain_array = gains
  >>> cal.quality_array = chisq

  >>> write_file = 'tutorial.fits'
  >>> if os.path.exists(write_file):
  ...    os.remove(write_file)
  >>> cal.write_calfits(write_file)

UVCal: Selecting data
-----------------------
The select method lets you select specific antennas (by number or name),
frequencies (in Hz or by channel number), times or polarizations
to keep in the object while removing others.

a) Select 3 antennas to keep using the antenna number.
********************************************************************
::

  >>> from pyuvdata import UVCal
  >>> import numpy as np
  >>> cal = UVCal()
  >>> filename = 'pyuvdata/data/zen.2457698.40355.xx.fitsA'
  >>> cal.read_calfits(filename)

  # print all the antennas numbers with data in the original file
  >>> print(cal.ant_array)
  [  9  10  20  22  31  43  53  64  65  72  80  81  88  89  96  97 104 105
   112]
  >>> cal.select(antenna_nums=[9, 22, 64])

  # print all the antennas numbers with data after the select
  >>> print(cal.ant_array)
  [ 9 22 64]

b) Select 3 antennas to keep using the antenna names, also select 5 frequencies to keep.
**********************************************************************************************
::

  >>> from pyuvdata import UVCal
  >>> import numpy as np
  >>> cal = UVCal()
  >>> filename = 'pyuvdata/data/zen.2457698.40355.xx.fitsA'
  >>> cal.read_calfits(filename)

  # print all the antenna names with data in the original file
  >>> print([cal.antenna_names[np.where(cal.antenna_numbers==a)[0][0]] for a in cal.ant_array[0:9]])
  ['ant9', 'ant10', 'ant20', 'ant22', 'ant31', 'ant43', 'ant53', 'ant64', 'ant65']

  # print all the frequencies in the original file
  >>> print(cal.freq_array)
  [[1.00000000e+08 1.00097656e+08 1.00195312e+08 ... 1.99707031e+08
    1.99804688e+08 1.99902344e+08]]
  >>> cal.select(antenna_names=['ant31', 'ant81', 'ant104'], freq_chans=np.arange(0, 4))

  # print all the antenna names with data after the select
  >>> print([cal.antenna_names[np.where(cal.antenna_numbers==a)[0][0]] for a in cal.ant_array])
  ['ant31', 'ant81', 'ant104']

  # print all the frequencies after the select
  >>> print(cal.freq_array)
  [[1.00000000e+08 1.00097656e+08 1.00195312e+08 1.00292969e+08]]

------
UVBeam
------


UVBeam: Reading/writing
-----------------------
Reading and writing beam files using UVBeam.

a) Reading a CST power beam file
******************************************
::

  >>> from pyuvdata import UVBeam
  >>> import numpy as np
  >>> import matplotlib.pyplot as plt
  >>> beam = UVBeam()

  # you can pass several filenames and the objects from each file will be
  # combined across the appropriate axis -- in this case frequency
  >>> filenames = ['pyuvdata/data/HERA_NicCST_150MHz.txt', 'pyuvdata/data/HERA_NicCST_123MHz.txt']

  # have to specify the telescope_name, feed_name, feed_version, model_name
  # and model_version because they are not included in the file
  # specify the polarization that the file represents and set rotate_pol to
  # generate the other polarization by rotating by 90 degrees.
  >>> beam.read_cst_beam(filenames, beam_type='power', frequency=[150e6, 123e6],
  ...                    feed_pol='x', rotate_pol=True, telescope_name='HERA',
  ...                    feed_name='PAPER_dipole', feed_version='0.1',
  ...                    model_name='E-field pattern - Rigging height 4.9m',
  ...                    model_version='1.0')
  >>> print(beam.beam_type)
  power
  >>> print(beam.pixel_coordinate_system)
  az_za
  >>> print(beam.data_normalization)
  physical

  # number of beam polarizations and polarization type.
  >>> print(beam.Npols, beam.polarization_array)
  (2, array([-5, -6]))
  >>> print(beam.Nfreqs)
  2
  >>> print(beam.data_array.shape)
  (1, 1, 2, 2, 181, 360)

  # plot zenith angle cut through beam
  >>> plt.plot(beam.axis2_array, beam.data_array[0, 0, 0, 0, :, 0]) # doctest: +SKIP
  >>> plt.xscale('log') # doctest: +SKIP
  >>> plt.xlabel('Zenith Angle (radians)') # doctest: +SKIP
  >>> plt.ylabel('Power') # doctest: +SKIP
  >>> plt.show() # doctest: +SKIP

b) Reading a CST E-field beam file
******************************************
::

  >>> from pyuvdata import UVBeam
  >>> import numpy as np
  >>> beam = UVBeam()

  # you can pass several filenames and the objects from each file will be
  # combined across the appropriate axis -- in this case frequency
  >>> filenames = ['pyuvdata/data/HERA_NicCST_150MHz.txt', 'pyuvdata/data/HERA_NicCST_123MHz.txt']

  # have to specify the telescope_name, feed_name, feed_version, model_name
  # and model_version because they are not included in the file
  >>> beam.read_cst_beam(filenames, beam_type='efield', telescope_name='HERA',
  ...                    feed_name='PAPER_dipole', feed_version='0.1',
  ...                    model_name='E-field pattern - Rigging height 4.9m',
  ...                    model_version='1.0')
  >>> print(beam.beam_type)
  efield

c) Writing a regularly gridded beam FITS file
**********************************************
::

  >>> from pyuvdata import UVBeam
  >>> import numpy as np
  >>> beam = UVBeam()
  >>> filenames = ['pyuvdata/data/HERA_NicCST_150MHz.txt', 'pyuvdata/data/HERA_NicCST_123MHz.txt']
  >>> beam.read_cst_beam(filenames, beam_type='power', telescope_name='HERA',
  ...                    feed_name='PAPER_dipole', feed_version='0.1',
  ...                    model_name='E-field pattern - Rigging height 4.9m',
  ...                    model_version='1.0')
  >>> beam.write_beamfits('tutorial.fits', clobber=True)

d) Writing a HEALPix beam FITS file
******************************************
::

  >>> from pyuvdata import UVBeam
  >>> import numpy as np
  >>> beam = UVBeam()
  >>> filenames = ['pyuvdata/data/HERA_NicCST_150MHz.txt', 'pyuvdata/data/HERA_NicCST_123MHz.txt']
  >>> beam.read_cst_beam(filenames, beam_type='power', telescope_name='HERA',
  ...                    feed_name='PAPER_dipole', feed_version='0.1',
  ...                    model_name='E-field pattern - Rigging height 4.9m',
  ...                    model_version='1.0')
  >>> beam.az_za_to_healpix()
  >>> beam.write_beamfits('tutorial.fits', clobber=True)

UVBeam: Selecting data
-----------------------
The select method lets you select specific image axis indices (or pixels if
pixel_coordinate_system is HEALPix), frequencies and feeds (or polarizations if
beam_type is power) to keep in the object while removing others.

a) Selecting a range of Zenith Angles
******************************************
::

  >>> from pyuvdata import UVBeam
  >>> import numpy as np
  >>> import matplotlib.pyplot as plt
  >>> beam = UVBeam()
  >>> filenames = ['pyuvdata/data/HERA_NicCST_150MHz.txt', 'pyuvdata/data/HERA_NicCST_123MHz.txt']
  >>> beam.read_cst_beam(filenames, beam_type='power', telescope_name='HERA',
  ...                    feed_name='PAPER_dipole', feed_version='0.1',
  ...                    model_name='E-field pattern - Rigging height 4.9m',
  ...                    model_version='1.0')
  >>> new_beam = beam.select(axis2_inds=np.arange(0, 20), inplace=False)

  # plot zenith angle cut through beams
  >>> plt.plot(beam.axis2_array, beam.data_array[0, 0, 0, 0, :, 0], # doctest: +SKIP
  ...         new_beam.axis2_array, new_beam.data_array[0, 0, 0, 0, :, 0], 'r')
  >>> plt.xscale('log') # doctest: +SKIP
  >>> plt.xlabel('Zenith Angle (radians)') # doctest: +SKIP
  >>> plt.ylabel('Power') # doctest: +SKIP
  >>> plt.show() # doctest: +SKIP

UVBeam: Converting to beam types and coordinate systems
---------------------------------------------------------------------

a) Convert a regularly gridded az_za power beam to HEALpix (leaving original intact).
********************************************************************
::

  >>> from pyuvdata import UVBeam
  >>> import numpy as np
  >>> import healpy as hp
  >>> beam = UVBeam()
  >>> filenames = ['pyuvdata/data/HERA_NicCST_150MHz.txt', 'pyuvdata/data/HERA_NicCST_123MHz.txt']
  >>> beam.read_cst_beam(filenames, beam_type='power', telescope_name='HERA',
  ...                    feed_name='PAPER_dipole', feed_version='0.1',
  ...                    model_name='E-field pattern - Rigging height 4.9m',
  ...                    model_version='1.0')
  >>> hpx_beam = beam.az_za_to_healpix(inplace=False)
  >>> hp.mollview(hpx_beam.data_array[0,0,0,0,:]) # doctest: +SKIP

b) Convert a regularly gridded az_za efield beam to HEALpix (leaving original intact).
********************************************************************
::

  >>> from pyuvdata import UVBeam
  >>> import numpy as np
  >>> import healpy as hp
  >>> beam = UVBeam()
  >>> filenames = ['pyuvdata/data/HERA_NicCST_150MHz.txt', 'pyuvdata/data/HERA_NicCST_123MHz.txt']
  >>> beam.read_cst_beam(filenames, beam_type='efield', telescope_name='HERA',
  ...                    feed_name='PAPER_dipole', feed_version='0.1',
  ...                    model_name='E-field pattern - Rigging height 4.9m',
  ...                    model_version='1.0')
  >>> hpx_beam = beam.az_za_to_healpix(inplace=False)
  >>> hp.mollview(np.abs(hpx_beam.data_array[0,0,0,0,:])) # doctest: +SKIP


c) Convert a regularly gridded efield beam to a power beam (leaving original intact).
********************************************************************
::

  >>> from pyuvdata import UVBeam
  >>> import copy
  >>> import numpy as np
  >>> import matplotlib.pyplot as plt
  >>> beam = UVBeam()
  >>> filenames = ['pyuvdata/data/HERA_NicCST_150MHz.txt', 'pyuvdata/data/HERA_NicCST_123MHz.txt']
  >>> beam.read_cst_beam(filenames, beam_type='efield', telescope_name='HERA',
  ...                    feed_name='PAPER_dipole', feed_version='0.1',
  ...                    model_name='E-field pattern - Rigging height 4.9m',
  ...                    model_version='1.0')
  >>> new_beam = beam.efield_to_power(inplace=False)

  # plot zenith angle cut through the beams
  >>> plt.plot(beam.axis2_array, beam.data_array[1, 0, 0, 0, :, 0].real, label='E-field real') # doctest: +SKIP
  >>> plt.plot(beam.axis2_array, beam.data_array[1, 0, 0, 0, :, 0].imag, 'r', label='E-field imaginary') # doctest: +SKIP
  >>> plt.plot(new_beam.axis2_array, np.sqrt(new_beam.data_array[0, 0, 0, 0, :, 0]), 'black', label='sqrt Power') # doctest: +SKIP
  >>> plt.xlabel('Zenith Angle (radians)') # doctest: +SKIP
  >>> plt.ylabel('Magnitude') # doctest: +SKIP
  >>> plt.legend() # doctest: +SKIP
  >>> plt.show() # doctest: +SKIP


-----------------
Tutorial Cleanup
-----------------
::

  # delete all written files
  >>> import shutil, os
  >>> filelist = ['tutorial' + f for f in ['.uvfits', '1.uvfits', '2.uvfits', '3.uvfits', '.fits']]
  >>> for f in filelist:
  ...     os.remove(f)
  >>> shutil.rmtree('tutorial.uv')
