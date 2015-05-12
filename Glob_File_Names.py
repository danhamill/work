from glob import glob
import os

os.chdir("c:/workspace/CM/mb_sed_class")

list = glob('*xyz')

for afile in list:
	print afile

