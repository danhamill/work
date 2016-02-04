from glob import glob
import os
import sys

def gFpath2(drive,reach,date):
    list1 = glob(os.path.normpath(os.path.join(drive, reach, date,'*')))
    list2 =[]
    for afolder in list1:
      if afolder.rfind('class') != -1:
         list2.append(afolder)
    print list2
    
if __name__ == '__main__':
    gFpath2(sys.argv[1],sys.argv[2],sys.argv[3])
