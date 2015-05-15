import psycopg2

try:
    conn = psycopg2.connect("dbname='test' user='postgres' host='localhost' password='daniel'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

cur.execute("""SELECT * FROM layer Order By sed_class """)

rows = cur.fetchall()

#Close Database
try:
    conn.close()
except:
    print "I cant close the database"