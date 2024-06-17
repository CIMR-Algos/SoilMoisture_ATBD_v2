
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec
from matplotlib import colors
plt.rcParams.update({'font.size': 22})


# Settings

# plot limits within global EASE grids
plim_36 = np.array([82, 120, 463, 501])
plim_09 = plim_36 * 4

# Zoomed plot limits within global EASE grids
plim_36_zoom = np.array([103, 120, 463, 501-11])
plim_09_zoom = plim_36_zoom * 4
plim_01_zoom = plim_36_zoom * 36
plim_tc_36_zoom = np.array([21, 21+17, 0, 501-463-11])
plim_tc_09_zoom = plim_tc_36_zoom * 4
plim_tc_01_zoom = plim_tc_36_zoom * 36

# AOIs within Testcard
aoi1 = [13, 21, 21+1+14, 21+1+7]    # Bare Soil
aoi2 = [13, 21, 21+1+7, 21+1]       # Grassland
aoi3 = [3, 11, 21+1+7, 21+1]        # Cropland
aoi4 = [3, 11, 21+1+14, 21+1+7]     # Mixed
aois_36 = np.array([aoi1, aoi2, aoi3, aoi4])
aois_09 = aois_36 * 4
aois_01 = aois_36 * 36

# Zoomed AOIs within Testcard
aoi1_zoom = [13, 21, 1+14, 1+7]    # Bare Soil
aoi2_zoom = [13, 21, 1+7, 1]       # Grassland
aoi3_zoom = [3, 11, 1+7, 1]        # Cropland
aoi4_zoom = [3, 11, 1+14, 1+7]     # Mixed
aois_36_zoom = np.array([aoi1_zoom, aoi2_zoom, aoi3_zoom, aoi4_zoom])
aois_09_zoom = aois_36_zoom * 4
aois_01_zoom = aois_36_zoom * 36

# Legend and ticks for land use
leg_lu = ['Forest', 'Mixed', 'Cropland', 'Grassland', 'Bare Soil', 'Water']
ticks_lu = np.linspace(0.5, 4.5, 6)

# colormaps, legend, range for flags
cmap_flags = colors.ListedColormap([[1, 1, 1], 
                                    [0.8, 0.9, 1], 
                                    [0.7, 0.75, 1], 
                                    [0.75, 1, 0.7]])
leg_flag = ['No Flag', 'Water Fract', 'Coastline', 'Dense Veg.']
plt_range_flags = [0, 4]

# load 'colormaps.py' module if available
try:
    import colormaps
    cmap_sm = colormaps.get_cm('parula')
except ModuleNotFoundError:
    print('Colormaps module not available. Default colormap is used.')
    cmap_sm = 'Blues'



def _drawaois(aois, symbol, lw):
    for aoi in aois:
        xmin = aoi[0] - 0.5
        xmax = aoi[1] - 0.5
        ymin = aoi[2] - 0.5
        ymax = aoi[3] - 0.5
        plt.plot([xmin, xmin], [ymin, ymax], symbol, linewidth=lw)
        plt.plot([xmax, xmax], [ymin, ymax], symbol, linewidth=lw)
        plt.plot([xmin, xmax], [ymin, ymin], symbol, linewidth=lw)
        plt.plot([xmin, xmax], [ymax, ymax], symbol, linewidth=lw)


def plot_tc(plotdata, title, grid, plot_range, colormap=None, zoom=False):
    
    # select plot limits and aois depending on grid   
    if grid == 36:
        if zoom:
            aois = aois_36_zoom
            plim = plim_tc_36_zoom
        else:
            aois = aois_36
    elif grid == 9:
        if zoom:
            aois = aois_09_zoom
            plim = plim_tc_09_zoom
        else:
            aois = aois_09  
    elif grid == 1:
        if zoom:
            aois = aois_01_zoom
            plim = plim_tc_01_zoom
        else:
            aois = aois_01 
    else:
        raise ValueError('Grid not known (expected 9 or 36)')
         
    if zoom:
        plotdata_plim = plotdata[plim[0]:plim[1], plim[2]:plim[3]]
    else:
        plotdata_plim = plotdata
    
    # colormap settings
    if colormap is None:
        cmap = cmap_sm
    else:
        cmap = colormap

    # plot test card
    plt.imshow(plotdata_plim, vmin=plot_range[0], vmax=plot_range[1], 
               cmap=cmap)
    plt.title(title + ' ({} km)'.format(grid))
    plt.tick_params(which='both', size=0, labelsize=0)
    cbar = plt.colorbar(location='bottom', pad=0.05)
    
    # add labels and ticks to colorbar (hard coded)
    if title == 'Land Use':
        cbar.set_ticks(ticks_lu, labels=leg_lu, rotation=40)
    if (title == 'Soil Moisture') or ('Testcard' in title):
        cbar.set_label('(m³/m³)', labelpad=15)
    if 'TB' in title:
        cbar.set_label('(K)', labelpad=15)

    # draw AOIs
    _drawaois(aois, 'k-', 2)


