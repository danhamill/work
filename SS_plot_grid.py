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

reach = 'R4a'
path2 = 'C:\\'
path3 = 'D:\\'	#USU Computer
date= 'April2015'

#Change to parent folder of side scan recordings
os.chdir(os.path.normpath(os.path.join(path2, 'users','dan','Reach_4a','humminbird', date)))

#get list of folder for that survey
list1 = glob('*')
fnames, outfile,x,y,tex = [], [],[], [],[]

#create list of xy_Classes from each folder
for afolder in list1:
    os.chdir(os.path.normpath(os.path.join(path2, 'users','dan','Reach_4a','humminbird', date,afolder)))
    list2 = glob('x_y_class[0-10].asc')
    for afile in list2:
        fname = os.path.normpath(os.path.join(path2, 'users','dan','Reach_4a','humminbird', date,afolder,afile))
        fnames.append(fname)

for afile in fnames:
    with open(afile,'r') as fp:
        reader = csv.reader(fp, delimiter=' ')
        for row in reader:
            a,b,c = [float(i) for i in row]
            x.append(a)
            y.append(b)
            tex.append(c)

X = np.asarray(x,'float')
X = X.flatten()
TEX = np.asarray(tex,'float')
TEX=TEX.flatten()
# merge flatten and stack
Y = np.asarray(y,'float')
Y = Y.flatten()            
trans =  pyproj.Proj(init="epsg:26949")        
res = 0.25
fig = plt.figure(frameon=False)
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_axis_off()
glon, glat = trans(X, Y, inverse=True)
fig.add_axes(ax)

del tex, x,y,X,Y

print 'now mapping'
cs2cs_args = "epsg:26949"
fig = plt.figure(frameon=False)
map = Basemap(projection='merc', epsg=cs2cs_args.split(':')[1], llcrnrlon=np.min(glon)-0.0001, llcrnrlat=np.min(glat)-0.0001,urcrnrlon=np.max(glon)+0.0001, urcrnrlat=np.max(glat)+0.0001)

map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)

x,y = map.projtran(glon, glat)

map.scatter(x.flatten(), y.flatten(), 0.5, TEX.flatten(), cmap='YlOrRd',linewidth = '0')
os.chdir(r'C:\Users\dan\Desktop')
plt.savefig('April_2015.png',bbox_inches='tight',dpi=1000, transparent=True)

