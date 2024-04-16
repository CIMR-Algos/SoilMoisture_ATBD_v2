import numpy as np
import xarray as xr
import pyresample as pr

from datetime import datetime

l2_format_version = '0.0.1'
l2_time_unit = "days since 2000-01-01 00:00:00 UTC"

def _set_geospatial_latlon_attributes(ds, geo_def):

    lons, lats = geo_def.get_lonlats()

    lat_min = lats.min()
    if (0, -90.) in geo_def:
        lat_min = -90.
    lat_max = lats.max()
    if (0, +90.) in geo_def:
        lat_max = +90.
    lon_min = lons.min()
    lon_max = lons.max()
    if (180, 0) in geo_def:
        lon_min = -180.
        lon_max = +180.
        
    ds.attrs['geospatial_lat_max'] = lat_max
    ds.attrs['geospatial_lat_min'] = lat_min
    ds.attrs['geospatial_lon_max'] = lon_max
    ds.attrs['geospatial_lon_min'] = lon_min

    return ds

def to_cf_template(area_def, skip_lonlat=True, crs_encoding='pyproj_to_cf'):
    """Return a template xarray Dataset holding the structure of a netCDF/CF file for this grid."""
    
    # prepare the crs object with pyproj.to_cf()
    crs_cf = area_def.crs.to_cf()
    type_of_grid_mapping = crs_cf['grid_mapping_name']
    
    # alter this set of attributes on user input
    if crs_encoding == 'pyproj_to_cf':
        pass
    elif crs_encoding == 'only_cf_attrs':
        crs_cf.pop('crs_wkt')
    elif crs_encoding == 'only_wkt':
        crs_cf = {'crs_wkt': crs_cf['crs_wkt']}
    else:
        raise ValueError("Unsupported value for crs_encoding=")
        
    # prepare the x and y axis (1D)
    xy = dict()
    xy_dims = ('x', 'y')
    for axis in xy_dims:
        
        # access the valid standard_names (also handle the 'default')
        try:
            valid_coord_standard_names = pr.utils.cf._valid_cf_coordinate_standardnames[type_of_grid_mapping][axis]
        except KeyError:
            valid_coord_standard_names = pr.utils.cf._valid_cf_coordinate_standardnames['default'][axis]
        
        xy[axis] = dict()
        # CF wants the center of the grid cells
        if axis == 'x':
            xy[axis]['_coords'] = area_def.projection_x_coords
        else:
            xy[axis]['_coords'] = area_def.projection_y_coords     
        # each axis requires a valid name, which depends on the type of projection
        xy[axis]['standard_name'] = valid_coord_standard_names[0]
        # CF recommendation to have axis= attribute
        xy[axis]['axis'] = axis.upper()
        # units
        xy[axis]['units'] = 'm'
    
    # latitude and longitude (2D)
    lons, lats = area_def.get_lonlats()
    
    # determine the order of the x, y dimensions that match the shape of lat/lon arrays
    
    if lons.shape == (len(xy['y']['_coords']),len(xy['x']['_coords'])):
        xy_dims = ('y', 'x')
    elif lons.shape == (len(xy['x']['_coords']),len(xy['y']['_coords'])):
        xy_dims = ('x', 'y')
    else:
        raise ValueError("Incompatible shape for lon/lat {}, x {}, and y {}.".format(lons.shape,
                                                                                    len(xy['x']['_coords']),
                                                                                    len(xy['y']['_coords'])))
    
    # define a Dataset as a template.
    #   we cannot define a Dataset without a data variable. The strategy is to 
    #   create the Dataset with an (empty) variable, and the user can later 
    #   add his own variables, and finally drop our 'template' variable before
    #   writing to file.
    varn = 'template'
    shape = lons.shape
    da_empty_data = np.ones_like(lons) * np.nan
    da_dims = list(xy_dims)
    da_coords = {'x':('x',xy['x']['_coords']), 'y':('y',xy['y']['_coords']),}
    if not skip_lonlat:
        da_coords['lon']=(xy_dims, lons)
        da_coords['lat']=(xy_dims, lats)
    ds = xr.Dataset(data_vars={varn:(da_dims, da_empty_data),
                               'crs':([], 0)},
                    coords=da_coords,)
    
    # add CF attributes and encodings to the xarray template
    
    # x and y dims
    for axis in xy_dims:
        for attr in xy[axis].keys():
            if attr.startswith('_'): continue
            ds[axis].attrs[attr] = xy[axis][attr]
        ds[axis].encoding = {'_FillValue':None}
    
    # crs object
    ds['crs'].attrs = crs_cf
    ds['crs'].encoding = {'dtype':'int32'}
    
    # latitude and longitude
    if not skip_lonlat:
        ds['lon'].attrs={'long_name': 'longitude coordinate', 'standard_name': 'longitude', 'units': 'degrees_east'}
        ds['lat'].attrs={'long_name': 'latitude coordinate', 'standard_name': 'latitude', 'units': 'degrees_north'}
        ds['lon'].encoding = {'_FillValue':None}
        ds['lat'].encoding = {'_FillValue':None}
        
    # the empty variable itself
    ds[varn].attrs['grid_mapping'] = 'crs'
    
    # global attributes
    ds.attrs['Conventions'] = 'CF-1.8, ACDD-1.3'
    ds = _set_geospatial_latlon_attributes(ds, area_def)
    ds.attrs['geospatial_bounds_crs'] = 'EPSG:' + str(area_def.crs.to_epsg())
    
    return ds
    
