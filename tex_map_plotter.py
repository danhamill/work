import os, csv, sys
import numpy as np
import matplotlib.pyplot as plt 
import pyproj
from glob import glob
try:
   from mpl_toolkits.basemap import Basemap
except:
   print "Error: Basemap could not be imported"
   pass
from glob import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable


def make_plot(FolderIn,scale_par,scale_mer,font_size,out_name):
    #Change to parent folder of side scan recordings
    os.chdir(FolderIn,)
    
    #get list of folder for that survey
    list1 = glob('*')
    fnames, outfile,x,y,tex = [], [],[], [],[]
    
    for afile in list1:
        with open(afile,'r') as fp:
            reader = csv.reader(fp, delimiter=' ')
            for row in reader:
                a,b,c = [float(i) for i in row]
                x.append(a)
                y.append(b)
                tex.append(c)
    
    # merge flatten and stack
    X = np.asarray(x,'float')
    X = X.flatten()
    TEX = np.asarray(tex,'float')
    TEX=TEX.flatten()
    Y = np.asarray(y,'float')
    Y = Y.flatten()  
    del x, y, tex    
        
        
    trans =  pyproj.Proj(init="epsg:26949") 
    
    
    
    #Transform Coordnates to lat/lon for plotting
    glon, glat = trans(X, Y, inverse=True)
    del X,Y
    
    print 'now mapping'
    
    
    
    cs2cs_args = "epsg:26949"
    fig = plt.figure(frameon=True)
    ax = plt.subplot(1,1,1)
    
    
    map = Basemap(projection='merc', epsg=cs2cs_args.split(':')[1], llcrnrlon=np.min(glon)-0.0009, llcrnrlat=np.min(glat)-0.0009,urcrnrlon=np.max(glon)+0.0009, urcrnrlat=np.max(glat)+0.0009)
    
    map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=600)
    
    #Scale Bar
    map.drawmapscale(np.min(glon)-0.0004, np.min(glat)-0.0006, np.min(glon), np.min(glat), 75., units='m', barstyle='fancy', labelstyle='simple', fontcolor='#F8F8FF')
    
    #Parallels and Meridians 
    map.drawparallels(np.arange(np.min(glat)-0.001, np.max(glat)+0.001, scale_par),labels=[1,0,0,1], linewidth=0.0, fontsize = font_size)
    map.drawmeridians(np.arange(np.min(glon)-0.001, np.max(glon)+0.001, scale_mer),labels=[1,0,0,1], linewidth=0.0,fontsize = font_size)
    
    
    #Transform texture classificatons back to state plane
    x,y = map.projtran(glon, glat)
    del glon, glat
    
    #Smaller Ticks
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(font_size)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(font_size)
    
    
    TEX2 = np.round(5*TEX.flatten())/5 # or 4,6,7 - play with numbers
    #Plot Texture Classifications
    im = map.scatter(x.flatten(), y.flatten(), 0.5, TEX2, cmap='YlOrRd',linewidth = '0', vmin=0.1, vmax=0.7)
    #im = map.contourf(x.flatten(), y.flatten(), TEX.flatten(), cmap='YlOrRd',levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7], vmin=0.1, vmax=0.7)
    #im = map.hexbin(x.flatten(), y.flatten(), C=TEX.flatten(), cmap='YlOrRd',reduce_C_function = np.mean, gridsize=5, mincnt=3, linewidths=0.5, edgecolors='k',vmin=0.1, vmax=0.7)
    
    #Add color bar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbr = plt.colorbar(im, cax=cax)
    cbr.set_label('Texture Lengthscale [m]', size=font_size)
    for t in cbr.ax.get_yticklabels():
        t.set_fontsize(font_size)
    os.chdir(r'C:\workspace\Research\Riverflow')
    
    #Save the plot
    print 'Saving ...'
    fig.set_size_inches(3.55,3.15)
    #plt.show()
    plt.savefig(out_name, bbox_inches='tight',dpi=1000, transparent=False)
    print 'Done!'

plot3_2014 = [r'C:\workspace\Research\Riverflow\2014_Plot\Plot_3',0.0005,0.002,8, 'Scatter_5class_2014_Plot3.png']
plot2_2014 = [r'C:\workspace\Research\Riverflow\2014_Plot\Plot_2',0.0005,0.002,8, 'Scatter_5class_2014_Plot2.png']
plot1_2014 = [r'C:\workspace\Research\Riverflow\2014_Plot\Plot_1',0.0005,0.0015,8,'Scatter_5class_2014_Plot1.png']
plot3_2015 = [r'C:\workspace\Research\Riverflow\2015_Plot\Plot_3',0.0005,0.002,8, 'Scatter_5class_2015_Plot3.png']
plot2_2015 = [r'C:\workspace\Research\Riverflow\2015_Plot\Plot_2',0.0005,0.002,8, 'Scatter_5class_2015_Plot2.png']
plot1_2015 = [r'C:\workspace\Research\Riverflow\2015_Plot\Plot_1',0.0005,0.0015,8,'Scatter_5class_2015_Plot1.png']

list = [plot1_2014,plot2_2014,plot3_2014,plot3_2015,plot2_2015,plot1_2015]

for item in list:
    FolderIn, scale_par, scale_mer,font_size,out_name = [i for i in item]
    make_plot(FolderIn,scale_par,scale_mer,font_size,out_name)