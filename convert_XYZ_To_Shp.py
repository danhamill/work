# Parse a delimited text file of volcano data and create a shapefile

import osgeo.ogr as ogr
import osgeo.osr as osr
import csv

# use a dictionary reader so we can access by field name
reader = csv.DictReader(open("NO_Reach4a_May2009_eyeball_grainsize.csv","rb"),
    delimiter=',',
    quoting=csv.QUOTE_NONE)

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
data_source = driver.CreateDataSource("AZFIPS.shp")

# create the spatial reference, AZ Central SP
srs = osr.SpatialReference()
srs.ImportFromProj4('+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +units=m +no_defs ')

# create the layer
layer = data_source.CreateLayer("AZFIPS", srs, ogr.wkbPoint)

# Add the fields we're interested in
field_name = ogr.FieldDefn("Date", ogr.OFTString)
field_name.SetWidth(24)
layer.CreateField(field_name)
layer.CreateField(ogr.FieldDefn("Easting", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Northing", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("p=50", ogr.OFTReal))

# Process the text file and add the attributes and features to the shapefile
for row in reader:
  # create the feature
  feature = ogr.Feature(layer.GetLayerDefn())
  # Set the attributes using the values from the delimited text file
  feature.SetField("Date", row['Date'])
  feature.SetField("Easting", row['Easting'])
  feature.SetField("Northing", row['Northing'])
  feature.SetField("p=50", row['p=50'])

  # create the WKT for the feature using Python string formatting
  wkt = "POINT(%f %f)" %  (float(row['Northing']) , float(row['Easting']))

  # Create the point from the Well Known Txt
  point = ogr.CreateGeometryFromWkt(wkt)

  # Set the feature geometry using the point
  feature.SetGeometry(point)
  # Create the feature in the layer (shapefile)
  layer.CreateFeature(feature)
  # Destroy the feature to free resources
  feature.Destroy()

# Destroy the data source to free resources
data_source.Destroy()