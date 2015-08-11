#/bin/sh
#encoding: utf-8


reach='R4a'
ss='r4a'
pkey='_pkey'
gist='_the_geom_gist'
files=$(find D:/R4a/2015_04/ -name "x_y_class*")
rpkey=$reach$pkey
rgist=$reach$gist


#Create blank table for importing csv's too
psql -h localhost -d $reach -U postgres -p 5432 -c "CREATE TABLE "$ss"(
  gid SERIAL NOT NULL,
  easting double precision,
  northing double precision,
  texture double precision,
  the_geom GEOMETRY,
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(the_geom) = 'POINT'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 26949));"

#loop through all x_y_class*.asc files for the supplied reach    
for file in $files:
do
echo $file
if [ -f $file ]; then
echo "That directory exists"
psql -h localhost -d $reach -U postgres -p 5432 -c "\COPY "$ss" (easting,northing,texture) FROM "$file" DELIMITER ' ' CSV;"
else
echo "That directory doesn't exists"
fi
done

#Populate Geometry field 
psql -h localhost -d $reach -U postgres -p 5432 -c "UPDATE "$ss" SET the_geom = ST_GeomFromText('POINT(' || easting || ' ' || northing || ')', 26949);"