def get_CIMR_L2_template(l2_product_type, geo_def=None, add_time=None):

    # check the validity of the input parameters
    l2_product_types = ('swath', 'grid')
    if l2_product_type not in l2_product_types:
        raise ValueError("The L2 product type is not understood. Should be one of {}.".format(l2_product_types))

    if l2_product_type == 'grid':
        if not isinstance(geo_def, pr.geometry.AreaDefinition):
            raise ValueError("The geo_def should be a Pyresample AreaDefinition for the product type 'grid'. Got {}.".format(type(geo_def)))
        if add_time is not None:
            min_l2_dt, max_l2_dt = None, None
            if len(add_time) == 1:
                l2_dt = add_time[0]
            elif len(add_time) == 3:
                l2_dt, min_l2_dt, max_l2_dt = add_time

    elif l2_product_type == 'swath':
        if not isinstance(geo_def, pr.geometry.SwathDefinition):
            raise ValueError("The geo_def should be a Pyresample SwathDefinition for the product type 'swath'. Got {}.".format(type(geo_def)))

    # prepare the xarray Dataset corresponding to the product type
    if l2_product_type == 'swath':
        raise NotImplementedError("The 'swath' product type is unforunately not yet implemented.")

    elif l2_product_type == 'grid':
        ds = to_cf_template(geo_def, skip_lonlat=False)

        # add time dimension if asked by user
        if add_time is not None:
            # add a time dimension
            time_da = xr.DataArray([l2_dt,], [('time', [l2_dt,])])
            ds = ds.expand_dims(time=time_da)
            # configure time attributes
            ds['time'].encoding = {'units': l2_time_unit, 'calendar': 'standard', '_FillValue':None}
            # add time bounds if they were provided
            if min_l2_dt is not None:
                time_bounds_name = 'time_bnds'
                da_time_bounds = xr.DataArray([[min_l2_dt, max_l2_dt],], dims=('time', 'two',), name=time_bounds_name)
                ds = ds.merge(da_time_bounds)
                ds['time'].attrs['bounds'] = time_bounds_name

    # add global attributes
    ds.attrs['project'] = 'ESA CIMR DEVALGO (contract 4000137493)'
    ds.attrs['project_lead'] = 'Thomas Lavergne'
    ds.attrs['project_lead_email'] = 'thomas.lavergne@met.no'
    ds.attrs['date_created'] = datetime.utcnow().isoformat(timespec="seconds")+'Z'
    ds.attrs['processing_level'] = 'Level-2'
    ds.attrs['standard_name_vocabulary'] = "CF Standard Name Table (Version 83, 17 October 2023)"
    ds.attrs['spacecraft'] = "CIMR"
    ds.attrs['instrument'] = "CIMR" ;
    ds.attrs['product_level'] = "2" ;
    if min_l2_dt is not None:
        ds.attrs['time_coverage_start'] = np.datetime_as_string(min_l2_dt)+'Z'
    if max_l2_dt is not None:
        ds.attrs['time_coverage_end'] = np.datetime_as_string(max_l2_dt)+'Z'
    ds.attrs['format_version'] = l2_format_version ;

    return ds


