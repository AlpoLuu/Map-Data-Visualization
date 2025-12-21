
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