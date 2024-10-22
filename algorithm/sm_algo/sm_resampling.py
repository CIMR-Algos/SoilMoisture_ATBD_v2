
import numpy as np
import pyresample as pr
import copy


def resample(l1b, bands, area_defs, what, method, params=None, verbose=False):

    # check valid methods
    valid_methods = ('nn',  'gauss')
    if method not in valid_methods:
        raise ValueError('method must be one of {}'.format(valid_methods))

    # empty dictionary for l1x output
    l1x_dict = {}

    # Run resampling for each band
    for i, band in enumerate(bands):

        # grid area definition
        area_def = area_defs[i]

        # extract the swath area definition for the chosen band
        lat_sat = l1b[band].lat.data
        lon_sat = l1b[band].lon.data
        swath_def = pr.geometry.SwathDefinition(lons=lon_sat.flatten(),
                                                lats=lat_sat.flatten())

        # Prepare a stack of what in the l1b is to be regridded
        _l1b_stack = np.empty((swath_def.size, len(what)))
        for iw, w in enumerate(what):
            _l1b_stack[:,iw] = l1b[band][w].data.flatten()

        if method == 'nn':
            if params is None:
                roi = {'L':40, 'C':15, 'X':15, 'KU':7, 'KA':7}[band] * 1000
            else:
                roi = params['roi']
            _l1x_stack = pr.kd_tree.resample_nearest(swath_def, _l1b_stack,
                        area_def, radius_of_influence=roi, fill_value=np.nan)
        elif method == 'gauss':
            if params is None:
                roi = {'L':40, 'C':15, 'X':15, 'KU':7, 'KA':7}[band] * 1000
                sigma = {'L':10, 'C':5, 'X':5, 'KU':3.5, 'KA':3.5}[band] * 1000
            else:
                roi = params['roi']
                sigma = params['sigma']
                neighbours = params['neighbours']
            _l1x_stack = pr.kd_tree.resample_gauss(swath_def, _l1b_stack,
                        area_def, radius_of_influence=roi,
                        sigmas=[sigma]*len(what))

        # Transform back from the stack to an output dictionary
        _l1x_dict = {}
        _l1x_dict['_band'] = '{}-band'.format(band)
        _l1x_dict['_type'] = 'l1x grid'
        _l1x_dict['_grid'] = area_def.name
        _l1x_dict['lat'] = area_def.get_lonlats()[1]
        _l1x_dict['lon'] = area_def.get_lonlats()[0]
        for iw, w in enumerate(what,):
            _l1x_dict[w] = _l1x_stack[:, :, iw].reshape(area_def.shape)

        # fill l1x_dict for given band
        l1x_dict[band] = _l1x_dict

        if verbose:
            print('regridding complete')
            print('band   = {}-band'.format(band))
            print('grid   = ' + area_def.name)
            print('method = ' + method)
            print('radius = {} km'.format(int(roi / 1000)))
            if method == 'gauss':
                print('sigma  = {} km'.format(int(sigma / 1000)))

    return l1x_dict


def compute_aux_lookup(lookup, lu):
    array = np.zeros(lu.shape) * np.nan
    for i in range(0, 5):
        array[lu == i] = lookup[i]
    return array


def testcard_compute_lu_wf(lu_array, window_size):
    # computes dominant land use and water fraction of pixels
    from scipy.stats import mode
    steps_x = lu_array.shape[0] // window_size
    steps_y = lu_array.shape[1] // window_size
    norm = float(window_size**2)
    lu = np.zeros([steps_x, steps_y]) * np.nan
    wf = np.zeros([steps_x, steps_y]) * np.nan
    for i in range(steps_x):
        for j in range(steps_y):
            lu_window = lu_array[i*window_size : (i+1)*window_size,
                                 j*window_size : (j+1)*window_size].flatten()
            lu[i,j] = mode(lu_window, keepdims=False)[0]
            wf[i,j] = (np.sum(lu_window == 5) + np.sum(lu_window == 6)) / norm
            if wf[i,j] >= 0.5:
                lu[i,j] = 5
    return lu, wf


def sharpen(l1x, band_lr, band_hr, what, aoi_lr, verbose=True):

    """
    Simple sharpening algorithm, similar to the smoothing filter-based 
    intensity modulation (SFIM) [1, 2].
    
    [1] Liu, 2000, IJRS, Vol. 21, Issue 18
    [2] Santi, 2010, IJRS, Vol. 31, Issue 9
    """

    # extract dimensions
    dim1_lr = l1x[band_lr]['lat'].shape[0]
    dim2_lr = l1x[band_lr]['lat'].shape[1]
    dim1_hr = l1x[band_hr]['lat'].shape[0]
    dim2_hr = l1x[band_hr]['lat'].shape[1]

    # check dimension factor
    factor_rows = dim1_hr / dim1_lr
    factor_cols = dim2_hr / dim2_lr
    if factor_rows != factor_cols:
        raise Exception('Column and row factors do not match')
    else:
        factor = int(factor_rows)
        if verbose:
            print('')
            print('Sharpening')
            print('band low resolution  = {}-band'.format(band_lr))
            print('band high resolution = {}-band'.format(band_hr))
            print('downscaling factor   = {}'.format(factor))

    # initialize l1x_enhanced datastructure
    band_e = '{}_E'.format(band_lr)
    l1x_e = dict()
    l1x_e[band_e] = copy.deepcopy(l1x[band_hr])
    l1x_e[band_e]['_band'] = '{}-Band Enhanced'.format(band_lr)
    for w in what:
        l1x_e[band_e][w][:,:] = np.nan

    # loop over each lr pixel in AOI
    for i in range(aoi_lr[0], aoi_lr[1]):
        for j in range(aoi_lr[2], aoi_lr[3]):
            # define window
            row = slice(0 + i*factor, np.min([factor + i*factor, dim1_hr]))
            col = slice(0 + j*factor, np.min([factor + j*factor, dim2_hr]))
            # apply SFIM
            for w in what:
                lr_mean = l1x[band_lr][w][i, j]
                hr_data = l1x[band_hr][w][row, col]
                hr_mean = np.nanmean(hr_data)
                l1x_e[band_e][w][row, col] = hr_data * (lr_mean / hr_mean)

    return l1x_e