def _plot_l1x(l1x, band, what, plot_range, colormap):
    if l1x[band]['_grid'] == 'Global Equal Area grid (36.0 km)':
        plim = plim_36
        aois = aois_36           
    elif l1x[band]['_grid'] == 'Global Equal Area grid (9.0 km)':
        plim = plim_09
        aois = aois_09
    else:
        raise ValueError('Grid not known. No Plots drawn')
    plotdata = l1x[band][what][plim[0]:plim[1], plim[2]:plim[3]]
    plt.imshow(plotdata, vmin=plot_range[0], vmax=plot_range[1], 
               cmap=colormap)
    _drawaois(aois, 'k-', 2)
    plt.tick_params(which='both', size=0, labelsize=0)
    cbar = plt.colorbar(location='bottom', pad=0.05)
    cbar.set_label('(K)', labelpad=15)


def plot_l1x(files, filenames, bands, what, whatname, plot_range, colormap):
    # function to draw a grid of plots of different files, bands, pols
    rows = len(bands) * len(what)
    cols = len(files)
    gs = gridspec.GridSpec(rows, cols, width_ratios=[1] * cols,
                           height_ratios=[1] * rows)
    fig = plt.figure(figsize=(6 * cols, 8 * rows))
    for k, file in enumerate(files):
        for i, band in enumerate(bands):
            for j, w in enumerate(what):
                bin_index = int(str(i) + str(j), 2)
                ax = fig.add_subplot(gs[bin_index, k])
                _plot_l1x(file, band, w, plot_range, colormap)
                plt.title(band + ' ' + whatname[j])
                if bin_index == 0:
                    filename = filenames[k]
                    loc = file[band][w].shape[1] / 100.
                    plt.text(loc * 0.6, -loc * 1.1, filename)
    plt.subplots_adjust(wspace=0.25, hspace=0.05)


def plot_sm(plotdata, title, grid, plot_range, colormap=None, 
            zoom=False):
    
    # select plot limits and aois depending on grid
    if grid == 36:
        if zoom:
            plim = plim_36_zoom
            aois = aois_36_zoom
        else:
            plim = plim_36
            aois = aois_36
    elif grid == 9:
        if zoom:
            plim = plim_09_zoom
            aois = aois_09_zoom
        else:
            plim = plim_09
            aois = aois_09
    else:
        raise ValueError('Grid not known (expected 9 or 36)')
        
    # mask and crop plotdata
    plotdata[plotdata == -999.] = np.nan
    plotdata_plim = plotdata[plim[0]:plim[1], plim[2]:plim[3]]
    
    # colormap settings
    if colormap is None:
        cmap = cmap_sm
    else:
        cmap = colormap

    # plot
    plt.imshow(plotdata_plim,vmin=plot_range[0], vmax=plot_range[1],
               cmap=cmap)
    plt.title(title)
    plt.tick_params(which='both', size=0, labelsize=0)
    cbar = plt.colorbar(location='bottom', pad=0.05)
    if ('SM' in title) or ('Soil Moisture' in title):
        cbar.set_label('(m³/m³)', labelpad=15)
    if ('VOD' in title) or ('Vegetation Optical Depth' in title):
        cbar.set_label('(-)', labelpad=15)
    
    # draw AOIs in black boxes
    _drawaois(aois, 'k-', 2)


def plot_sm_diff(reference, plotdata, title, grid, plot_range, colormap, 
                 zoom=False):
    
    # select plot limits and aois depending on grid
    if grid == 36:
        if zoom:
            plim = plim_36_zoom
            aois = aois_36_zoom
            plim_tc = plim_tc_36_zoom
        else:
            plim = plim_36
            aois = aois_36
    elif grid == 9:
        if zoom:
            plim = plim_09_zoom
            aois = aois_09_zoom
            plim_tc = plim_tc_09_zoom
        else:
            plim = plim_09
            aois = aois_09
    else:
        raise ValueError('Grid not known (expected 9 or 36)')
        
    # mask and crop plotdata      
    plotdata[plotdata == -999.] = np.nan
    plotdata_plim = plotdata[plim[0]:plim[1], plim[2]:plim[3]]
    if zoom:
        reference_plim = reference[plim_tc[0]:plim_tc[1], 
                                   plim_tc[2]:plim_tc[3]]
    else:
        reference_plim = reference
    
    # sanity check of plot limits of data and reference 
    if plotdata_plim.shape != reference_plim.shape:
        raise Exception('Mismatch of data and reference plot limits')
    
    # difference between reference and data
    difference = reference_plim - plotdata_plim
    
    # plot
    plt.imshow(difference, vmin=plot_range[0], vmax=plot_range[1], 
               cmap=colormap)
    plt.title(title)
    plt.tick_params(which='both', size=0, labelsize=0)
    cbar = plt.colorbar(location='bottom', pad=0.05)
    cbar.set_label('(m³/m³)', labelpad=15)
    
    # draw AOIs in black boxes
    _drawaois(aois, 'k-', 2)


