#/bin/sh
#encoding: utf-8


reach='R4a'
pkey='_pkey'
gist='_the_geom_gist'
files=$(find D:/R4a/2015_04/ -name "x_y_class*")
rpkey=$reach$pkey
rgist=$reach$gist

#create temp import table
psql -h localhost -d $reach -U postgres -p 5432 -c "CREATE TABLE tmp(
    easting double precision,
    northing double precision,
    texture double precision);"

#Create blank table for importing csv's too
# psql -h localhost -d $reach -U postgres -p 5432 -c "CREATE TABLE "$reach"(
    # easting double precision,
    # northing double precision,
    # texture double precision,
    # gid serial NOT NULL,
    # the_geom geometry,
    # CONSTRAINT "$rpkey" PRIMARY KEY (gid),
    # CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
    # CONSTRAINT enforce_geotype_geom CHECK (geometrytype(the_geom) = 'POINT'::text OR the_geom IS NULL),
    # CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 26949));"

# psql -h localhost -d $reach -U postgres -p 5432 -c "CREATE INDEX "$rgist" ON "$reach" USING gist (the_geom );"

#loop through all x_y_class*.asc files for the supplied reach    
for file in $files:
do
    echo $file
    if [ -f $file ]; then
        echo "That directory exists"
        psql -h localhost -d $reach -U postgres -p 5432 -c "\COPY tmp FROM "$file" DELIMITER ' ' CSV;"
    else
        echo "That directory doesn't exists"
    fi
    #
done
