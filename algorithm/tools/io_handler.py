
import os

from copy import copy, deepcopy

import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
plt.rcParams.update({'font.size': 22})

import xarray as xr
import numpy as np
from collections import OrderedDict

n_horns = {'L':1, 'C': 4, 'X': 4, 'KU': 8, 'KA':8}
valid_bands = n_horns.keys()


def parse_slice(string):
    """
    Parses a '[start:stop:step,start:stop:step,...]' string into a tuple of `slice()` for
      array indexing
    """
    slices = []
    for part in string.strip('[]').split(','):
        try:
            i = int(part)
            sl = slice(i,i+1,None)
        except ValueError:
            sl = slice(*(int(i) if i else None for i in part.strip().split(':')))
            
        slices.append(sl)
    
    return tuple(slices)

class CIMR_L1B(object):
    
    def __init__(self, l1b_fn, selected_bands=('L', 'C', 'X', 'KU', 'KA'),
                 keep_calibration_view=True,
                 hard_coded_scan_angle_feeds_offset=False,
                 hard_coded_scan_angle_corr4SCEPS=False):
        
        if not os.path.exists(l1b_fn):
            raise ValueError("File not found {}".format(l1b_fn))
        
        # prepare some attributes of the object
        self.file_path = l1b_fn
        self.bands = selected_bands
        self.scan = 'Full'
        self.data = dict()
        
        # open access to the dataset (by band)
        for band in self.bands:
            if band not in valid_bands:
                raise ValueError('band must be in {} (got {})'.format(valid_bands, band))
            
            bandn = band + '_BAND'
            self.data[band] = xr.open_dataset(self.file_path, group=bandn)
            # move the scan_angle_feeds_offset(n_horns,) variable as it confuses xarray
            self.move_scan_angle_feeds_offset(band=band, hard_coded=hard_coded_scan_angle_feeds_offset)
            # enforce longitudes are [-180;+180]
            for v in ('lon', 'sub_satellite_lon'):
                try:
                    self.data[band][v] = ( self.data[band][v] + 180 ) % 360 - 180
                except KeyError:
                    pass
            # remove the calibration (and house keeping) part of the scanlines
            if not keep_calibration_view:
                sflag = self.data[band].instrument_status
                self.data[band] = self.data[band].where((sflag==0)+(sflag==1), drop=True)
            # FIX for SCEPS file :
            if hard_coded_scan_angle_corr4SCEPS:
                print("Change 'scan_angle' for band {}".format(band))
                self.data[band]['scan_angle'].data[self.data[band]['scan_angle'].data<0] += 360
        
        # perform some pre-processing
        self.add_orig_scans_samples_horns()
        self.add_horn_scan_angle()

    @classmethod
    def from_TestCard(cls, l1b_fn, selected_bands=('L', 'C', 'X', 'KU', 'KA'),):
        """Return a L1B object from a TestCard"""

        if not os.path.exists(l1b_fn):
            raise ValueError("File not found {}".format(l1b_fn))
        
        # prepare some attributes of the object
        self.file_path = l1b_fn
        self.bands = selected_bands
        self.scan = 'NA'
        self.data = dict()
        
        # open access to the dataset (by band)
        for band in self.bands:
            if band not in valid_bands:
                raise ValueError('band must be in {} (got {})'.format(valid_bands, band))
            
            bandn = band + '_BAND'
            self.data[band] = xr.open_dataset(self.file_path, group=bandn)
            # move the scan_angle_feeds_offset(n_horns,) variable as it confuses xarray
            self.move_scan_angle_feeds_offset(band=band, hard_coded=True)
            # enforce longitudes are [-180;+180]
            for v in ('lon', 'sub_satellite_lon'):
                try:
                    self.data[band][v] = ( self.data[band][v] + 180 ) % 360 - 180
                except KeyError:
                    pass
            # remove the calibration (and house keeping) part of the scanlines
            if not keep_calibration_view:
                sflag = self.data[band].instrument_status
                self.data[band] = self.data[band].where((sflag==0)+(sflag==1), drop=True)
        
        # perform some pre-processing
        self.add_orig_scans_samples_horns()
        self.add_horn_scan_angle()


    
    def __str__(self, ):
        ret  = 'Upstream file: {}\n'.format(self.file_path)
        for band in self.bands:
            ret += '\t{} : {}\n'.format(band, self.data[band].dims)
        ret += '{} scans'.format(self.scan)
        return ret
    
    def add_orig_scans_samples_horns(self, ):
        """ Add three integer arrays (per band) to record the (original) scan(line), sample (scanpos),
               and horn (feed). This is useful to keep track of the origin of each sample when
               we re-arrange samples and change the dimensions of the arrays.
        """
        scan_n = 'orig_scan'
        samp_n = 'orig_sample'
        horn_n = 'orig_horn'
        for band in self.bands:
            shape = self.data[band].brightness_temperature_v.shape
            if len(shape) != 3:
                raise ValueError("Variable 'brightness_temperature_v' has {} dims in band {}. Was expecting 3 dims.".format(len(shape), band))
            # scan(line) counter
            scan_v = np.arange(0, shape[0], dtype='int16')[:,None,None].repeat(shape[1],axis=1).repeat(shape[2], axis=2)
            # samples (scanpos) counter
            samp_v = np.arange(0, shape[1], dtype='int16')[None,:,None].repeat(shape[0],axis=0).repeat(shape[2], axis=2)
            # horns (feed) counter
            horn_v = np.arange(0, shape[2], dtype='int16')[None,None,:].repeat(shape[0],axis=0).repeat(shape[1], axis=1)
            # store the three variables
            self.data[band][scan_n] = xr.DataArray(data=scan_v,\
                                                  dims=self.data[band].brightness_temperature_v.dims,
                                                  coords=self.data[band].brightness_temperature_v.coords)
            self.data[band][samp_n] = xr.DataArray(data=samp_v,\
                                                  dims=self.data[band].brightness_temperature_v.dims,
                                                  coords=self.data[band].brightness_temperature_v.coords)
            self.data[band][horn_n] = xr.DataArray(data=horn_v,\
                                                  dims=self.data[band].brightness_temperature_v.dims,
                                                  coords=self.data[band].brightness_temperature_v.coords)
            
            
    def get_scan_angle_feeds_offsets(self, band):
        try:
            return self.data[band].scan_angle_feeds_offsets
        except:
            return self.data[band]['scan_angle'].scan_angle_feeds_offsets

    def move_scan_angle_feeds_offset(self, band=None, hard_coded=False):
        # transfer the scan_angle_feeds_offsets tuplet to an attribute of the scan_angle variable,
        #   and delete it from the list of variables. This is because xarray later complains when
        #   the scan_angle_feeds_offsets is manipulated
        if band is None:
            bands = self.bands
        else:
            bands = (band,)

        for band in bands:
            scan_angle_offset = self.data[band].scan_angle_feeds_offsets.to_numpy()
            if hard_coded:
                scan_angle_offset = np.asarray({'L':(0.,),
                                                'C':(1.5725,4.5864,0.,5.3726),
                                                'X':(1.6670,4.7446,0.,5.5140),
                                                'KU':(1.2636,1.7316,0.5616,1.0764,1.5444,0.,0.4680,0.9360),
                                                'KA':(1.2814,1.8009,0.5887,1.0736,1.5931,0.,0.4848,1.0043)}[band])
            self.data[band].scan_angle.attrs['scan_angle_feeds_offsets'] = scan_angle_offset
            self.data[band] = self.data[band].drop(labels=('scan_angle_feeds_offsets',))
            
    def add_horn_scan_angle(self, ):
        """ Combine the scan_angle and scan_angle_feeds_offsets variables into a
               set of horn-dependent variables horn_scan_angle
        """
        var_n = 'horn_scan_angle'
        for band in self.bands:
            n_feed = n_horns[band]
            # read the variables and get them in np arrays
            scan_angle = self.data[band].scan_angle.to_numpy()
            scan_angle_offset = self.get_scan_angle_feeds_offsets(band)
            # prepare the new feed-dependent scan angle array
            if len(scan_angle.shape) != 2:
                raise ValueError("Variable 'scan_angle' for band {} has {} dims. Was expecting 2 dims".format(band, len(scan_anle.shape)))
            scan_angle = scan_angle[:,:,None].repeat(n_feed, axis=2)
            # apply the offsets
            scan_angle_corr = scan_angle + scan_angle_offset.reshape((1,n_feed))
            # keep the angles modulo 360
            scan_angle_corr = scan_angle_corr % 360
            # store in a new variable, using brightness_temperature as a template (this relies on the latter having 3 dims)
            self.data[band][var_n] = xr.DataArray(data=scan_angle_corr,\
                                                             dims=self.data[band].brightness_temperature_v.dims,
                                                             coords=self.data[band].brightness_temperature_v.coords)
    
    def align_arrays_to_start_at_zero_scan_angle(self,):
        """ data arrays originally start (index=0) where scan_angle = 0. But because of the
               horn-dependent offset, the scan arrays of the different horns are not aligned.
            This routine re-aligns all the arrays so that the horn-dependent scan angle is 0
               at the start of the arrays. This requires moving cells from the end of the
               backward scan (previous line in the array) to the start of the forward scan
        """
    
        def rearrange_array(arr, horn_start_of_scan):
            """ helper routine to move a chunk at the end of an (scan, sample, horn) arraybrightness_temperature_v
                to the start of the array. """
            
            junk = np.nan
            if not np.issubdtype(arr.dtype, np.floating):
                junk = -1
            
            ret = np.ones_like(arr) * junk
            for horn in range(0,arr.shape[2]):
                if horn_start_of_scan[horn] is None:
                    ret[:,:,horn] = arr[:,:,horn]
                else:
                    start_of_scan = horn_start_of_scan[horn]
                    nb_samples = arr.shape[1]
                    ret[1:,:(nb_samples-start_of_scan),horn] = arr[:-1,start_of_scan:,horn]
                    ret[:,(nb_samples-start_of_scan):,horn] = arr[:,:start_of_scan,horn]
            
            return ret
            
    
        # the re-arrangement is performed for each band and each horn separately
        for band in self.bands:
            # find if the scan angle offset requires an alignment, and if yes, how
                #   many samples must be moved around
            horn_start_of_scan = [None,]*n_horns[band]
            for horn in range(0,n_horns[band]):
                # check if the horn has 0-offset, in which case nothing to do here
                horn_offset = self.get_scan_angle_feeds_offsets(band)[horn]
                if  horn_offset == 0:
                    # we already have None in horn_start_of_scan
                    continue
            
                if horn_offset < 0:
                    print("WARNING ! negative scan angle offset {} for {} horn={}!".format(horn_offset, band, horn))
                    
                # load the horn-dependent scan angle
                scan_angle = self.data[band].horn_scan_angle[:,:,horn].to_numpy()
                shape = scan_angle.shape
                # the samples to be re-aligned are the small scan angle values (< 180)
                #   that are in the last 3rd of the scan angle array.
                start_of_scan = np.ones(shape, dtype='bool')
                start_of_scan[:,:2*shape[1]//3] = False
                start_of_scan *= (scan_angle < 180)  
                start_of_scan = start_of_scan.sum(axis=0)
                # this 'where' is guaranteed to work because the offset is not null
                start_of_scan = np.where(start_of_scan)[0][0]
                horn_start_of_scan[horn] = start_of_scan
            
            # Now we are ready to align all the data variables for this band and horn.
            for v in self.data[band].variables:
                # we only need to rearrange variables that have the n_horns dimension. 
                
                #print("Realign {}? {}".format(v, self.data[band][v].dims))
                if 'n_horns' in self.data[band][v].dims and len(self.data[band][v].dims) >= 3 and self.data[band][v].dims[2] == 'n_horns':
                    #print("Re-align {} {} {}".format(band, v, horn_start_of_scan))
                    np_v = self.data[band][v].values
                    #print("Before: {} {} {}".format(np_v.shape, np_v.min(), np_v.max()))
                    np_v_a = rearrange_array(np_v, horn_start_of_scan)
                    #print("After: {} {} {}".format(np_v_a.shape, np.nanmin(np_v_a), np.nanmax(np_v_a)))
                    self.data[band][v] = xr.DataArray(data=np_v_a,
                                                      dims=self.data[band][v].dims,
                                                      coords=self.data[band][v].coords,)
                    
                    #if v.startswith('orig_') or v in ('horn_scan_angle',):
                    #    h = 3
                    #    fig = plt.figure(figsize=(8,5))
                    #    ax = fig.add_subplot(2,1,1)
                    #    ax.imshow(np_v[:,:,h], interpolation='none',vmin=np_v.min(), vmax=np_v.max())
                    #    ax.set_aspect(10)
                    #    ax.set_xticks([]);ax.set_yticks([])
                    #    ax.set_title("{} {}".format(band, v),fontsize=18)
                    #    ax = fig.add_subplot(2,1,2)
                    #    ax.imshow(np_v_a[:,:,h], interpolation='none',vmin=np_v.min(), vmax=np_v.max())
                    #    ax.set_aspect(10)
                    #    ax.set_xticks([]);ax.set_yticks([])
                    #    plt.show()
                elif 'n_horns' in self.data[band][v].dims:
                    print("WARNING (align_arrays_to_start_at_zero_scan_angle): dim n_horns is not in 3rd pos for {}:{}".format(band,v))
                else:
                    pass

    
    def split_forward_backward_scans(self, method='scan_angle'):
        """ Return two CIMR_L1B objects, one with the forward arc of the scan, the other with the
            backward arc of the scan
        """
        if not self.scan == 'Full':
            raise ValueError('Error: can only split "Full" scans into forward/backward.')
        
        if not method in ('scan_angle', 'instrument_status', 'horn_scan_angle'):
            raise ValueError('Unknown method to split forward and backward scan.')
        
        fwd_l1b = deepcopy(self); fwd_l1b.scan = 'Forward'
        bck_l1b = deepcopy(self); bck_l1b.scan = 'Backward'
        
        for band in self.bands:
            if method == 'scan_angle':
                scan_angle = self.data[band].scan_angle
                fwd_mask = (scan_angle >= 0)*(scan_angle < 180.)
                bck_mask = (scan_angle >= 180.)*(scan_angle < 360.)
            elif method == 'instrument_status':
                sflag = self.data[band].instrument_status
                fwd_mask = (sflag == 0)
                bck_mask = (sflag == 1)
            elif method == 'horn_scan_angle':
                horn_scan_angle = self.data[band].horn_scan_angle
                fwd_mask = (horn_scan_angle >= 0)*(horn_scan_angle < 180.)
                bck_mask = (horn_scan_angle >= 180.)*(horn_scan_angle < 360.)

            # do the selection
            fwd_l1b.data[band] = self.data[band].where(fwd_mask, drop=True)
            bck_l1b.data[band] = self.data[band].where(bck_mask, drop=True)

            # ensure that the first three dimensions stay ('n_scans', 'n_samples_earth', 'n_horns')
            #   sometimes xarray creates a n_horns dimension at the end of the dimension tuplet, but
            #   most of our software relies on having these three dims first
            if 'n_scans_interleave_feed' in fwd_l1b.data[band].dims:
                fwd_l1b.data[band] = fwd_l1b.data[band].transpose('n_scans_interleave_feed', 'n_samples_earth', ...)
                bck_l1b.data[band] = bck_l1b.data[band].transpose('n_scans_interleave_feed', 'n_samples_earth', ...)
            else:
                fwd_l1b.data[band] = fwd_l1b.data[band].transpose('n_scans', 'n_samples_earth', 'n_horns', ...)
                bck_l1b.data[band] = bck_l1b.data[band].transpose('n_scans', 'n_samples_earth', 'n_horns', ...)
        
        return fwd_l1b, bck_l1b
    
    def reshape_interleave_feed(self):
        """ Return a new CIMR_L1B object with more scanlines and no feeds dimensions """

        # the order in which to interleave the horns is important for the end results
        #   For the moment, we use a different order for the Forward and Backward scans
        #   but this relies on having split the two in advance. The default is to use an
        #   order that will look ok with Forward and less with Backward.
        horn_order = -1
        if self.scan == 'Backward':
            horn_order = 1
    
        reshaped_ds = {}
        for band in self.bands:
            # go through all variables
            n_horn = n_horns[band]
            reshaped_da = dict()
            for v in self.data[band].variables:
                np_v = self.data[band][v].values

                if tuple(self.data[band][v].dims)[:2] != ('n_scans', 'n_samples_earth',):
                    print("WARNING: skip reshape variable {}:{} {}".format(band,v,self.data[band][v].dims))
                    continue

                ori_sizes = OrderedDict(self.data[band][v].sizes)
                new_sizes = OrderedDict()
                new_sizes['n_scans_interleave_feed'] = ori_sizes['n_scans'] * n_horn
                new_sizes[tuple(ori_sizes.keys())[1]] = tuple(ori_sizes.values())[1]
                for d in range(3,len(ori_sizes.keys())):
                    dn = tuple(ori_sizes.keys())[d]
                    new_sizes[dn] = ori_sizes[dn]

                #if len(self.data[band][v].dims) > 3:
                #    print("band {}, variable {}, ori_sizes {} new_sizes {}".format(band, v, ori_sizes, new_sizes))
                
                if tuple(self.data[band][v].dims) == ('n_scans', 'n_samples_earth'):
                    # 2d field, reshape by repeat
                    scanl, scanp = np_v.shape
                    reshaped_np = np_v.repeat( n_horn, axis=0, )
                elif tuple(self.data[band][v].dims)[:3] == ('n_scans', 'n_samples_earth', 'n_horns'):
                    # field with feed as 3rd dim: reshape by interleave
                    reshaped_np = np_v.swapaxes(1,2)[:,::horn_order,:].reshape(tuple(new_sizes.values()))
            
                # create a data array with the reshaped data  
                reshaped_da[v] = xr.DataArray(reshaped_np,
                                             dims=new_sizes.keys(),
                                             attrs=self.data[band][v].attrs, name=v)
                
            # create a xarray dataset with the reshaped data arrays
            reshaped_ds[band] = xr.Dataset(data_vars = reshaped_da, attrs=self.data[band].attrs)
    
        # finally, create a full L1B object and return it
        reshaped_l1b = deepcopy(self)
        reshaped_l1b.data = reshaped_ds
        return reshaped_l1b
    
    def coarsen_along_scanlines(self, kernel=5):
        """ Coarsen a L1B file by averaging along scanlines """
        if kernel%2 == 0:
            raise ValueError("Cannot coarsen along scanline with an even kernel.")
        
        coarsened_ds = {}
        for band in self.bands:
            # the default is to coarsen by average "kernel" values along scan
            coarsened_ds[band] = self.data[band].coarsen(n_samples_earth=kernel,boundary='trim').mean()
            # for some variables it is better to select a value with a stride of "kernel"
            for v in ('lat', 'lon', ):
                coarsened_ds[band][v] = self.data[band][v].isel(n_samples_earth=slice(kernel//2,None,kernel))
    
        coarsened_l1b = deepcopy(self)
        coarsened_l1b.data = coarsened_ds
        return coarsened_l1b
    
    def to_netcdf(self, outf):
        
        for iband, band in enumerate(self.bands):
            mode = 'w';
            if iband > 0: mode = 'a'
            self.data[band].to_netcdf(outf, mode=mode, format="NETCDF4", group=band+'_BAND')
            
    
    def plot_latlon(self, ax=None, bands = None, slice_str='[:,:,:]', colors=None, legend=True, proj='lonlat'):
        s = parse_slice(slice_str)
        
        if proj == 'lonlat':
            proj = ccrs.PlateCarree()
        elif proj == 'nh':
            proj = ccrs.LambertAzimuthalEqualArea(central_latitude=+90.0)
        else:
            print("Non-supported proj={}. Revert to PlateCarree()".format(proj))
            proj  = ccrs.PlateCarree()
            
        # Plot (main plot area)
        if ax is None:
            ax = plt.axes(projection=proj)
            ax.stock_img()
            ax.coastlines()
            #ax.set_title(os.path.basename(self.file_path))
        
        cmap_v = None
        cmap_c = 'viridis'
        cmap_m = None
        cmap_M = None
        colordict = None
        if isinstance(colors, dict):
            colordict = colors
        elif colors is None:
            colordict = dict()
            colordict['L'] = 'gold'
            colordict['C'] = 'coral'
            colordict['X'] = 'dodgerblue'
            colordict['KU'] = 'lime'
            colordict['KA'] = 'magenta'
        elif isinstance(colors, str):
            # <variable>[:<cmap>[:<vmin>:<vmax>]]
            cmap_args = colors.split(':')
            if len(cmap_args) == 1:
                if cmap_args[0] in [i for i in self.data[self.bands[0]].data_vars]:
                    # one of the variable names
                    cmap_v = cmap_args[0]
                else:
                    # assume string is a colorname to be used for all bands
                    colordict = dict()
                    for band in valid_bands:
                        colordict[band] = colors
                    
            elif len(cmap_args) == 2:
                cmap_v, cmap_c = cmap_args
            elif len(cmap_args) == 4:
                cmap_v, cmap_c, cmap_m, cmap_M = cmap_args
            cmap_c = plt.get_cmap(cmap_c)
        
        if colordict is not None and cmap_v is not None:
            raise ValueError("Cannot instruct both dicrete (color=) and colormap (c=) in plotting!")
        
        min_lon = +999
        max_lon = -999
        min_lat = +999
        max_lat = -999
        
        if bands is None:
            bands = self.bands
            
        for band in bands:
            lon = self.data[band]['lon'][s].data
            lat = self.data[band]['lat'][s].data
            valid_lonlat = ~( np.isnan(lon) + np.isnan(lat) )
            lon = lon[valid_lonlat]
            lat = lat[valid_lonlat]
            min_lon = min(lon.min(), min_lon)
            max_lon = max(lon.max(), max_lon)
            min_lat = min(lat.min(), min_lat)
            max_lat = max(lat.max(), max_lat)
            
            label = None
            if legend:
                what = cmap_v
                if cmap_v is None:
                    what = 'pos'
                label = '{} {}{}'.format(band,what,slice_str)
            
            color_kwarg = dict()
            if colordict is not None:
                color_kwarg['color'] = colordict[band]
            elif cmap_v is not None:
                cmap_v = self.data[band][cmap_v][s].data
                cmap_v = cmap_v[valid_lonlat]
                color_kwarg['c'] = cmap_v
                color_kwarg['cmap'] = cmap_c
                color_kwarg['vmin'] = cmap_m
                color_kwarg['vmax'] = cmap_M

            ax.scatter(x=lon, y=lat,
                s = 3,
                alpha=1,
                transform=ccrs.PlateCarree(),
                label=label,**color_kwarg)
        
        lat_range = max_lat - min_lat
        max_lat = min(max_lat + 0.2*lat_range, +90.)
        min_lat = max(min_lat - 0.2*lat_range, -90.)
        lon_range = max_lon - min_lon
        max_lon = min(max_lon + 0.2*lon_range, +180.)
        min_lon = max(min_lon - 0.2*lon_range, -180.)
        
        ax.set_extent([min_lon, max_lon, min_lat, max_lat,], crs=ccrs.PlateCarree())
        legend = ax.legend(fontsize=14, markerscale=3, loc='lower left')
        plt.gcf().set_size_inches((10,10))
        
        return ax
        