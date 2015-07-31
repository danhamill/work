from glob import glob
import os
import numpy as np
import psycopg2



reach = 'R4a'
path2 = 'C:\\'
path3 = 'D:\\'	#USU Computer
date= '2015_04'

os.chdir(os.path.normpath(os.path.join(path3, reach, date)))

#get list of folder for that survey
list1 = glob('*')

#create list of xy_Classes from each folder
for afolder in list1:
    os.chdir(os.path.normpath(os.path.join(path3, reach, date,afolder)))
    list2 = glob('x_y_class?.asc')
    for afile in list2:
        fnames = []
        fname = os.path.normpath(os.path.join(path3, reach, date,afolder,afile))
        fnames.append(fname)
        print fnames 


#connect to datatbase
try:
    conn = psycopg2.connect("dbname='mb_sed_class' user='postgres' host='localhost' password='Daniel'")
    print 'we are connected'
except:
    print "I am unable to connect to the database"
    

    
#Close Database
try:
    conn.close()
except:
    print "I cant close the database"
#Change Directory back to git repository
os.chdir(os.path.normpath(os.path.join(path2,'workspace', 'Reach_4a', 'Python_Scripts')))