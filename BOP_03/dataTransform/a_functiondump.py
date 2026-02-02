
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


"""
Tried to read a 1.6 gb raw octet stream, 16-bit signed integers using python only
will implement numpy array
mask the original file

# file reader for the NOAA_elevation megafile ( which contains the 16 subfiles in grid->linear format in octet stream)
# as 16-bit signed integers
# to read 4 characters into an array

#NOAA_elevation
NOAA_elevationArray = np.zeros((401760000, 3), dtype=np.int32)

with open('/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/16megafile', 'rb') as f:
    NOAA_elePosX = 0
    NOAA_elePosY = 0
    NOAA_eleCurPosY = 0
    NOAA_caseType = 0

    i = -1

    while chunk := f.read(2):  # 2 bytes = 16 bits

        mapEleVal = struct.unpack('>h', chunk)[0]  # 'h' = signed short (16-bit)
        NOAA_elevationArray.append([int(mapEleVal), NOAA_elePosX%10800, (NOAA_elePosY-NOAA_eleCurPosY)%(4800+NOAA_caseType*1200)])
        NOAA_elePosX += 1

        #print(NOAA_elePosX, i, NOAA_elePosY, NOAA_caseType)
        if(i == 8):
            print("halfway")

        # 0, 1, 2, 3, 12, 13, 14, 15, 16 is caseType = 0
        # 4, 5, 6, 7, 8, 9, 10, 11 is caseType = 1

        if(NOAA_elePosX%10800 == 0 and NOAA_elePosY%(4800+1200*NOAA_caseType) == 0): #check for file-type to read
            NOAA_eleCurPosY = NOAA_elePosY

            i += 1
            if( i >= 4 and i < 12):
                NOAA_caseType = 1
            else:
                NOAA_caseType = 0
                
        if (NOAA_elePosX % 10800 == 0):
            NOAA_elePosY += 1
"""

""" Old Major Vote Downscale for unformatted file still in [[A,B,C,D], . . . . [M, N, O, P]]
def fileMajorVoteDownscale(height,width,scaleAmount):
    input_path = '/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/'
    output_path = '/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/'

    placeholderArray = np.zeros((scaleAmount*scaleAmount), dtype=np.uint8)
    writeCursor = [] #in file writing to, arithmetic for position is done in writeCursor

    megafile_mask = open(input_path, 'rb')
    megafile_mask_majorvote = open(output_path,'wb')

    block_size = scaleAmount

    row_bytes = width * 1 # you can multiply by how many "bytes per pixel"
    block_rows_bytes = row_bytes * block_size

    #megafile_mask_majorvote.seek(50, 0) # go to byte 50 from start
    #megafile_mask_majorvote.seek(200, 1) # jump 200 bytes from current position

    columnPos = 0
    for i in range(0,int(43200*21600/(scaleAmount*scaleAmount))):

        megafile_mask_majorvote.seek(0,0)

        megafile_mask_majorvote.write(majorityVote(read_block(megafile_mask, writeCursor,2)))

    absOffset = 0
"""

""" Old function for downsampling using majority vote
def majorVoteDownscale(height,width,scaleAmount): # scale amount is expressed in 1/(scaleAmount), make sure scaleamount divides
    #data amount in data set
    mask_mm = np.fromfile('/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/megafile_mask', dtype=np.uint8)

    majorityVoteFileArr = np.zeros((int(height/scaleAmount), int(width/scaleAmount)), dtype=np.uint8)

    mask_mm = np.reshape(mask_mm,(height, width)) #reshapes 1d array into a 2d array with width 43200, height 21600 then returns it
    mask_mm = np.reshape(mask_mm, (int(height/scaleAmount),scaleAmount,int(width/scaleAmount),scaleAmount)) #reshapes into a 3d array with
    #blocks of scaleAmount x scaleAmount
    mask_mm = np.transpose(mask_mm,(0,2,1,3))
    #print(mask_mm)

    for i in range(0,int(height/scaleAmount)):
        for j in range(0,int(width/scaleAmount)):
            print(i,j)
            block = mask_mm[i, j]
            #print(block)
            majorityVoteFileArr[i, j] = majorityVote([0,1],block)

    majorityVoteFileArr.tofile("/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/megafile_mask_majorvote")
"""

"""
    #print(fileToDownsample.shape)

    #print(fileToDownsample, fileToDownsample.shape)

    count = fileToDownsample[np.newaxis,:] == voteVals[:,np.newaxis]
    print(count, count.shape)
    #count3d = count[np.newaxis]

    #I'm going to turn the entry ( x ) into one by counting which gives the count for both 0 and 1 which becomes
    #the majority vote value

    #countedSwap = np.swapaxes(count, 1, 0)
    counted = (count.sum(axis=0)).T
    print(counted,counted.shape)
        #counted counts the values and gets two lines of sums of 1 or 0 occurences respectively in a block
        #countedSwap makes result function work

    #print(counted,counted.shape)

    result = (counted[1,:] > counted[0,:]).astype(np.uint8)

    print(result,result.shape)

    #counted.resize((14580000,1))
    #counted.reshape(14580000)
"""

""" turning a str array and float array into one big polars array
def arrays_to_polarsArray(arr1, arr2):
    numberOfCols1 = arr1.shape[0]
    numberOfCols2 = arr2.shape[0]

    polarsData = {}

    for i in range(numberOfCols1):
        return
    for i in range(numberOfCols2):
        return
    return polarsData
"""

