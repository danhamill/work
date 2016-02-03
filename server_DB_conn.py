#On windows psycopg2 cant be imported from pip psycopg2
#Import from pip install git+https://github.com/nwcell/psycopg2-windows.git@win64-py27#egg=psycopg2
#To find all the correct dll's
#dont forget to set up ssh tunnel forwarding to local host from cmd

import psycopg2

try:
    conn = psycopg2.connect("dbname='EB' user='root' host='localhost' port='9000' password='myPassword'")
except:
    print "I am unable to connect to the database"


#get table names from data base
cur = conn.cursor()
cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
print cur.fetchall()

#Close Database
try:
    conn.close()
except:
    print "I cant close the database"

print 'Database connection destroyed'