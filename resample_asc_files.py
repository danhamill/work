from pyresample import geometry, kd_tree
from joblib import cpu_count
from glob import glob
import numpy as np
import pyproj
import os

trans =  pyproj.Proj(init="epsg:26949")


def right(s, amount):
    return s[-amount:]
    
def ascol( arr ):
   '''
   reshapes row matrix to be a column matrix (N,1).
   '''
   if len( arr.shape ) == 1: arr = arr.reshape( ( arr.shape[0], 1 ) )
   return arr 

def trythis(fOut,fIn):
    names = "Easting,Northing,Texture"
    d = np.genfromtxt(fIn, dtype=float, delimiter =' ', names=names)
    humlon, humlat = trans(d['Easting'],d['Northing'],inverse=True)
    orig_def = geometry.SwathDefinition(lons=humlon.flatten(), lats=humlat.flatten())
    
    res = 0.25
    grid_x, grid_y = np.meshgrid( np.arange(np.floor(np.min(d['Easting'])), np.ceil(np.max(d['Easting'])), res), np.arange(np.floor(np.min(d['Northing'])), np.ceil(np.max(d['Northing'])), res) )
    longrid, latgrid = trans(grid_x, grid_y, inverse=True)
    target_def = geometry.SwathDefinition(lons=longrid.flatten(), lats=latgrid.flatten())
    result = kd_tree.resample_nearest(orig_def, d['Texture'].flatten(), target_def, radius_of_influence=1, fill_value=None, nprocs = cpu_count())
    
    del d
    
    gridded_result = np.reshape(result,np.shape(longrid))
    mask = gridded_result.mask==True
    with open(fOut, 'wb')as f:
        np.savetxt(f, np.hstack((ascol(grid_x[mask==False].flatten()),ascol(grid_y[mask==False].flatten()),ascol(gridded_result[mask==False].flatten()))),delimiter=' ', fmt="%8.6f %8.6f %1.6f")   
    f.close()
    del gridded_result, mask, result
    
if  __name__ == '__main__':
    WrkFolder = os.path.normpath(os.path.join('D:\\','2015_09_R4a'))
    Scan_List = glob(WrkFolder+os.sep+'R*')
    for scan in Scan_List[2:]:
        point_cloud_list = glob(scan + os.sep + 'x_y_class[0-20].asc')
        for point_cloud in point_cloud_list:
            fIn = point_cloud
            scan_name = right(os.path.split(point_cloud)[0],6)
            fOut = os.path.split(point_cloud)[0] + os.sep + scan_name + os.path.split(point_cloud)[1]
            print 'Now Gridding ' + point_cloud
            trythis(fOut,fIn)