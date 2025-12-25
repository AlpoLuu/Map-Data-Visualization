
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