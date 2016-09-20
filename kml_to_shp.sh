#Bash script to convert a directory of kml files to shape files

inkml=$(find C:/workspace/Reach_4a/2015_04/ | egrep "trackline.kml")
array1=($inkml)
outdir="C:/workspace/Merged_SS/raster/2015_04/"
ext='.shp'
for i in "${!array1[@]}"; do
kml_file=${array1[$i]}
echo $kml_file
base="$(echo ${kml_file##*/})"
base2=${base%.kml}
oName=$outdir$base2$ext
echo $oName
(cd C:/Program\ Files/GDAL; ogr2ogr -f 'ESRI Shapefile' $oName $kml_file -t_srs EPSG:26949 )
done
