import math
import sys
import numpy
import csv
import dataExt

from mpmath import ln

"""
standardized 2d array for data
columns: lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val, temp,
Only fully do-able after going through file types

OTD test
columns: lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val 

Geospatial data is raster not vector

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

standardArray = [[]]

# for row name completion, I need to know all possible data types:
# row[0] names for NOAA_OAA and base: positionName, lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, map_val
# row[1] names for units: str, rad, rad, float, float, float, float, float, float, binary

# row[0],2 names for CDS

# row process for NOAA_elevation ( flatten to earth mask )
# refer to https://www.ngdc.noaa.gov/mgg/topo/gltiles.html
# set startPosA, startPosB, . . . . startPosP

# row names for CDS (Climate Data Store) :
    #files are from https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview
    #data is in either .grib or .NETCDF ( must be downloaded using the python earthkit module or through web API )
        #.grib has a header, and is stored in binary; it seems as though .NETCDF is what you want
        #1 Used WEB-API for file, CDS and OTD are easy to access for testing, then cloud/remote access is done using

        #2 curling https, api requests and cloud for USGS, NOAA_buoy, NOAA_w, OWM, NASA, ISS
        # ( the main actings otherwise )

        #3 big data is OSN ( for tracking all airplanes ); all of this would be much easier if I had a database
        # language like SQL; I use 2d-arrays, python and matrix concepts

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

with open('/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/robinsonTable.csv', 'r') as f:
    reader = csv.reader(f)
    rLT = list(reader) #reads CSV turns to str-2d-array

#hex

def main():

    print(rLT) #takes str-2d-array into float-2d-array
    for k in range(0,3):
        for i in range(1,19):
            rLT[i][k] = float(rLT[i][k])

    #test run for NOAA elevation array

    #print(robinsonLT) #Check if 2d array went from str to float

    #print("\n" + robinsonLT[1][0] )
    #print(sys.platform)
    #print(sys.version)
    print(robinson([math.pi/4,math.pi/2])) #testing values

#flush needs a good conditional for block buffer; either append a marker line or have manual check for flush
#block buffer send, just flush whenever it fills

def preproData(streamData):
    #latitude and longitude into mercator, robinson and gall-peters 2 -> 6 columns

    # 4 new columns or preserve latitude/longitude for processing?
    # 4 new columns

    # 6 new columns
    print("w")

def mapHexaValToMask(hexaVal):
    if(hexaVal > hex("3326")):
        hexaVal = 1
    else:
        hexaVal = 0
    return hexaVal

def streamSend():
    #flush when it completely fills
    print("w")

def mercator(twoTuple):
    twoTuple[0] = twoTuple[0]
    twoTuple[1] = numpy.ln(math.tan(math.pi/4 + twoTuple[1]/2))

    return twoTuple

def robinson(twoTuple):
        #Blindly trusted Claude for the robinson formula
    #twoTuple[0] = robinsonX(twoTuple[1])*twoTuple[0]*0.8487
    #twoTuple[1] = robinsonY(twoTuple[1])*signZero(twoTuple[1])*1.3523

    newTuple = [0,0]

    newTuple[0] = robinsonX(twoTuple[0])*twoTuple[1] # X ( latitude ) * longitude
    newTuple[1] = robinsonY(twoTuple[0])

    return newTuple

def robinsonX(latitude): # x in x = 0.8487 * X * latitude
    valX = 0
    triTuple = [0, 0, 0]

    for i in range(0, 18):
        if (rLT[i + 1][2] < latitude and rLT[i + 1][2] >= latitude):
            triTuple = [latitude, rLT[i + 1][2], rLT[i + 1][2]]
            valX = 0.8487 * tableInterp[triTuple, 0]

    return valX

def robinsonY(latitude): # y in y = 1.3523 * Y
    valY = 0
    triTuple = [0,0,0]

    for i in range(0,18):
        if(rLT[i+1][2] < latitude and rLT[i+1][2] >= latitude):
            triTuple = [latitude,rLT[i+1][2],rLT[i+1][2]]
            valY = 1.3523 * tableInterp[triTuple,1]

    return valY

def tableInterp(triTuple,XorY): #X or Y function on Robinson projection
    #lookup table interpolation for robinsonX and robinsonY
    #either Atiken interpolation or Hermite interpolation from Robinson Projection Wikipedia
    #Atiken interpolation is similar to Neville's algorithmn, so I will use Neville's algorithmn

    #triTuple = [latitude, less than index, more than index] = [ lambda, l_i, m_i ]

    lookVal = (triTuple[0] - triTuple[1])*rLT[1+triTuple[2]][XorY+1]
    lookVal = lookVal - (triTuple[0] - triTuple[2])*rLT[1+triTuple[1]][XorY+1]
    lookVal = lookVal / ( triTuple[1] - triTuple[0] )

    return lookVal

def gallpeters(twoTuple):
    twoTuple[0] = twoTuple[0]
    twoTuple[1] = 2*(math.sin(twoTuple))

    return twoTuple

def signZero(number):
    if number < 0:
        return -1
    if number == 0:
        return 1
    if number > 0:
        return 1

if __name__ == "__main__":
    main()

