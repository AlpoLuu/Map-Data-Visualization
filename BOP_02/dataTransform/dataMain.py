from dataFile import scaleCoords

import math
import sys
import numpy as np
import csv
import dataExt
import subprocess
import pandas as pd
from io import StringIO

from mpmath import ln

"""
standardized 2d array for data
columns: lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val, temp,
Only fully do-able after going through file types

OTD test
columns: lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val 

All geospatial data is raster not vector

rows: station/points from globe/set of sensors on a point processed
"""

"""
We're gonna take the files ( data ) from the data folder in 
/home/user/Desktop/stars/bashOrchestrationProgram/
then output streams ( using Bash )
to a file that is said to be processed
"""

# Latitude is given as an angular measurement ( in this program Radians )
# with 0 at the equator, ranging from -pi/2 south to pi/2 north

# Longitude is given as an angular measurement
# with 0 at the Prime Meridian, ranging from −pi westward to +pi eastward

#twotuple is [latitude, longitude]; array choice is reverse-order not array itself

"""
1.
test projections with GMT land/ocean latitude,longitude data on Processing visualization
use a stream
send 2d-array of x,y from projection P to Processing using streams

find bounds for each of the projections for scaling in Processing
"""

#standard array will be an xArray, all data CDS and in 2),3)
standardArrayStr = [[]]
standardArrayVals = [[]]

#the header rows with ( dataType and dataUnits ) are done manually

# for row name completion, I need to know all possible data types:
# row[0] names for NOAA_ele and base: provider,time,name, lat, long, x_equ, y_equ, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, map_val
# row[1] names for units: str,yearmonthday, str, degreesRot, degreesRot, float, float, float, float, float, float, binary
# row[2:] vals for NOAA_ele: NOAA_ele, 20000101, map, someLambda, somePhi, somex, somey, somex, somey, somex, somey, 0or1
# column [0 to 12] correspond to NOAA_ele
NOAA_ele_row =[[ "provider", "time", "name", "lat", "long", "x_mer", "y_mer", "x_rob", "x_rob", "y_rob", "x_gall", "y_gall"
, "map_val"],["str","yearmonthday","str","degrees90","degrees90","float","float","float","float","float","float","bin"]]

CIs = {"lat":0, "long":1, "x_equ":2, "y_equ":3, "x_mer":4, "y_mer":5,
"x_rob":6, "y_rob":7, "x_gall":8, "y_gall":9 }

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

def main():
    return
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

def streamSend():
    #flush when it completely fills
    print("w")

    return

def latLongToAllEntries(array): # 0 1 2 are str entries, 0 1; 2 3, 4 5, 6 7, 8 9;
    for i in range(0,4): # x coordinates from long
        array[:,2*i+2] = array[:,CIs["long"]]

    for i in range(0,4): # y coordinates from lat
        array[:,2*i+3] = array[:,CIs["lat"]]

def equiArray(array):
    scaleCoords(array,0,-180,180,CIs["x_equ"],2160,1080)
    scaleCoords(array, 1, -90, 90, CIs["y_equ"], 2160, 1080)

def mercatorArray(array):
    array[:,CIs["x_mer"]] = array[:,CIs["x_mer"]]
    array[:,CIs["y_mer"]] = ln(approxTan(math.pi/4+array[:,CIs["y_mer"]]/2,0))

    scaleCoords(array, 0, -180, 180, CIs["x_mer"], 2160, 1080)
    scaleCoords(array, 1, -90, 90, CIs["y_mer"], 2160, 1080)

# only approximates -pi/2 <= x <= pi/2, using Pade Approximants (3/2) of tan(x)
def approxTan(valueArray, degreesORradian):
    if(degreesORradian == 0): # does tan for degree values:
        valueArray = valueArray / radToDeg
        valueArray = (valueArray) * (15 - np.power(valueArray, 2)) / (15 - 6 * np.power(valueArray, 2))

    else: # does tan for radian values:
        valueArray = (valueArray) * (15 - np.power(valueArray, 2)) / (15 - 6 * np.power(valueArray, 2))
    return valueArray

# close function takes an array of values any values above the upper bound are made the upper bound
# and any values below the lower bound are made the lower bound

# function already exists, close is a better name

def close(array,lowerBound,upperBound):
    np.clip(array,lowerBound,upperBound)
    return array

# numpy function call for natural log direct
def ln(array):
    array = np.log(array)/np.log(math.e)
    return array

