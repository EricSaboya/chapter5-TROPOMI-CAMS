#!/bin/sh
#set up environment
# HPC requirements
#PBS -l walltime=06:00:00
#PBS -l select=1:ncpus=8:mem=8gb

# *************************************************************************************************************
# ABOUT
# download_data.sh
# Author: Eric Saboya, Dept. of Physics, Imperial College London
# Contact: ericsaboya54[at]gmail.com
# Created 18 Jun 2021
# Last modified 14 Dec. 2021
#
# BASH script for batch downloading TROPOMI files from across a region of interest
# A box is created over the region of interest with [lat1, lon1] the lower-left coordinate
# and [lat2, lon2] the upper-right coordinate

# *************************************************************************************************************

# setting up virtual environment
module load anaconda3/personal
source /rds/general/user/ess17/home/anaconda3/bin/activate TROPOMI
python --version

# batch downloading script input
INFILE=dhusget.sh


# Loop through each 0 to n-1 days of month
for i in {1..30}
do
  echo $i

  # region of interest
  lat1=49.696
  lon1=-13.535
  lat2=60.305
  lon2=3.867

  # path to batch-downloading script 
  script=$HOME/Projects/tropomi/processing/$INFILE

  # path to directory where TROPOMI files downloaded
  save=$HOME/TROPOMI_ROI/

  # start time
  TimeS="2021-01-${i}T00:00:00.000Z"

  # end time
  TE=$(($i + 1))
  TimeE="2021-01-${TE}T00:00:00.000Z"

  # running script and downloading files
  ${script} -u s5pguest -p s5pguest -S ${TimeS} -E ${TimeE} -T L2__CH4___ -l 50 -o product -O ${save} footprint:"Intersects(POLYGON((${lon1} ${lat1},${lon2} ${lat1},${lon2} ${lat2}, ${lon1} ${lat2}, ${lon1} ${lat1})))" -l 100 -o product -O ${save}

done

# Last day of the month
# region of interest
lat1=49.696
lon1=-13.535
lat2=60.305
lon2=3.867

# path to batch-downloading script
script=$HOME/Projects/tropomi/processing/$INFILE

# path to directory where TROPOMI files downloaded
save=$HOME/TROPOMI_ROI

# start time
TimeS="2021-01-31T00:00:00.000Z"
# end time
TimeE="2021-02-01T00:00:00.000Z"

#running script
${script} -u s5pguest -p s5pguest -S ${TimeS} -E ${TimeE} -T L2__CH4___ -l 50 -o product -O ${save} footprint:"Intersects(POLYGON((${lon1} ${lat1},${lon2} ${lat1},${lon2} ${lat2}, ${lon1} ${lat2}, ${lon1} ${lat1})))" -l 100 -o product -O ${save}

                                                                                                                                                 80,0-1        Bot
