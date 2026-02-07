import math
import sys
import numpy as np
import csv
import dataExt
import subprocess
from io import StringIO

import polars as pl
import runpy as rp

#from dataFile import CDSPlArray, mapPlArray # gets archived arrays for testing
import dataFile

"""
DATA
standardized 2d array for data
columns: lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val, temp,
Only fully do-able after going through file types

OTD test
columns: lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val 

All geospatial data is raster not vector
    geospatial data will have different resolutions

rows: station/points from globe/set of sensors on a point processed

PROCESS
We're gonna take the files ( data ) from the data folder (or remote cloud APIs not) in 
/home/user/Desktop/stars/bashOrchestrationProgram/
then output streams ( using Bash and Arrow IPC )
to processing for visualization

datafile.py is for 1) and archived file testing
dataMain.py is for 2)/3) and real-time/cyclic data 

stream file/cyclic and stream real-time are two seperate data streams


GEOSPATIAL DATA INTERPRETATION
# Latitude is given as an angular measurement ( in this program Radians )
# with 0 at the equator, ranging from -pi/2 south to pi/2 north

# Longitude is given as an angular measurement
# with 0 at the Prime Meridian, ranging from −pi westward to +pi eastward

#twotuple is [latitude, longitude]; array choice is reverse-order not array itself

WRITTEN PROCESS 1
test projections with GMT land/ocean latitude,longitude data on Processing visualization
use a stream
send 2d-array of x,y from projection P to Processing using streams

find bounds for each of the projections for scaling in Processing
"""

#standard array will be an xArray, all data CDS and in 2),3)
standardArrayStr = [[]]
standardArrayVals = [[]]
standardArray = None

#the header rows with ( dataType and dataUnits ) are done manually

# for row name completion, I need to know all possible data types:
# row[0] names for NOAA_ele and base: provider,time,name, lat, long, y_equ, x_equ, y_mer, x_mer, y_rob, x_rob, y_gall, x_gall, map_val
# row[1] names for units: str,yearmonthday, str, degreesRot, degreesRot, float, float, float, float, float, float, binary
# row[2:] vals for NOAA_ele: NOAA_ele, 20000101, map, someLambda, somePhi, somey, somex, somey, somex, somey, somex, 0or1
# column [0 to 12] correspond to NOAA_ele
NOAA_ele_row =[[ "provider", "time", "name", "lat", "long", "y_equ", "x_equ", "y_mer", "x_mer", "y_rob", "x_rob",  "y_gall", "x_gall"
, "map_val"],["str","yearmonthday","str","degrees90","degrees90","float","float","float","float","float","float","bin"]]

CIs = {"lat":0, "long":1, "y_equ":2, "x_equ":3, "y_mer":4, "x_mer":5,
"y_rob":6, "x_rob":7, "y_gall":8, "x_gall":9 }

# for every new provider, there is a new set of values and names, though it continues from the previous provider
# row[3] names for CDS and base: provider, time, name, lat, long . . . . 2m_TMP, ss_TMP, total_p
# row[4]names for units: str,yearmonthday, str, degreeRots, degreeRots . . . . . . degreesK, degreesK, m
#                                               .(10zero columns).
# row[5] vals for CDS: CDS_ERA5,20190101, ERA5, . . . . . . . . .  300,      300,    0.005
# column[0 to 3, 12 to 15] correspond to CDS, the columns with no CDS entries are entries having zero
CDS_row = [["2m_TMP","ss_TMP","total_p"],["degreesK","degreesK","m"]]

#---------------------------------------------------------------------

# row process for NOAA_elevation ( flatten to earth mask )
# refer to https://www.ngdc.noaa.gov/mgg/topo/gltiles.html
# set startPosA, startPosB, . . . . startPosP

# row names for CDS (Climate Data Store) :
    #files are from https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview
    #data is in either .grib or .NETCDF ( must be downloaded using the python earthkit module or through web API )
        #.grib has a header, and is stored in binary; it seems as though .NETCDF is what you want ( only .grib )
        #1 Used WEB-API for file, CDS and OTD are easy to access for testing, then cloud/remote access is done using
        # some API

        #2 curling https, api requests and cloud for USGS, NOAA_buoy, NOAA_w, OWM, NASA, ISS
        # ( the main actings otherwise )

        #3 big data is OSN ( for tracking all airplanes ); all of this would be much easier if I had a database
        # language like SQL; I use 2d-arrays, python and matrix concepts
        # this is where vectorization and every optimization technique possible becomes important

# row names for USGS (National Earth Center):
# https://earthquake.usgs.gov/fdsnws/event/1/ is the api-documentation for USGS earthquake catalog

#https: // earthquake.usgs.gov / fdsnws / event / 1 / [METHOD[?PARAMETERS]]


# row names to be appended with NOAA_Buoy: [ WSPD, ATMP, WTMP, OTMP ]
    #files are from https://www.ndbc.noaa.gov/data/realtime2/
    #same file format implies same data format, (.drift, .txt, .ocean)
    #LAT(1/3), LON(1/3), WSPD, ATMP, WTMP, OTMP are the usable data types in these files

    #position function that searches through all station names and links data with station name to get long/lat
    # ( .txt and .ocean don't have LAT and LONG )

    #implementation for NOAA

# row names for NOAA_NWS:

