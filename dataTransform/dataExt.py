import dataMain
import math
import struct
import numpy as np


# file reader for the NOAA_elevation megafile ( which contains the 16 subfiles in grid->linear format in octet stream)
# as 16-bit signed integers
# to read 4 characters into an array
# optimizations: numpy operations, numpy arrays, 16-bit signed int to 8-bit unsigned file, spaced compression

#NOAA_elevation
NOAA_elevationArray = np.zeros((401760000, 3), dtype=np.int32)

with open('/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/16megafile_mask', 'rb') as f:
    NOAA_elePosX = 0
    NOAA_elePosY = 0
    NOAA_eleCurPosY = 0
    NOAA_caseType = 0

    i = -1

    while chunk := f.read(2):  # 2 bytes = 16 bits

        mapEleVal = struct.unpack('>h', chunk)[0]  # 'h' = signed short (16-bit)

        NOAA_elevationArray[i+1]=([mapEleVal, NOAA_elePosX%10800, (NOAA_elePosY-NOAA_eleCurPosY)%(4800+NOAA_caseType*1200)])
        #NOAA_elePosX += 1
        np.add(NOAA_elePosX, 1, out=NOAA_elePosX)

        #print(NOAA_elePosX, i, NOAA_elePosY, NOAA_caseType)

        print(NOAA_elePosX, NOAA_elePosY)

        # 0, 1, 2, 3, 12, 13, 14, 15, 16 is caseType = 0
        # 4, 5, 6, 7, 8, 9, 10, 11 is caseType = 1

        if(NOAA_elePosX%10800 == 0 and NOAA_elePosY%(4800+1200*NOAA_caseType) == 0): #check for file-type to read
            NOAA_eleCurPosY = NOAA_elePosY

            #i += 1, np in-place operations don't create an intermediate array
            np.add(i, 1, out=i)

            if( i >= 4 and i < 12):
                NOAA_caseType = 1
            else:
                NOAA_caseType = 0

        if (NOAA_elePosX % 10800 == 0):
            NOAA_elePosY += 1


def main(): #for test running and checking what's inside an array
    #array1 = NOAA_elevation(NOAA_elevationArray)
    #print(array1[0], array1[1], array1[2])
    return

#NOAA elevation extraction method
#all the math for data into array
#files concatenated into one mega file, Xfile which is used in data
# make posA(x,y) offsets then depending on .OS9a, .OS9b


def NOAA_elevation(dataArray):
    presetArray = [[]]
    entries = []*9
    entries[0] = "map"
    #data.x and data.y come from file pos
    xPos = 0
    yPos = 0



    caseType = 0 #either 4800 or 6000 in cases when 0 or 1 respectively, use mod_4(index) for longitude

    positionArray = [] * 16
    #case for ?0S9a ( 10800 x 4800 ) ( file type name is a placeholder )
    #4 for loops is slightly computationaly better, while using yBound and modulus is cleaner code
    for i in (0,4):
        positionArray[i] = [0+i*10800,0]
    for i in (12,16):
        positionArray[i] = [0+i*10800,16800]

    #case for ?0S9b ( 10800 x 6000 ) ( file type name is a placeholder
    for i in (4,8):
        positionArray[i] = [0+i*10800,4800]
    for i in (8,12):
        positionArray[i] = [0+i*10800,10800]

    #
    """
    for k in (0,16):
        #k % 4 gives the horizontal position
        #floor(k/(k % 4)) gives the vertical position
        # this is for going from a 2d-array to a 1d-array, or encoding from a 2d to 1d; it's already 1d

        if(k >= 4 and k < 11):
            caseType = 1
        else:
            caseType = 0

        #case .OS9a
        for i in range (0, 10800):
            for j in range (0,4800+caseType*1200):
                entries[2] = (( NOAA_elevationArray[1][w] + positionArray[0][k] - 21600)/43200)*math.pi
                entries[1] = (( NOAA_elevationArray[2][w] + positionArray[1][k] - 10800)/21600)*(math.pi/2)
                entries[9] = NOAA_elevationArray[0][w]

                presetArray.append(entries)
    """
    posGridIn = -1  #what grid the index i of elevationArray is in
    posType = 0 #what grid type the index i of elevation array is in, start with grid A grid type
    #curPosIndexInArray = 0 #current grid first position in elevation array

    for i in range(0,43200*21600):

        if( i%(10800*(4800+posType*1200) == 0 )):
            posGridIn =+ 1
            if( posGridIn >= 4 and posGridIn < 12):
                posType = 1
            else:
                posType = 0
                
        entries[2] = (( dataArray[1][i] + positionArray[0][posType] - 21600)/43200)*math.pi
        entries[1] = (( dataArray[2][i] + positionArray[1][posType] - 10800)/21600)*(math.pi/2)
        if( dataArray[0][i] == 3326):
            entries[9] = 0
        else:
            entries[9] = 1

        presetArray.append(entries)

        #a is just data.
                #data.currentByte to entries[9]
        #case .0S9b
    #yBound and modulus approach
    """
    for i in (0,16):
        if(i >= 4 and i < 11):
            yBound = 1
        else:
            yBound = 0


        if
    """

    # sets equirectangular projection back to lat long back into mercator, robinson and gall-peters
    return presetArray



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
