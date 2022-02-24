#!/bin/sh
# *************************************************************************************************************
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54[at]gmail.com
# Created: 25 June 2021
# 
# Python script to copy tropomi files from txt list to a dir
# *************************************************************************************************************

import os 
import numpy as np 
import shutil

#List of files to keep
files_to_keep = np.loadtxt("/rds/general/user/ess17/home/Projects/tropomi/data/temp/tropomi_files_keep.txt", dtype=str)

# where to copy files 
dest_folder = "//rds/general/user/ess17/home/Projects/tropomi/data/tropomi_roi_pixels/"

# locations of files
file_path = "/rds/general/user/ess17/home/TROPOMI_ROI/"

for f in files_to_keep:
    full_name = os.path.join(file_path,f)
    if os.path.isfile(full_name):
        shutil.copy(full_name, dest_folder)

