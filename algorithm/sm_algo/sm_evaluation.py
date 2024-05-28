
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
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
aoi2 = [13, 21, 21+1+7, 21+1]      # Grassland
aoi3 = [3, 11, 21+1+7, 21+1]      # Cropland
aoi4 = [3, 11, 21+1+14, 21+1+7]    # Mixed
aois_36 = np.array([aoi1, aoi2, aoi3, aoi4])
aois_09 = aois_36 * 4
aois_01 = aois_36 * 36

# Zoomed AOIs within Testcard
aoi1_zoom = [13, 21, 1+14, 1+7]    # Bare Soil
aoi2_zoom = [13, 21, 1+7, 1]      # Grassland
aoi3_zoom = [3, 11, 1+7, 1]      # Cropland
aoi4_zoom = [3, 11, 1+14, 1+7]    # Mixed
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


cm_data = [[0.2081, 0.1663, 0.5292], [0.2116238095, 0.1897809524, 0.5776761905], 
 [0.212252381, 0.2137714286, 0.6269714286], [0.2081, 0.2386, 0.6770857143], 
 [0.1959047619, 0.2644571429, 0.7279], [0.1707285714, 0.2919380952, 
  0.779247619], [0.1252714286, 0.3242428571, 0.8302714286], 
 [0.0591333333, 0.3598333333, 0.8683333333], [0.0116952381, 0.3875095238, 
  0.8819571429], [0.0059571429, 0.4086142857, 0.8828428571], 
 [0.0165142857, 0.4266, 0.8786333333], [0.032852381, 0.4430428571, 
  0.8719571429], [0.0498142857, 0.4585714286, 0.8640571429], 
 [0.0629333333, 0.4736904762, 0.8554380952], [0.0722666667, 0.4886666667, 
  0.8467], [0.0779428571, 0.5039857143, 0.8383714286], 
 [0.079347619, 0.5200238095, 0.8311809524], [0.0749428571, 0.5375428571, 
  0.8262714286], [0.0640571429, 0.5569857143, 0.8239571429], 
 [0.0487714286, 0.5772238095, 0.8228285714], [0.0343428571, 0.5965809524, 
  0.819852381], [0.0265, 0.6137, 0.8135], [0.0238904762, 0.6286619048, 
  0.8037619048], [0.0230904762, 0.6417857143, 0.7912666667], 
 [0.0227714286, 0.6534857143, 0.7767571429], [0.0266619048, 0.6641952381, 
  0.7607190476], [0.0383714286, 0.6742714286, 0.743552381], 
 [0.0589714286, 0.6837571429, 0.7253857143], 
 [0.0843, 0.6928333333, 0.7061666667], [0.1132952381, 0.7015, 0.6858571429], 
 [0.1452714286, 0.7097571429, 0.6646285714], [0.1801333333, 0.7176571429, 
  0.6424333333], [0.2178285714, 0.7250428571, 0.6192619048], 
 [0.2586428571, 0.7317142857, 0.5954285714], [0.3021714286, 0.7376047619, 
  0.5711857143], [0.3481666667, 0.7424333333, 0.5472666667], 
 [0.3952571429, 0.7459, 0.5244428571], [0.4420095238, 0.7480809524, 
  0.5033142857], [0.4871238095, 0.7490619048, 0.4839761905], 
 [0.5300285714, 0.7491142857, 0.4661142857], [0.5708571429, 0.7485190476, 
  0.4493904762], [0.609852381, 0.7473142857, 0.4336857143], 
 [0.6473, 0.7456, 0.4188], [0.6834190476, 0.7434761905, 0.4044333333], 
 [0.7184095238, 0.7411333333, 0.3904761905], 
 [0.7524857143, 0.7384, 0.3768142857], [0.7858428571, 0.7355666667, 
  0.3632714286], [0.8185047619, 0.7327333333, 0.3497904762], 
 [0.8506571429, 0.7299, 0.3360285714], [0.8824333333, 0.7274333333, 0.3217], 
 [0.9139333333, 0.7257857143, 0.3062761905], [0.9449571429, 0.7261142857, 
  0.2886428571], [0.9738952381, 0.7313952381, 0.266647619], 
 [0.9937714286, 0.7454571429, 0.240347619], [0.9990428571, 0.7653142857, 
  0.2164142857], [0.9955333333, 0.7860571429, 0.196652381], 
 [0.988, 0.8066, 0.1793666667], [0.9788571429, 0.8271428571, 0.1633142857], 
 [0.9697, 0.8481380952, 0.147452381], [0.9625857143, 0.8705142857, 0.1309], 
 [0.9588714286, 0.8949, 0.1132428571], [0.9598238095, 0.9218333333, 
  0.0948380952], [0.9661, 0.9514428571, 0.0755333333], 
 [0.9763, 0.9831, 0.0538]]


cmap_sm = LinearSegmentedColormap.from_list('cmap_sm', cm_data).reversed()


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
    
    # add labels to colorbar for land use (hard coded)
    if title == 'Land Use':
        cbar.set_ticks(ticks_lu, labels=leg_lu, rotation=40)
        
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
    plt.colorbar(location='bottom', pad=0.05)


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
    plt.subplots_adjust(wspace=0.25, hspace=-0.05)


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
    plt.colorbar(location='bottom', pad=0.05)
    
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
    plt.colorbar(location='bottom', pad=0.05)
    
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
