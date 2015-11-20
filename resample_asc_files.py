from pyresample import geometry, kd_tree
from joblib import cpu_count
import numpy as np
import pyproj


trans =  pyproj.Proj(init="epsg:26949")

fIn = "C:\\users\\dan\\Reach_4a\\humminbird\\April2015\\R02027\\x_y_class0.asc"
fOut = 'C:\\users\\dan\\Reach_4a\\humminbird\\April2015\\R02027\\x_y_class0_gridded.asc'


def ascol( arr ):
   '''
   reshapes row matrix to be a column matrix (N,1).
   '''
   if len( arr.shape ) == 1: arr = arr.reshape( ( arr.shape[0], 1 ) )
   return arr 

def trythis(fOut,fIn):
    names = "Easting,Northing,Texture"
    d = np.genfromtxt(fIn, dtype=float, delimiter =' ', names=names)
    data = np.vstack(d.flatten())
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
    

if  __name__ == '__main__':
    trythis(fOut,fIn)
