from t1_function import approxTan, close, radToDeg
import math
import numpy as np

CIs = {"lat":0, "long":1, "y_equ":2, "x_equ":3, "y_mer":4, "x_mer":5,
"y_rob":6, "x_rob":7, "y_gall":8, "x_gall":9 }
# y_rob is 9 in series, # x_rob is 10 in series

resolutionY = 540
resolutionX = 1080

def latLongToProjectionSet(array): #changes all lat,long values into corresponding x,y projections from paste
    latLongToAllProj(array)
    gallpetersArray(array)
    robinsonArray(array)
    mercatorArray(array)
    equiArray(array)

    #return array4

def latLongToAllProj(array): #pastes lat,long into corresponding projection x,y's
    for i in range(0,4):
        array[:,i*2+2] = array[:,0]
    for i in range(0,4):
        array[:, i*2+3] = array[:,1]

# both equiRectToLatLong latLongToProjectionSet take numpy arrays or python arrays
def equirectToLatLong(array,width,height): # turns equirectangular x,y into lat long
    array[:,1] = (((array[:,3]-(width/2))*2*math.pi)/width)*radToDeg # conversion on a column for longitude
    array[:,0] = (((array[:,2]-(height/2))*math.pi)/height)*radToDeg # conversion on a column for latitude

    return array

def equiArray(array): # takes lat long and turns into corresponding equirectangular projection x,y
    #scaleCoords(array,0,-180,180,CIs["x_equ"],2160,1080)
    #scaleCoords(array, 1, -90, 90, CIs["y_equ"], 2160, 1080)

    scaleCoordsXorY(array, -180, 180, CIs["x_equ"], resolutionX)
    scaleCoordsXorY(array, -90, 90, CIs["y_equ"], resolutionY)

def mercatorArray(array): # takes lat long and turns into corresponding mercator projection x,y

    array[:,CIs["x_mer"]] = array[:,CIs["x_mer"]]

    sign = np.sign(approxTan(math.pi / 4 + array[:, CIs["y_mer"]] / 2, 0))

    array[:,CIs["y_mer"]] = np.log(np.abs(approxTan(math.pi/4+array[:,CIs["y_mer"]]/2,0)))
    # ln(tan(x)) is real for x that is negative on Desmos, numpy natural log does not take negative values
    # use sign on array trick
    array[:,CIs["y_mer"]] = array[:,CIs["y_mer"]] * sign
    #array[:,CIs["y_mer"]] = close(array[:,CIs["y_mer"]],-5.2,5.2)

    #print("mer_y_x", array[:,CIs["y_mer"]], array[:,CIs["x_mer"]], np.max(array[:,CIs["y_mer"]]), np.min(array[:,CIs["y_mer"]]))
    yUpper = np.max(array[:,CIs["y_mer"]])
    yLower = np.min(array[:,CIs["y_mer"]])
    #finds lower and upper bounds for scale to coordinates ( -7, 6 ) --> ( 0, 1080

    #scaleCoords(array, 0, -180, 180, CIs["x_mer"], 2160, 1080)
    scaleCoordsXorY(array, -180, 180, CIs["x_mer"], resolutionX)
    scaleCoordsXorY(array, yLower, yUpper, CIs["y_mer"], resolutionY)
    #scaleCoords(array, 1, -90, 90, CIs["y_mer"], 2160, 1080)