def plot_flag(flag_surf, flag_ret, title, grid, zoom=False):

    # select plot limits and aois depending on grid
    if grid == 36:
        if zoom:
            plim = plim_36_zoom
            aois = aois_36_zoom
        else:
            plim = plim_36
            aois = aois_36
    elif grid == 9:
        if zoom:
            plim = plim_09_zoom
            aois = aois_09_zoom
        else:
            plim = plim_09
            aois = aois_09
    else:
        raise ValueError('Grid size not known (expected 9 or 36)')
    
    # specify flags to be plotted     
    flag_surf[flag_ret > 0] = 0   # flag=0 if no retrieval was attempted
    flag_surf[flag_surf == 3] = 2 # combine coastline and waterbody flags
    flag_surf[flag_surf > 4] = 0  # omit all other flags
    
    # crop to plot limits
    flag_surf_plim = flag_surf[plim[0]:plim[1], plim[2]:plim[3]]

    # plot
    plt.imshow(flag_surf_plim, 
               vmin=plt_range_flags[0], 
               vmax=plt_range_flags[1],
               cmap=cmap_flags)
    plt.title(title)
    plt.tick_params(which='both', size=0, labelsize=0)
    cbar = plt.colorbar(location='bottom', pad=0.05)
    cbar.set_ticks([0.5, 1.5, 2.5, 3.5], labels=leg_flag, rotation=30)
    
    # draw AOIs in black boxes
    _drawaois(aois, 'k-', 2)


def barplot(metric, ylimit, yline, linestyle, plottitle, title, ticks):
    
    # plot barplot + reference line
    plt.bar([0, 1, 2, 3], metric)
    plt.ylim(ylimit)
    plt.xlim([-0.5, 3.5])
    plt.plot([-1, 100], [yline, yline], linestyle)
    
    # plot title and ticks (if selected)
    if title:
        plt.title(plottitle)
    if ticks:
        plt.xticks([0, 1, 2, 3], 
                   ['Bare', 'Grassland', 'Cropland', 'Mixed'],
                   rotation=30)
    else:
        plt.xticks([0, 1, 2, 3], ['', '', '', ''])


def bias_aoi(reference, data, grid):
    
    # select plot limits and aois depending on grid
    if grid == 36:
        plim = plim_36
        aois = aois_36
    elif grid == 9:
        plim = plim_09
        aois = aois_09
    else:
        raise ValueError('Grid size not known (expected 9 or 36)')
        
    # initialize
    bias = np.zeros(len(aois)) * np.nan
    
    # crop data
    data_plim = data[plim[0]:plim[1], plim[2]:plim[3]]
    
    # sanity check of plot limits of data and reference 
    if data_plim.shape != reference.shape:
        raise Exception('Mismatch of data and reference limits')
    
    # calculate bias for each AOI
    for i, aoi in enumerate(aois):
        data_aoi = data_plim[aoi[3]:aoi[2], aoi[0]:aoi[1]]
        reference_aoi = reference[aoi[3]:aoi[2], aoi[0]:aoi[1]]
        bias[i] = np.nanmean(reference_aoi) - np.nanmean(data_aoi)
        
    return bias


def ubrmserr_aoi(reference, data, grid):
    
    # select plot limits and aois depending on grid
    if grid == 36:
        plim = plim_36
        aois = aois_36
    elif grid == 9:
        plim = plim_09
        aois = aois_09
    else:
        raise ValueError('Grid size not known (expected 9 or 36)')
        
    # initialize        
    ubrmserr = np.zeros(len(aois)) * np.nan

    # crop data
    data_plim = data[plim[0]:plim[1], plim[2]:plim[3]]
    
    # sanity check of plot limits of data and reference 
    if data_plim.shape != reference.shape:
        raise Exception('Mismatch of data and reference limits')
    
    # calculate ubRMSE for each AOI
    for i, aoi in enumerate(aois):
        data_aoi = data_plim[aoi[3]:aoi[2], aoi[0]:aoi[1]]
        reference_aoi = reference[aoi[3]:aoi[2], aoi[0]:aoi[1]]
        ubrmserr[i] = np.sqrt(np.nanmean((reference_aoi - data_aoi)**2))
        
    return ubrmserr
