"""
grab the 3 datasets to get an archived files for initial testing

with live data, grab with .py then standardize the stream for use

update processing every based on data stream

-----

This is where data will be taken from the extract then optimized for data stream ( sys.stdout and sys.stderr)

"""

import subprocess
import sys
import dataMain

#archived
#cyclic, realtime
#global, sector, point

    #Do I have to set block buffer? Yes, maybe. IO is FIFO
    

extractProc = {
    #archived
    "GMT": "1", #GMT Remote Data, cached locally
        #changed to NOAA_OAA

    "CDS": "2", #Copernicus Climate Data Store (CDS), needs API key
    #"NASA": "3", #needs an Earthdata account to access data

    #cyclic + realtime
    "USGS": "4", #USGS Earth Center
    "NOAA_buoy": "5", #NOAA buoy observations ( US-sector, cyclic-01h )
    "NOAA_weather": "6", #NOAA weather observations ( US-sector, cyclic-01h )
    "OWM": "7", #OpenWeatherMap API ( point;city, realtime for a point, 15 major cities to cycle )
    "ISS": "8", #ISS-position ( global;moving station, realtime )
    "NASA_EON": "9", #NASA_E ( global;occurence, realtime, major natural events )

    #big data set
    "OSN": "10", #OpenSkyNetwork ( global;planes, realtime, plane movements )
    
    #biggest data set from Claude, 100gb/run: how do I compress/parse through the data set?
    "GFS": "11" #Global Forecast Service ( global, cyclic, weather )
        #cull to 1/1000 using compression, iterate through data and only grab every 1000 point
}


dataSets = [[]]

    #partition using 2d-lists in Python
    #make a big 2d array after

    #how do we stream this? 6 streams, 2 streams of different types of information (cyclic, realtime), 1 stream
    #1 stream, then just have some way to see what data is what

    #it seems that 2 streams cyclic and realtime is best
        #anonymous pipe, then 2 named pipes "cyclic and realtime"

def main():

    print("w")
    #print(sys.platform)
    #print(sys.version)
    #grabbing is just extracting

def extract(particularProcess): # not needed can just grab standardized array from dataMain
    match particularProcess:
        case 1: # for each case, extract format turn into an array
            print("w")

        case _:
            pass


def standardizeData(arrayOfData): # not needed can just grab standardized array from dataMain
    print("w")
    #apparently, you're supposed to partition this data using SQL or something though I won't be doing that

# systemOutManage method
# function to manage input ( data )
# where data is the standardized array from dataMain.py
# is where actions sys.stdout, sys.stderr will be done

def systemOutManage(input):
    print("w")



if __name__ == "__main__":
    main()