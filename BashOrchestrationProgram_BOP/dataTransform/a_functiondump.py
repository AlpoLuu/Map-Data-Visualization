
""" Old Function for robinsonX lookup table
def robinsonX(latitude):
    lookVal = 0

    #check longitude between every sequential value in 1st column, for loop through rows
    #if is between, in that row --> set lookVal to linear interpolation of value above
    # define a function with line intercept y =
    for i in range(1, 19):
        print(robinsonLT[i+1][0], robinsonLT[i][0])

    for i in range(1,19):
        #if ( latitude >= robinsonLT[0][i] and latitude <= robinsonLT[0][i+1]):
        #    lookVal = ((robinsonLT[2][i+1]-robinsonLT[2][i])/(robinsonLT[1][i+1]-robinsonLT[1][i]))*(latitude-robinsonLT[1][i])+robinsonLT[2][i]

        if (latitude >= robinsonLT[i][0] and latitude <= robinsonLT[i+1][0]):
            lookVal = ((robinsonLT[i+1][2] - robinsonLT[i][2]) / (robinsonLT[i+1][1] - robinsonLT[i][1])) * (latitude - robinsonLT[i][1]) + robinsonLT[i][1]

    #lookval = (()/())*()+

    return lookVal
"""

""" Old Function for robinsonY lookup table
def robinsonY(latitude):
    lookVal = 0

    # check longitude between every sequential value in 1st column, for loop through rows
    # if is between, in that row --> set lookVal to linear interpolation of value above
    # define a function with line intercept y =

    for i in range(1, 19):
        #if (latitude >= robinsonLT[0][i] and latitude <= robinsonLT[0][i + 1]):
        #    lookVal = ((robinsonLT[1][i + 1] - robinsonLT[1][i]) / (robinsonLT[2][i + 1] - robinsonLT[2][i])) * (latitude - robinsonLT[2][i]) + robinsonLT[1][i]
        if (latitude >= robinsonLT[i][0] and latitude <= robinsonLT[i+1][0]):
            lookVal = ((robinsonLT[i+1][1] - robinsonLT[i][1]) / (robinsonLT[i+1][2] - robinsonLT[i][2])) * (latitude - robinsonLT[i][2]) + robinsonLT[i][2]

    # lookval = (()/())*()+

    return lookVal
    return
"""