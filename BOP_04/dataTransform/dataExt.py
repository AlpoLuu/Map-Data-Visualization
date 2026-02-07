import dataMain
import math
import struct
import numpy as np

# data extract is exclusively for 2); remote cloud, cloud APIs, data streams; all data that is extracted as files
# is done in dataFile


def main():
    return


def NOAA_buoy(): #NOAA
    dataArray = [[]]

    return dataArray

def NOAA_weather(): #NOAA
    dataArray = [[]]
    return dataArray

def OWM(): #OpenWeatherMap API
    dataArray = [[]]
    return dataArray

def ISS(): #International Space Station location, math done in here for re-positioning on a map
    dataArray = [[]]
    return dataArray

def NASA(): #
    dataArray = [[]]
    return dataArray

#USGS National Earthquake Center
#can grab many event types, only grabbing Earthquakes on https://earthquake.usgs.gov/fdsnws/event/1/
# refer to https://www.fdsn.org/webservices/FDSN-WS-Specifications-1.0.pdf for using the web service
# uses GeoJSON format for automated applications, for GeoJSON look at https://datatracker.ietf.org/doc/html/rfc7946
# based on javascript and object notation
# will have to convert GeoJSON to array through process convertA

# curl "https://earthquake.usgs.gov/fdsnws/event/1/[METHOD[?PARAMETERS]] "

def USGS():

    dataArray = [[]]

    return dataArray


    
if __name__ == "__main__":
    main()
