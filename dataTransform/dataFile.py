
import numpy as np
import mmap
import io


maskPreFormatPos = []
maskPreFormatDims = []
maskFileDims = [4,4]

def main():
    #1 NOAA_Elevation
    #eleToMask(3326) #takes a file with int-16 signed and turns all non-3326 ( sea elevation ) values into 1 ( land val )
    # can be used for converting bathymetry and relief data into an earth mask

    #height = 21600 #width = 43200 ( resolution of file type )
    #for use in megafile_mask to megafile_mask_majorityvote
    #majorVoteDownscale(21600,43200,4) #too slow and memory consuming if array operations are done in PyCharm

    testFile = f"/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/RF_megafile_mask"
    outputFile = f"/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/RF_megafile_mask_downsampled"

    #initially tried using sequential reads through a binary file to access information then moved onto memory
    #mapping for accessing uncompressed data, ( sequential ought/should be used for receiving not accessing )
        #memory mapping starts after megafile_mask

    #fileGridsReformat('megafile_mask','RF_megafile_mask')

    #fileMajorVoteDownscale('RF_megafile_mask','RF_megafile_mask_downscaled',21600,43200,8)
    downsampleModeFile(testFile, outputFile,16,43200,21600)
    #1a CDS - ERA5 Climate Reanalysis

#reformats an ar.reshape[filesHeight,filesWidth] on a file to become ar.shape = [1]
def fileGridsReformat(file, formattedFile, formatDims=maskPreFormatDims,formatPos=maskPreFormatPos, formatDim=maskFileDims):
    # can make a general version that reformats a file given a 3D-array of files dim [[x_i,y_i]
    # where y_i = y_i+r or y_i = y_i-r, where x_i = x_i+1 or x_i = x_i-1 for entries in a 2D array
    # for now, just reformat .OS9a and .0S9b into a regular megafile
        # use default function pass for specific and general

    # make the program first then generalize and parameterize
    input_path = f'/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/{file}'
    output_path = f'/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/{formattedFile}'

    readBuffer = open(input_path, 'rb')
    writeBuffer = open(output_path,'wb')

    #16megafiles_mask has 933120000 ( 43200 x 21600 ) entries
    #16megafiles_mask_majorvote has 933120000 / 16 = 58320000 ( 10800 x 5400 ) entries

    # w, s := 0
    #read write til end of row grid Z, jump grid_Z.(x*y), read write til end of row grid Z+1, . . . jump grid_(Z+1).(x*y)
    #.... jump grid_(Z+3).(x*y), read write til end of row grid (Z+3)
    #
    # go back to start of grid Z, add one to s ( height )
    for i in range(0,21600): #implementation is easier because all files have same widths
        for j in range(0,4):
            #print(i,j)
            writeBuffer.write(read_line(readBuffer, 10800, j*10800+i*43200 ))





    #general file reformat from grid of 2D data(s)
    #figure out new file format dimensions from formatDims diagonals

    #file.seek(0,0) #absolute current cursor in file
    #file.seek(0, 1) #jump from current cursor in file

#downsamples a file using majority vote
def fileMajorVoteDownscale(file, downscaledFile,height,width,scaleAmount):
    input_path = f'/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/{file}'
    output_path = f'/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/{downscaledFile}'

    readBuffer = open(input_path, 'rb') #intialize buffers for regular file and downscaled file
    writeBuffer = open(output_path,'wb')

    for i in range(0,int(height/scaleAmount)):
        for j in range(0,int(width/scaleAmount)):
            print(i, j)
            downsampledVal = majorityvote_vectorized([0,1],read_block_vectorized(readBuffer, scaleAmount, j*scaleAmount+i*scaleAmount, width))

            writeBuffer.write(bytes(downsampledVal))


#reads a line from a file
def read_line(readBuffer, lineLength, pos):

    readBuffer.seek(pos,0)
    #line = line + readBuffer.read()
    #line.extend(b'readBuffer.read()') space efficient
    line = readBuffer.read(lineLength)

    return line

#reads a block from a file using array indices and for loops
def read_block(readBuffer, blockLength, pos, rowLength):
    values = np.zeros((blockLength, blockLength), dtype=np.uint8)
    #values = []

    for i in range(0,blockLength):
        readBuffer.seek(pos+i*rowLength,0)
        values[i] = (list(readBuffer.read(blockLength)))

    finalArray = values.ravel()

    #print(values, finalArray)

    return finalArray

#reads a block from a file using numpy array routines
def read_block_vectorized(readBuffer, blockLength, pos, rowLength):
    total_bytes = rowLength*(blockLength-1) + blockLength
    readBuffer.seek(pos,0)

    bytesFromFile = readBuffer.read(total_bytes)

    arrayOfBytes = np.frombuffer(bytesFromFile, dtype=np.uint8)
    #oneDArray = np.copy(arrayOfBytes)
    #arrayOfBytes = arrayOfBytes.reshape(blockLength,)

    #arrayOfBytes = arrayOfBytes.transpose

    row_offset = np.arange(blockLength) * rowLength
    col_offset = np.arange(blockLength) #

    indices = row_offset[:, np.newaxis] + col_offset
    #print(indices)



    block_oneDArray = arrayOfBytes[indices.ravel()]
    #print(block_oneDArray)
    # Not familiar with numPy array operations and routines, will have to work with them
    # more in the future for database style thinking

    return block_oneDArray

