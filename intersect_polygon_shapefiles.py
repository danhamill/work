# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 14:33:19 2016

@author: dan
"""

from osgeo import ogr, osr


sfm_shp = r"C:\Users\dan\Desktop\test_intersect\030R_150925_DSLRT18_thresh1_mask.shp"
out_shp = r"C:\Users\dan\Desktop\test_intersect\test.shp"
ts_SHP  = r"C:\Users\dan\Desktop\test_intersect\ts_030R_150925_DSLRT18.shp"

ds_ts = ogr.Open(ts_SHP)
ds_sfm = ogr.Open(sfm_shp)

layer1 = ds_ts.GetLayer(0)
layer2 = ds_sfm.GetLayer(0)


for row in layer2:
    print row.maskValue
layer2.ResetReading()

srs = osr.SpatialReference()
srs.ImportFromEPSG(26949)

driver = ogr.GetDriverByName('ESRI Shapefile')
out_shp = driver.CreateDataSource(out_shp)
out_layer = out_shp.CreateLayer('layer',srs,geom_type=ogr.wkbPolygon)
id_field = ogr.FieldDefn('id', ogr.OFTInteger)
out_layer.CreateField(id_field)


for feature1 in layer1:
   geom1 = feature1.GetGeometryRef()
   for feature2 in layer2:
       geom2 = feature2.GetGeometryRef()
       if geom2.Intersects(geom1):
           print 'We have an intersection'
           intersection = geom2.Intersection(geom1)
           wkt = intersection.ExportToIsoWkt()
           feature = ogr.Feature(out_layer.GetLayerDefn())    
           feature.SetGeometry(ogr.CreateGeometryFromWkt(wkt))
           out_layer.CreateFeature(feature)
           feature.id = 1
           del feature
         

del ds_ts, ds_sfm, out_shp