def robinsonArray(array): #robinson could be problematic for millions of values, may be omitted
    # lookup table may become a continous interpolated math function using Neville's or some other algorithmn to 18

    # R_x(lambda) = value, R_y(lambda) = value ( 0 <= lambda <= 90 )
    # derivation of R_x and R_y from lookup table written in this function

    #print(array[:,CIs["x_rob"]], array[:,CIs["y_rob"]])

    rLF_valuesX = robinsonLookupFunction(array[:,CIs["y_rob"]],0)
    rLF_valuesY = robinsonLookupFunction(array[:,CIs["y_rob"]],1)

    #print(rLF_valuesX, rLF_valuesY)
    #print(array[:,CIs["x_rob"]])
    array[:,CIs["x_rob"]] = array[:,CIs["x_rob"]] / radToDeg
    #print(array[:,CIs["x_rob"]])

    array[:,CIs["x_rob"]] = 0.8487 * rLF_valuesX * array[:,CIs["x_rob"]]
    array[:, CIs["y_rob"]] = 1.3523 * rLF_valuesY

    xLower = np.min(array[:,CIs["x_rob"]])
    xUpper = np.max(array[:,CIs["x_rob"]])
    yLower = np.min(array[:,CIs["y_rob"]])
    yUpper = np.max(array[:,CIs["y_rob"]])

    #print(array[:,CIs["y_rob"]], array[:,CIs["x_rob"]])

    scaleCoordsXorY(array, yLower, yUpper, CIs["y_rob"], resolutionY)
    scaleCoordsXorY(array, xLower, xUpper, CIs["x_rob"], resolutionX)

    #scaleCoords(array,0, -9.128904, 0, CIs["x_rob"], 2160,1080)
    #scaleCoords(array, 1, -1.3523, 1.3523, CIs["y_rob"], 2160, 1080)

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
        #print(array)
        sign_x = np.sign(array[:])
        x_values = np.abs(array[:])
        x_values = -5.83803168/np.power(10,7)*np.power(x_values,3)
        x_values = x_values + 4.9463154/np.power(10,5)*np.power(x_values,2)
        x_values = x_values + 1.13882218008/np.power(10,2)*np.power(x_values,1)
        values = x_values * sign_x


    # for Y lookup table ( endpoints and point (0,1),(32.5,0.95135),(90,0.5322))
    # in wolframalpha, gaussian elimination:
    # gaussian elimination {{0,0,0,1,1},{32.5^3,32.5^2,32.5,1,0.95135},{90^3,90^2,90,1,0.5322},{6*32.5,2,0,0,k}}
    # to get polynomial with k_y = -0.000135, n_y = ( 1.48644 * 10^(-9) )
    # P_Y(lambda) = a_y*x^3 + b_y*x^2 + c_y*x
    # where a_y=n_y*(-13455000*k_y-1732), b_y=n_y*(1648237500*k_y+168870), c_y = n_y*(-39355875000*k_y-4665905)
    # P_Y(lambda) with coefficients = 1.25492697*10^(-7)*(x)^3 + -7.97357073825*10^(-5)*(x)^(2) + 9.61931994525*10^(-4)*(x) + 1

    if(XY == 1):
        sign_y = np.sign(array[:])
        y_values = np.abs(array[:])
        y_values = 1.25492697/np.power(10,7)*np.power(y_values,3)
        y_values = y_values + -7.97357073825/np.power(10,5)*np.power(y_values,2)
        y_values = y_values + 9.61931994525/np.power(10,4)*np.power(y_values,1)
        values = y_values * sign_y

    return values

def gallpetersArray(array):
    #X gall-peters to change
    #print(array.shape)
    #scaleCoords(array,0, -90, 90, CIs["y_gall"],2160,1080)
    #print(array.shape)
    #Y gall-peters to change
    #print(array[:,CIs["y_gall"]], np.min(array[:,CIs["y_gall"]]), np.max(array[:,CIs["y_gall"]]))

    array[:,CIs["y_gall"]] = 2*np.sin( array[:,CIs["y_gall"]]*(radToDeg) )
    #scaleCoords(array, 0, -180, 180, CIs["y_gall"],2160,1080)

    scaleCoordsXorY(array, -2, 2, CIs["y_gall"], resolutionY)
    scaleCoordsXorY(array, -180, 180, CIs["x_gall"], resolutionX)

#converts from ( -t units <= a ) a'unit to a'degrees celsius ( celsius is standard ) ( -273 c <= a )
def standardizeTemp(array,CKFin,columnIndex):

    # celsius to celsius
    if(CKFin == 0):
        return

    # kelvin to celsius
    if(CKFin == 1):
        array[:,columnIndex] = array[:,columnIndex] - 273.15

    # fahrenheit to celsius
    if(CKFin == 2):
        array[:,columnIndex] = ( array[:,columnIndex] - 32 ) * (5/9)



#converts from a <= x <= b to -180 <= x <= 180
#converts from c <= y <= d to -90 <= y <= 90
#where a,b is equivalent to lowerX, upperX; where c,d is equivalent to lowerY, upperY

def standardizeCoordinates(array,lowerB,upperB,columnIndex,latLongIndex):

    midpoint = (lowerB+upperB)/2
    scale = abs(lowerB) + abs(upperB)

    array[:,columnIndex] = (array[:,columnIndex] - midpoint)
    if(latLongIndex == 0):
        array[:,columnIndex] = (array[:,columnIndex]*180)/scale
    else:
        array[:, columnIndex] = (array[:, columnIndex] * 360) / scale

    return array

# scales post-projection latlong coordinates to displayable coordinates ( [0,resolutionX], [0,resolutionY] )
def scaleCoords(array,XY,lowerB,upperB,columnIndex,resolutionX,resolutionY):

    midpoint = (lowerB + upperB) / 2
    scale = abs(lowerB) + abs(upperB)

    array[:,columnIndex] = (array[:,columnIndex] - midpoint)
    if(XY == 0):
        array[:,columnIndex] = (array[:,columnIndex] * resolutionX)/scale
    if(XY == 1):
        array[:,columnIndex] = (array[:,columnIndex] * resolutionY)/scale

def scaleCoordsXorY(array,lowerB,upperB,columnIndex,newResolution):

    array[:,columnIndex] = array[:,columnIndex] - lowerB
    array[:,columnIndex] = array[:,columnIndex] * newResolution / (upperB - lowerB )


def convertDegRad(array,toDegOrRad):

    if(toDegOrRad == 0): #to degrees
        array = array / radToDeg
    if(toDegOrRad == 1): #to radians
        array = array * radToDeg