# majority vote on a 2D-array using for-loops and array indices, returns one value
def majorityVote(voterVals,twoDArray): #takes votervals ( a, b, . . . . c ) in array, counts each voterval occurence in
    electionWinner = 0
    #array, then highest count is returned

    # another way to make this where voterVals is a 2d array with [ voterVal, voterCount ] go through voterCount
    # to find biggest voterVal

    countWin = 0
        #newArray = [] #numPy array as replacement for optimization, NOT NEEDED

    #print(twoDArray, len(twoDArray), len(twoDArray[0]), len(voterVals))

    """ Old 2D-Array into 1D-Array, not optimized enough
    for i in range(0,len(twoDArray)):
        #print(i)
        for j in range(0,len(twoDArray[i])):
            #print(j)
            newArray.append(twoDArray[i][j])
    """

    #grab the value(s) in array then make a 2D-array [ voterVal_i ]

    # k = n x n, i <= n x n
    # k < O_r( mV_dL ) <= k*i, k < O_r( mV_d ) <= k*i

    for k in range (0,len(voterVals)):
        countNow = 0
        for i in range(0,len(twoDArray)):
            if(twoDArray[k] == voterVals[k] ):
                countNow += 1
        if(countNow > countWin):
            countWin = countNow
            electionWinner = voterVals[k]

    return electionWinner

#majority vote on a 2D-array using vectorized method ( numpy array routines ) returns one value
def majorityvote_vectorized(voterVals,twoDArray):
    arrayFlat = twoDArray.ravel(order='C')
    npVoterVals = np.asarray(voterVals)
    #twoDArray 2D-array is flattened down-right to 1D, votervals is turned into an numpy array for operations

    matches = arrayFlat[:, np.newaxis] == npVoterVals[np.newaxis, :]
    #uses vectors to check every element a in arrayFlat[0,1, . . . 0,1] with [0,1]
    # I don't know the output, I need to check in another program

    counts = matches.sum(axis = 0)
    voteWin_index = np.argmax(counts)

    return npVoterVals[voteWin_index]

# downsamples a file using majority vote all in one function
def downsampleModeFile(inputFile, outputFile, blockLength, width, height, dtype=np.uint8):

    fileName = open(inputFile, 'rb')
    fileMemoryMap = mmap.mmap(
        fileName.fileno(), length=0, access=mmap.ACCESS_READ
    )
    voteVals = np.asarray([0,1])

    fileOneD = np.frombuffer(fileMemoryMap, dtype=np.uint8)
    #voteVals = np.unique(fileOneD) Too memory consuming and slow runtime
    #print(voteVals)
    newHeight = height // blockLength
    newWidth = width // blockLength


    fileTwoD = fileOneD.reshape(height, width)

    #fileTwoD.reshape(newHeight, blockLength, width)


    #fileBlocks = fileTwoD.reshape(int(height/blockLength),int(width/blockLength),blockLength,blockLength)
        #this holds for desired form and order, height/scale x width/scale of blockLength by blockLength blocks
        #if Claude analogy is right
    #print(fileBlocks.shape)
    #fileBlocksTransposed = np.moveaxis(fileBlocks,[0,1,2,3],[0,2,1,3])
    #print(fileBlocksTransposed, fileBlocksTransposed.shape)

    #fileToDownsample = fileBlocks.reshape(int(height/blockLength),int(width/blockLength),blockLength*blockLength)
    # you don't want reshape on (x,y,z) --> (f(x,y),z) because it perserves order and gives indices entries
    # you want arr.reshape without preserving order

    # you want to manipulate the axons in some way such that order is not preserved when flattening all arrays
    # in blockLength * blockLength axis or atleast preserved in such a way that the final result is ordered
    # in C-(numpy argument) format

    #print(fileToDownsample)

    result = stepArray.copy()


    for i in range(0,int((height*width)/(blockLength*blockLength))):
        print(i)
        count = np.count_nonzero(result[:,i])
        if( count >= blockLength*blockLength/2 ):
            #np.insert(fileToDownsample[i,:])
            result[0,i] = 1
        else:
            result[0,i] = 0

    newFile = result[0:1,:]

    #go from (big number, blockLength*blockLength) to (big number, 1) using one np vector function, this preserves order
    #

    # [[0,1,2,3,4,5,6, . . . n^2-1], [n^2, . . .,2n^2-1], . . . again which is pretty much almost a for loop

    #fileBlocks[i,j,:,:] there is some operation that transform this matrix, such that order can be preserved and you
    # can still count voter-ized version of the matrix

        # approaches that do not work: hot_ones, for loop with vectorization, for loops


    # voter-ized using only numpy functions #1 ( vectorized ) ( meaning for some block ( since it's binary ) that is a
    # flipped version of that block, such that we can count the number of votes
    # then set the value of first block to the majority winner then squeeze/delete the second block all at once in
    # axis


    #print(fileBlocks.shape)

    # once you sum the counted values using the boolean vectorized operation, you can't use reshape because it
    # preserves order


    output_mmap = np.memmap(outputFile, dtype=np.uint8, mode='w+', shape=newFile.shape)
    output_mmap[:] = newFile
    output_mmap.flush()
    del output_mmap

    #print(counted, counted.shape) # left entry is 0 majorvote, right entry is 1 majorvote


def eleToMask(x):
    data = np.fromfile(
        '/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/megafile',
        dtype='>i2')
    mask = (data != x).astype(np.uint8) #3326 was used as x
    mask.tofile(
        '/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/megafile_mask')

if __name__ == "__main__":
    main()