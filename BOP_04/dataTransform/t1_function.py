import numpy as np
import math

radToDeg = (360)/(2*math.pi)
eulerNum = 2.718281828459045

def eat(x,y):
    if(x >= y):
        return x
    else:
        return y

def splitByte(value, lengthOfSplit):
    valuesSplit = []

    valuesSplit.append(list(value))


    return valuesSplit

def splitInt(value, lengthOfSplit): #only works for positive integers as of right now
    valueSplit = []

    return valueSplit

def signZero(number):
    if number < 0:
        return -1
    if number == 0:
        return 1
    if number > 0:
        return 1

# only approximates -pi/2 <= x <= pi/2, using Pade Approximants (5/4) of tan(x)
def approxTan(valueArray, degreesORradian):
    if(degreesORradian == 0): # does tan for degree values:
        valueArray = valueArray / radToDeg
        valueArray = ( (valueArray) * (105 - 10*np.power(valueArray, 2)) )/ (105 - 45 * np.power(valueArray, 2) + np.power(valueArray, 4))

    else: # does tan for radian values:
        valueArray = ( (valueArray) * (105 - 10*np.power(valueArray, 2)) )/ (105 - 45 * np.power(valueArray, 2) + np.power(valueArray, 4))
    return valueArray

# close function takes an array of values any values above the upper bound are made the upper bound
# and any values below the lower bound are made the lower bound

# function already exists, close is a better name

def close(array,lowerBound,upperBound):
    np.clip(array,lowerBound,upperBound)
    return array

# numpy function call for natural log direct
