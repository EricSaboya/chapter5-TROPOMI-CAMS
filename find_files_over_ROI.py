#!/bin/sh

# *************************************************************************************************************
# find_files_over_ROI.py
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54[at]gmail.com
# Created: 23 June 2021
#
# Python script to retain TROPOMI files with high pixel values over UK
# files are saved to txt file list
#
# Data gridded to 0.08 by 0.08 degrees which closely matches the resolution of TROPOMI
#
# Make sure using TROPOMI venv
# *************************************************************************************************************
import os 
import numpy as np
import harp 

# Directory where saved TROPOMI files are kept
DataPath = "/rds/general/user/ess17/home/TROPOMI_ROI/"
# List of files in directory
files = os.listdir(DataPath)

# Empty list where file names are kept
keep = []

for f in range(len(files)):
    print(f, files[f])
    try:
        Product=harp.import_product(r"/rds/general/user/ess17/home/TROPOMI_ROI/"+files[f], operations='CH4_column_volume_mixing_ratio_dry_air_validity>99;keep(latitude_bounds,longitude_bounds,CH4_column_volume_mixing_ratio_dry_air);bin_spatial(2251,-90,0.08,4501,-180,0.08);')
        xCH4 = Product.CH4_column_volume_mixing_ratio_dry_air.data
        lat = np.arange(-90.0,90.08, 0.08)
        lon = np.arange(-180.0,180.08, 0.08)
        inds_lat = np.intersect1d(np.where(lat>49.0),np.where(lat<60.16))
        inds_lon = np.intersect1d(np.where(lon>-10.0),np.where(lon<3.15))

        xx = []
        for i in inds_lat:
            for j in inds_lon:
                if xCH4[0][i][j]>0:
                    xx.append(xCH4[0][i][j])
        total=np.sum(xx)

        if total>100000: # keep is approx 50 pixels in ROI
            keep.append(files[f])
    except:
        pass

fw=open("/rds/general/user/ess17/home/Projects/tropomi/data/temp/tropomi_files_keep.txt","a+")
for i in keep:
    fw.write(str(i)+'\n')
fw.close() 
