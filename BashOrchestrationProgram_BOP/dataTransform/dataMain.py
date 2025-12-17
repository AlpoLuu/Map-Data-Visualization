import math
import sys
import numpy
import csv

from mpmath import ln

"""
standardized 2d array for data
columns: lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val, temp,
Only fully do-able after going through file types

GMT test
columns: lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val 


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

with open('/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/robinsonTable.csv', 'r') as f:
    reader = csv.reader(f)
    rLT = list(reader) #reads CSV turns to str-2d-array

def main():

    print(rLT) #takes str-2d-array into float-2d-array
    for k in range(0,3):
        for i in range(1,19):
            rLT[i][k] = float(rLT[i][k])

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