# #I can't use tagging or categories yet: unless
# each column val ( WTMP, OTMP, ATMP ) corresponds to a respective column tag and then you group the point/station
# to the data-set you're pulling from, which is only a dict corresponding to the rows to set with the columns

    # categories = [NOAA_buoy, NOAA_weather, NOAA, USGS, OWM api, NASA ], misc: [OSN]
    # for now categories and tags only include ( NOAA is a category of NOAA_buoy and NOAA_weather )
        # categories are toggled with buttons
        # tags seem like they eat too much memory and slow execution runtime, so they will not be implemented

        # column tags may be exclusive and inclusive

# Aswell as define union in arrays

# constants
# radians to degrees constant
radToDeg = (360)/(2*math.pi)
#

"""
with open('/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/robinsonTable.csv', 'r') as f:
    reader = csv.reader(f)
    rLT = list(reader) #reads CSV turns to str-2d-array
""" # lookup table not needed after being replaced by a cubic spline interpolation replacement
#hex

def makeArray():
    dataFile.CDSPlArray = dataFile.CDSCSVtoCDSArray(f"{dataFile.dataDir}/CDS_ERA5/1_outputEra/")
    dataFile.mapPlArray = dataFile.equirectFileToPolarsArray(dataFile.dataDir + dataFile.RFDSFile)

    standardArray1 = standardizeArray(dataFile.mapPlArray, dataFile.CDSPlArray)
    del dataFile.CDSPlArray
    del dataFile.mapPlArray

    standardArray = squeezeDiagonalInPlArr(standardArray1,13)
    del standardArray1

    for col in standardArray.columns:
        if standardArray[col].dtype == pl.Binary:
            standardArray = standardArray.with_columns(
                pl.col(col).cast(pl.Utf8)
            )

    return standardArray

def main():
    #dataFile.main()
    dataFile.CDSPlArray = dataFile.CDSCSVtoCDSArray(f"{dataFile.dataDir}/CDS_ERA5/1_outputEra/")
    dataFile.mapPlArray = dataFile.equirectFileToPolarsArray(dataFile.dataDir+dataFile.RFDSFile)

    #print(dataFile.mapPlArray, dataFile.CDSPlArray)

    standardArray1 = standardizeArray(dataFile.mapPlArray, dataFile.CDSPlArray)
    #print(standardArray1)

    standardArray = squeezeDiagonalInPlArr(standardArray1,13)

    print(standardArray.shape)

    #print(standardArray.select("9"),standardArray.select("10"))

    for i in range(0,14):
        print( boundsInPolarsColumn(standardArray,str(i)))
    #print(rLT) #takes str-2d-array into float-2d-array
    #for k in range(0,3):
    #    for i in range(1,19):
    #        rLT[i][k] = float(rLT[i][k])

    #test run for NOAA elevation array

    #print(robinsonLT) #Check if 2d array went from str to float

    #print("\n" + robinsonLT[1][0] )
    #print(sys.platform)
    #print(sys.version)
    #print(robinson([math.pi/4,math.pi/2])) #testing values

#flush needs a good conditional for block buffer; either append a marker line or have manual check for flush
#block buffer send, just flush whenever it fills

def standardArrayToCSV(file): # the map value takes the most space out of all the values, so it's not memory intensive
    # nor demanding for pycharm to convert the standard array to a CSV, this is for tests
    return

def arrayToCSV(array, fileOutput): #either writes or appends to make a new line in a CSV fileOutput
    return

def standardizeArray(array1, array2): #takes two polars arrays then does "array standardization"

    standardizedArray = pl.concat([array1, array2], how="diagonal").fill_null(math.nan)
    # null is turned into nan's for consistency and readability, headers and side headers are the only strs
    # so we can treat all values bounded by the headers as floats ( so for consistency nan is for floats )
    return standardizedArray

def streamSend():
    #flush when it completely fills
    print("w")

    return

def latLongToAllEntries(array): # 0 1 2 are str entries, 0 1; 2 3, 4 5, 6 7, 8 9;
    for i in range(0,4): # x coordinates from long
        array[:,2*i+2] = array[:,CIs["lat"]]

    for i in range(0,4): # y coordinates from lat
        array[:,2*i+3] = array[:,CIs["long"]]

def squeezeArray(arr, start, end):
    # starting from column start to column end, squeeze all columns into one column in the arr
    # column count := column count - ( end - start )
    #
    # loop through rows check start to end, then get first non-nan value to become new column start
    pass

def squeezeDiagonalInPlArr(df: pl.DataFrame, dense_cols) -> pl.DataFrame:
    all_cols = df.columns

    dense = df.select(all_cols[:dense_cols]) #grabs first 12 columns
    sparse = df.select(all_cols[dense_cols:])  #grabs last 6 columns

    #dense = df.select(pl.all().head(dense_cols))  # first 12 columns ( ROWS)
    #sparse = df.select(pl.all().tail(df.width - dense_cols))  # remaining n columns ( ROWS )
    #print(sparse.schema)

    diagonal_values = sparse.with_columns(
        pl.col(pl.Float32).fill_nan(None)
    ).select(
        pl.coalesce(pl.all()).alias("13")
    )

    return pl.concat([dense, diagonal_values], how="horizontal")

def boundsInPolarsColumn(polarsArray, columnIndex):

    series = polarsArray[columnIndex]
    print(series)
    lower = series.min()
    end = series.max()

    print(lower,end)

if __name__ == "__main__":
    main()

