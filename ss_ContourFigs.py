from pyresample import geometry, kd_tree
from joblib import cpu_count
from glob import glob
import numpy as np
import pyproj
import os, csv, sys
import matplotlib.pyplot as plt 
from glob import glob
try:
   from mpl_toolkits.basemap import Basemap
except:
   print "Error: Basemap could not be imported"
   pass
from glob import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm

trans =  pyproj.Proj(init="epsg:26949")
cs2cs_args = "epsg:26949"

def trythis(fIn,scale_par,scale_mer,font_size,fOut):
    names = "Easting,Northing,ss_intensity"
    d = np.genfromtxt(fIn, dtype=float, delimiter =' ', names=names)
    humlon, humlat = trans(d['Easting'],d['Northing'],inverse=True)
    res = 0.25
    grid_x, grid_y = np.meshgrid( np.arange(np.floor(np.min(d['Easting'])), np.ceil(np.max(d['Easting'])), res), np.arange(np.floor(np.min(d['Northing'])), np.ceil(np.max(d['Northing'])), res) )
    
    #grid x any y coordinates
    glon, glat = trans(grid_x, grid_y, inverse=True)
    
    #resampling procedure
    orig_def = geometry.SwathDefinition(lons=humlon.flatten(), lats=humlat.flatten())
    target_def = geometry.SwathDefinition(lons=glon.flatten(), lats=glat.flatten())
    result = kd_tree.resample_nearest(orig_def, d['ss_intensity'].flatten(), target_def, radius_of_influence=1, fill_value=None, nprocs = cpu_count())
    del d
    
    #format sidescan intensities grid for plotting
    gridded_result = np.reshape(result,np.shape(glon))
    gridded_result = np.squeeze(gridded_result)
    gridded_result[np.isinf(gridded_result)] = np.nan
    gridded_result[gridded_result<=0] = np.nan
    grid2plot = np.ma.masked_invalid(gridded_result)

    print 'Now Mapping...'
    fig = plt.figure(frameon=True)
    ax = plt.subplot(1,1,1)
    map = Basemap(projection='merc', epsg=cs2cs_args.split(':')[1], llcrnrlon=np.min(glon)-0.0009, llcrnrlat=np.min(glat)-0.0009,urcrnrlon=np.max(glon)+0.0009, urcrnrlat=np.max(glat)+0.0009)
    gx,gy = map.projtran(glon,glat)
    map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=600)
    
    #Scale Bar
    map.drawmapscale(np.min(glon)-0.0004, np.min(glat)-0.0006, np.min(glon), np.min(glat), 75., units='m', barstyle='fancy', labelstyle='simple', fontcolor='#F8F8FF')
    
    #Parallels and Meridians 
    map.drawparallels(np.arange(np.min(glat)-0.001, np.max(glat)+0.001, scale_par),labels=[1,0,0,1], linewidth=0.0, fontsize = font_size)
    map.drawmeridians(np.arange(np.min(glon)-0.001, np.max(glon)+0.001, scale_mer),labels=[1,0,0,1], linewidth=0.0,fontsize = font_size)
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(font_size)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(font_size)
        
    im = map.pcolormesh(gx, gy, grid2plot, cmap='gray',vmin=0.1, vmax=30)
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbr = plt.colorbar(im, cax=cax)
    cbr.set_label('Sidescan Intensity [dBw]', size=font_size)
    for t in cbr.ax.get_yticklabels():
        t.set_fontsize(font_size)
    print 'Saving...'
    fig.set_size_inches(3.55,3.15)
    plt.savefig(fOut, bbox_inches='tight',dpi=1000, transparent=False)
    print 'Done!'
    
    

if  __name__ == '__main__':
    #Plotlist = [fIn,scale_par,scale_mer,font_size,fOut]
    #plot1_2015 = [r'C:\workspace\Research\Riverflow\2015_Plot\Plot_1\ss_plot1.asc',0.0005,0.0015,8, r'C:\workspace\Research\Riverflow\ss_colormesh_2015_Plot1.png']
    #plot2_2015 = [r'C:\workspace\Research\Riverflow\2015_Plot\Plot_2\ss_plot2.asc',0.0005,0.002,8, r'C:\workspace\Research\Riverflow\ss_colormesh_2015_Plot2.png']
    #
    #plot1_2014 = [r'C:\workspace\Research\Riverflow\2014_Plot\Plot_1\ss_plot1.asc',0.0005,0.0015,8, r'C:\workspace\Research\Riverflow\ss_colormesh_2014_Plot1.png']
    #plot2_2014 = [r'C:\workspace\Research\Riverflow\2014_Plot\Plot_2\ss_plot2.asc',0.0005,0.002,8,  r'C:\workspace\Research\Riverflow\ss_colormesh_2014_Plot2.png']
    plot3_2014 = [r'C:\workspace\Research\Riverflow\2014_Plot\Plot_3\ss_plot3.asc',0.0005,0.002,8, r'C:\workspace\Research\Riverflow\ss_colormesh_2014_Plot3.png']
    plot3_2015 = [r'C:\workspace\Research\Riverflow\2015_Plot\Plot_3\ss_plot3.asc',0.0005,0.002,8, r'C:\workspace\Research\Riverflow\ss_colormesh_2015_Plot3.png']
    
    #list = [plot1_2015,plot2_2015,plot3_2015,plot1_2014,plot2_2014,plot3_2014]
    list = [plot3_2014,plot3_2015]
    for item in list:
        fIn,scale_par,scale_mer,font_size,fOut = [i for i in item]
        trythis(fIn,scale_par,scale_mer,font_size,fOut)