""" #gallpeters projection for individual lat long ( -pi/2 <= lambda <= pi/2, -pi <= phi <= pi )
def gallpeters(twoTuple):
    twoTuple[0] = twoTuple[0]
    twoTuple[1] = 2*(math.sin(twoTuple))

    return twoTuple
"""

""" data ext, old NOAA elevation reader
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
    
    for i in (0,16):
        if(i >= 4 and i < 11):
            yBound = 1
        else:
            yBound = 0


        if
    

    # sets equirectangular projection back to lat long back into mercator, robinson and gall-peters
    return presetArray
"""

""" does Robinson for a single tuple [lat,long] inefficient when I can use vectorized operations on a column

def tableInterp(triTuple,XorY): #X or Y function on Robinson projection
    #lookup table interpolation for robinsonX and robinsonY
    #either Atiken interpolation or Hermite interpolation from Robinson Projection Wikipedia
    #Atiken interpolation is similar to Neville's algorithmn, so I will use Neville's algorithmn

    #triTuple = [latitude, less than index, more than index] = [ lambda, l_i, m_i ]

    lookVal = (triTuple[0] - triTuple[1])*rLT[1+triTuple[2]][XorY+1]
    lookVal = lookVal - (triTuple[0] - triTuple[2])*rLT[1+triTuple[1]][XorY+1]
    lookVal = lookVal / ( triTuple[1] - triTuple[0] )

    return lookVal
    
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
"""

""" datafile old functions before import chain fixing ( circular reference )
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
"""

""" datamain old functions before circular import fix
def equiArray(array):
    scaleCoords(array,0,-180,180,CIs["x_equ"],2160,1080)
    scaleCoords(array, 1, -90, 90, CIs["y_equ"], 2160, 1080)

def mercatorArray(array):
    array[:,CIs["x_mer"]] = array[:,CIs["x_mer"]]
    array[:,CIs["y_mer"]] = ln(approxTan(math.pi/4+array[:,CIs["y_mer"]]/2,0))
    array[:,CIs("y_mer")] = close(array[:,CIs["y_mer"]],-5.2,5.2)

    scaleCoords(array, 0, -180, 180, CIs["x_mer"], 2160, 1080)
    scaleCoords(array, 1, -90, 90, CIs["y_mer"], 2160, 1080)

# only approximates -pi/2 <= x <= pi/2, using Pade Approximants (5/4) of tan(x)
def approxTan(valueArray, degreesORradian):
    if(degreesORradian == 0): # does tan for degree values:
        valueArray = valueArray / radToDeg
        valueArray = (valueArray) * (105 - 10*np.power(valueArray, 2)) / (105 - 45 * np.power(valueArray, 2) + np.power(valueArray, 4))

    else: # does tan for radian values:
        valueArray = (valueArray) * (105 - 10*np.power(valueArray, 2)) / (105 - 45 * np.power(valueArray, 2) + np.power(valueArray, 4))
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
"""

"""
def stream_archived(arrowTable, requestPipe, writePipe): # used for map
    #polars goes to pyarrow then writes using a custom format specifically for processing

    requestTable = function(arrowTable)
    # the function for this should make
    with open(writePipe, 'wb') as f:
        #writer = ipc.new_stream(f, generate_to_send(arrowTable,request_from_processing(requestPipe)))
        # makes new stream to write_to_processing pipe from pyCharm, uses request schema
        # have to make a new pyarrow table from using request schema

        #writer.write_batch(arrowTable)
        #writer.close()

    #arrow_table = arrowTable.to_arrow()

    #archived_table = arrowTable.with_metadata()

    #writer = ipc.new_stream(sys.stdout.buffer, generate_to_send(arrowTable,request_from_processing(reader=)))



    writer.write_ipc(arrowTable)
    writer.flush()
    writer.close()
"""

"""
def get_section_indices(sendCode): #requires manual calculation

    #sendcode has two parts: map data and non-map data
        # map data requires manual calculation to find how to compress
        # non-map data is direct and hardcoded per data point

    section_indices = []

    # 50 columns, n x 10^7 or 10^8 rows
    # each row is a distinct datum

    sendCode[0]

    return section_indices
"""

"""
def write_to_file(arrowsArr,fileDir):
    i = 0
    with open(fileDir, "wb") as f:

        for column in arrowsArr.columns:
            #thisColumn = pl.Series(column)

            if( i >= 0 and i <= 2): # string column write to file
                encoded = column.encode('utf-8')[:10].ljust(10, b'\x00')
                f.write(encoded)
            else:
                f.write(column.to_numpy().tobytes())

            i = i + 1
"""

"""
def checkPipe(pipeDir): # why not just check, to use the walrus operator
    #checks if pipe has contents ( [0] ) and gets content of pioes ( [1] of infoArray )
    infoArray = []

    file = open(pipeDir, "rb")

    return infoArray

def dsToZoom(arrowArr, downscaleAmount): #downsamples a pyarrow table according to zoom of program
    #1/4 resolution or compression for
    newArr = []

    return newArr

def grab_section(array):
    # all you have to do is column calculation for one and it maps to all
    pass


    #go to the ele part of the array; grab a section using corners

def request_from_processing(reader):
    sendCode1 = []
    #parse request from

    #convert into whatToSend list for generate_to_send

#viewport bounding
#level of detail
#partition into tiles
    # compress for zoom
    return sendCode1

def checkRun(processName1, processName2, processName3): #check change in process name number count
    pass
"""