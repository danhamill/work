from pyresample import geometry, kd_tree
from joblib import cpu_count
import numpy as np
import pyproj


area_id = 'r4a'
name = 'Reach 4a grid'
proj_id = 'EPSG:26949'
proj4_args = 'proj=tmerc, +lat_0=31, +lon_0=-111.9166666666667, +k=0.9999, +x_0=213360, +y_0=0, +ellps=GRS80, +datum=NAD83, +units=m, +no_defs'
x_size = 400
y_size = 800
area_extent = (223000,578100,223100,578300)
proj_dict = {'proj': 'tmerc', 'lat_0': '31', 'lon_0': '-111.9166666666667', 'k': '0.9999', 'x_0': '213360', 'ellps':'GRS80', 'datum':'NAD83', 'units':'m', 'no_defs':''}
area_def = geometry.AreaDefinition(area_id, name, proj_id, proj_dict, x_size, y_size, area_extent)
print area_def

trans =  pyproj.Proj(init="epsg:26949")

fname = "E:/R4a/2012_05/R00034/x_y_class0.asc"
names = "Easting,Northing,Texture"
d = np.genfromtxt(fname, dtype=float, delimiter =' ', names=names)
data = np.vstack(d.flatten())
humlon, humlat = trans(d['Easting'],d['Northing'],inverse=True)
orig_def = geometry.SwathDefinition(lons=humlon.flatten(), lats=humlat.flatten())

res = 0.25
grid_x, grid_y = np.meshgrid( np.arange(np.floor(np.min(d['Easting'])), np.ceil(np.max(d['Easting'])), res), np.arange(np.floor(np.min(d['Northing'])), np.ceil(np.max(d['Northing'])), res) )
longrid, latgrid = trans(grid_x, grid_y, inverse=True)
target_def = geometry.SwathDefinition(lons=longrid.flatten(), lats=latgrid.flatten())

result = kd_tree.resample_nearest(orig_def, d['Texture'].flatten(), target_def, radius_of_influence=1, fill_value=None, nprocs = cpu_count())

gridded_result = np.reshape(result,np.shape(longrid))


result = kd_tree.resample_nearest(orig_def, d['Texture'].flatten(), area_def, radius_of_influence=1, fill_value=None, nprocs = cpu_count())



