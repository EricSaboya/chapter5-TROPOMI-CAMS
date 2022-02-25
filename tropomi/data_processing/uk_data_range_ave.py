#!/bin/sh
# *******************************************************************************
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54[at]gmail.com
# Created: 25 June 2021
# 
# Python script to calculate and save TROPOMI data product average
# for dataset range
# *******************************************************************************

import os 
import sys
import harp 
import numpy as np

# TROPOMI files
trop_dir ="/rds/general/user/ess17/home/TROPOMI_ROI/"
trop_files =os.listdir(trop_dir)

# Empty arrays (global - 0.08 deg resolution)
xch4_uk =np.zeros((2250,4500)) # XCH4 product
xch4_uk_biascorr =np.zeros((2250,4500)) # Bias corrected XCH4 product
xch4_uk_biascorr_aot =np.zeros((2250,4500)) # Bias corrected XCH4 product + aot<0.10

count =np.zeros((2250,4500))
albedo_uk =np.zeros((2250,4500))
aot_uk =np.zeros((2250,4500))

for f in trop_files:
  print(f)
  product =harp.import_product(r"/rds/general/user/ess17/home/TROPOMI_ROI/"+f, operations='CH4_column_volume_mixing_ratio_dry_air_validity>99;bin_spatial(2251,-90,0.08,4501,-180,0.08);')
  product_bias =harp.import_product(r"/rds/general/user/ess17/home/TROPOMI_ROI/"+f, operations='CH4_column_volume_mixing_ratio_dry_air_validity>99;bin_spatial(2251,-90,0.08,4501,-180,0.08);',options="ch4=bias_corrected")
  product_bias_aot =harp.import_product(r"/rds/general/user/ess17/home/TROPOMI_ROI/"+f, operations='CH4_column_volume_mixing_ratio_dry_air_validity>99;aerosol_optical_depth<0.1;bin_spatial(2251,-90,0.08,4501,-180,0.08);',options="ch4=bias_corrected")
  
  aot_i =product.aerosol_optical_depth.data[0]
  aot_i =np.nan_to_num(aot_i)
  aot_uk =aot_uk +aot_i
  
  alb_i =product.surface_albedo.data[0]
  alb_i =np.nan_to_num(alb_i)
  albedo_uk =albedo_uk +alb_i
  
  xch4_i =product.CH4_column_volume_mixing_ratio_dry_air.data[0]
  xch4_i =np.nan_to_num(xch4_i)
  xch4_uk =xch4_uk +xch4_i
  
  xch4_bias_i =product_bias.CH4_column_volume_mixing_ratio_dry_air.data[0]
  xch4_bias_i =np.nan_to_num(xch4_bias_i)
  xch4_uk_biascorr =xch4_uk_biascorr +xch4_bias_i
  
  xch4_bias_aot_i =product_bias_aot.CH4_column_volume_mixing_ratio_dry_air.data[0]
  xch4_bias_aot_i =np.nan_to_num(xch4_bias_aot_i)
  xch4_uk_biascorr_aot =xch4_uk_biascorr_aot +xch4_bias_aot_i
  
  count =count +np.nan_to_num(xch4_i/xch4_i)

  
# save arrays 
savedir ="/rds/general/user/ess17/home/scripts/tropomi/"
np.savetxt(savedir+"UK_2018_2020_xch4_ave.txt", xch4_uk/count)
np.savetxt(savedir+"UK_2018_2020_xch4_bias_ave.txt", xch4_uk_biascorr/count)
np.savetxt(savedir+"UK_2018_2020_xch4_bias_aot_ave.txt", xch4_uk_biascorr_aot/count)
np.savetxt(savedir+"UK_2018_2020_aot_ave.txt", aot_uk/count)
np.savetxt(savedir+"UK_2018_2020_albedo_ave.txt", albedo_uk/count)
np.savetxt(savedir+"UK_2018_2020_count.txt", count)