def robinsonArray(array): #robinson could be problematic for millions of values, may be omitted
    # lookup table may become a continous interpolated math function using Neville's or some other algorithmn to 18

    # R_x(lambda) = value, R_y(lambda) = value ( 0 <= lambda <= 90 )
    # derivation of R_x and R_y from lookup table written in this function
    rLF_valuesX = robinsonLookupFunction(array[:,CIs["y_rob"]],0)
    rLF_valuesY = robinsonLookupFunction(array[:,CIs["y_rob"]],1)

    array[:,CIs["x_rob"]] = 0.8487* rLF_valuesX*array[:,CIs["x_rob"]]
    array[:, CIs["y_rob"]] = 1.3523 * rLF_valuesY

    scaleCoords(array,0, -0.8487*math.pi,0.8487*math.pi, CIs["x_rob"], 2160,1080)
    scaleCoords(array, 1, -1.3523, 1.3523, CIs["y_rob"], 2160, 1080)

def robinsonLookupFunction(array, XY):
    # you can plot the lookup table on Desmos, then use a basic interpolation that only interpolates between the
    # the end points and a midpoint that is where you define curvature

    # visual interpolation guesswork is fine and does not need to satisfy numerical conditions, only visual conditions
    # because the projection is a visual ( though projections can/do satisfy some property conditions )

    # variables can be compressed to sign, values; it would be harder to read

    values = None

    # cubic interpolation ( hermite using gaussian reduction )
    # get polynomial from wolframalpha and using desmos https://www.desmos.com/calculator/lsm8z5su1m
    # to get k value (curvature around specified points ( only one point to curve around in both X and Y))
    # for X lookup table, ( endpoints and point ( (65+60)/2, (0.7903+0.7346)/2 )
    # in wolframalpha, gaussian elimination {{0,0,0,1,0},{62.5^3,62.5^2,62.5,1,0.76245},{90^3,90^2,90,1,1},{6*62.5,2,0,0,k}}
    # to get polynomial with k_x = -0.00012, n_x = (4.6176 * 10^(-11))
    # P_X(lambda) = a_x*x^3 + b_x*x^2 + c_x*x
    # where a_x=n_x*(309375000*k_x+24482), b_x=n_x*(-47179687500*k_x-4590375), c_x = n_x*(1740234375000k_x+455454550)
    # P_x(lambda) with coefficients = -5.83803168*10^(-7)*x^(3) + 4.9463154*10^(-5)*x^(2) + 1.13882218008*10^(-2)*x

    if(XY == 0):
        sign_x = np.sign(array[:,CIs["x_rob"]])
        x_values = np.abs(array[:,CIs["x_rob"]])
        x_values = (-5.83803168*10^(-7))*(x_values)^3 + (4.9463154*10^(-5))*(x_values)^(2) + (1.13882218008*10^(-2))*(x_values)
        values = x_values * sign_x

    # for Y lookup table ( endpoints and point (0,1),(32.5,0.95135),(90,0.5322))
    # in wolframalpha, gaussian elimination:
    # gaussian elimination {{0,0,0,1,1},{32.5^3,32.5^2,32.5,1,0.95135},{90^3,90^2,90,1,0.5322},{6*32.5,2,0,0,k}}
    # to get polynomial with k_y = -0.000135, n_y = ( 1.48644 * 10^(-9) )
    # P_Y(lambda) = a_y*x^3 + b_y*x^2 + c_y*x
    # where a_y=n_y*(-13455000*k_y-1732), b_y=n_y*(1648237500*k_y+168870), c_y = n_y*(-39355875000*k_y-4665905)
    # P_Y(lambda) with coefficients = 1.25492697*10^(-7)*(x)^3 + -7.97357073825*10^(-5)*(x)^(2) + 9.61931994525*10^(-4)*(x) + 1

    if(XY == 1):
        sign_y = np.sign(array[:,CIs["y_rob"]])
        y_values = array[:,CIs["y_rob"]]
        y_values = (1.25492697*10^(-7))*(y_values)^3 + (-7.97357073825*10^(-5))*(y_values)^(2) + (9.61931994525*10^(-4))*(y_values) + 1
        values = y_values * sign_y

    return values

def gallpetersArray(array):
    #X gall-peters to change
    scaleCoords(array,0, 0, 360, CIs["y_gall"],2160,1080)

    #Y gall-peters to change
    array[:,CIs["y_gall"]] = 2*math.sin( array[:,CIs["y_gall"]]*(radToDeg) )
    scaleCoords(array, 0, -2, 2, CIs["y_gall"],2160,1080)

if __name__ == "__main__":
    main()

