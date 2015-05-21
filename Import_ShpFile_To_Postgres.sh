#!/bin/bash

for f in c:/workspace/CM/mb_sed_class/output2/*.shp
do
    shp2pgsql -s 26949 -D $f `basename $f .shp` | (cd C:/Program\ Files/PostgreSQL/9.4/bin; psql -h localhost -d mb_sed_class -U postgres)
done
