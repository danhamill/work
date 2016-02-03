# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 14:56:04 2016
This script loops though a parent directory and merges the pointclouds (tex or SS) for each scan.
Outputs are created in the parent directory of each scan

@author: dan
"""
from glob import glob
import os

ParentFolder = r'C:\Users\dan\Desktop\New folder\Sept 2014'
ScanList = glob(ParentFolder+os.sep+'R*')


def mergefiles(fp, CloudList):
    with open(fp, 'w') as outfile:
        for cloud in CloudList:
            with open(cloud) as infile:
                for line in infile:
                    outfile.write(line)
    outfile.close()
    

for scan in ScanList:
    #Parse scan path for scan name (i.e., R02020)
    ScanFolder = scan.split('\\')[-1]
    
    #Create lists of input point cloouds
    SS_Clouds = glob(scan + os.sep + 'SS' + os.sep +'*')
    tex_clouds =glob(scan + os.sep + 'Texture' + os.sep +'*')
    
    #Build Outfile names
    merge_tex = ScanFolder +'_tex.asc'
    merge_ss = ScanFolder +'_ss.asc'
    fp_tex =scan + os.sep + merge_tex
    fp_ss = scan + os.sep + merge_ss
    
    #Write the files
    mergefiles(fp_ss,SS_Clouds)
    print 'Created ' + fp_ss
    mergefiles(fp_tex,tex_clouds)
    print 'Created ' + fp_tex
    
