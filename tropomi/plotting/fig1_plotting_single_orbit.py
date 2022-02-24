#!/bin/sh
# ****************************************************************************
# ABOUT
# plot_single_orbits.py
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54[at]gmail.com
# Created 8 Sep 2021
# Last modified 14 Dec. 2021
#
# Plot TROPOMI single overpasses over UK (data spatially binned 0.08 degrees)
# ****************************************************************************

import os 
import sys
import harp
import cartopy
import numpy as np 
import datetime as dt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def daily_orbit_plot(x):
  """ find time of retrieval
  """
  start_time = x.datetime_start.data
  # start time are seconds since 01 01 2010
  time_base = dt.datetime(2010,1,1,0,0)
  time_obs = time_base + dt.timedelta(seconds=start_time[0])
  return time_obs


def load_data(tropomi_file):
  """ Load data from TROPOMI
  """
  # Load data product from TROPOMI
  product = harp.import_product(r"//rds/general/user/ess17/home/Projects/tropomi/data/tropomi_roi_pixels/"+tropomi_file,operations='CH4_column_volume_mixing_ratio_dry_air_validity>99;bin_spatial(2251,-90,0.08,4501,-180,0.08);',options="ch4=bias_corrected")
  
  # Column average
  xch4 = product.CH4_column_volume_mixing_ratio_dry_air.data[0]
  
  # x2 uncertainty, based on single sounding precision as measurement noise. See Earth Engine page for more details
  xch4_uncert = product.CH4_column_volume_mixing_ratio_dry_air_uncertainty.data[0] * 2.
  
  # lat-lon bounds of gridded product
  lat = np.arange(-90.0,90.08, 0.08)
  lon = np.arange(-180.0,180.08, 0.08)
  xx, yy = np.meshgrid(lon, lat)
  
  # time stamp of data product
  time_out = daily_orbit_plot(product)
  
  return time_out, xx, yy, xch4, xch4_uncert


def plot_data(xx, yy, xch4, time, savepath):
  """ plot gridded tropomi product over UK
  """
  fig = plt.figure()
  ax = plt.subplot(projection=ccrs.PlateCarree())
  a0 = ax.pcolormesh(xx, yy, xch4, cmap='viridis',vmin=1835, vmax=1870)
  ax.coastlines()
  ax.set_extent([-9.0, 1.75, 49.9, 59.9])
  cbar = fig.colorbar(a0, ax=ax, orientation='vertical', label=r'XCH$_{4}$ (ppb)')
  fig.tight_layout()
  plt.savefig(savepath+str(time)+".png", dpi=300)
  plt.clf()
  plt.close()
    
# *************************************************************************************************************
# list of tropomi files
trop_files = os.listdir("//rds/general/user/ess17/home/Projects/tropomi/data/tropomi_roi_pixels/")

# find times of tropomi orbits
trop_times = [] 
for i in trop_files:
  t_out, xx, yy, xch4, xch4_err = load_data(i)
  trop_times.append(t_out)

for i, j in enumerate(trop_times):
  t_out, xx, yy, xch4, xch4_err = load_data(trop_files[i])
  if i!= len(trop_times):
    if t_out not in np.array(trop_times)[i+1::]:
      plot_data(xx, yy, xch4, t_out, "/rds/general/user/ess17/home/Projects/tropomi/plotting/fig1/figs/")
    
    else:
      inds = np.where(np.array(trop_time)[i+1::]==t_out)
      t_out2, xx2, yy2, xch4_2, xch4_err2 = load_data(trop_files[int(i+inds[0])])
      print(t_out, t_out2)

      count = (xch4/xch4) + (xch4_2/xch4_2)
      xch4 = (XCH4+XCH4_2)/count
      plot_data(xx, yy, xch4, t_out, "/rds/general/user/ess17/home/Projects/tropomi/plotting/fig1/figs/")
