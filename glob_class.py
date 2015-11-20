from glob import glob
import os


reach = 'R4a'
path2 = 'C:\\'
path3 = 'D:\\'	#USU Computer
date= 'April2015'

#Change to parent folder of sidescan recordings
os.chdir(os.path.normpath(os.path.join(path2, 'users','dan','Reach_4a','humminbird', date)))

#get list of folder for that survey
list1 = glob('*')

#create list of xy_Classes from each folder
for afolder in list1:
    os.chdir(os.path.normpath(os.path.join(path2, 'users','dan','Reach_4a','humminbird', date,afolder)))
    list2 = glob('x_y_class?.asc')
    for afile in list2:
        fnames = []
        fname = os.path.normpath(os.path.join(path2, 'users','dan','Reach_4a','humminbird', date,afolder,afile))
        fnames.append(fname)


print fnames        
#Change back to repository directory        
os.chdir(os.path.normpath(os.path.join(path2, 'users', 'dan', 'Reach_4a', 'Python_Scripts')))