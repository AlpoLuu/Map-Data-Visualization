import math
import numpy as np
import mmap
import subprocess
import pandas as pd
import polars as pl
from io import StringIO
from pathlib import Path
import csv

from dataTransform.dataMain import gallpetersArray, robinsonArray, mercatorArray, equiArray


def main():
    pl.Config.set_tbl_rows(20)
    pl.Config.set_tbl_cols(10)
    #1 NOAA_Elevation
    #eleToMask(3326) #takes a file with int-16 signed and turns all non-3326 ( sea elevation ) values into 1 ( land val )
    # can be used for converting bathymetry and relief data into an earth mask

    #height = 21600 #width = 43200 ( resolution of file type )
    #for use in megafile_mask to megafile_mask_majorityvote
    #majorVoteDownscale(21600,43200,4) #too slow and memory consuming if array operations are done in PyCharm

    dataDir = f"/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/"

    testFile = f"NOAA(elevation tiles)/RF_megafile_mask"
    outputFile = f"NOAA(elevation tiles)/RF_megafile_mask_downsampled"

    testFile1 = f"NOAA(elevation tiles)/megafile_mask"
    outputFile1 = f"NOAA(elevation tiles)/RF_megafile_mask"

    #initially tried using sequential reads through a binary file to access information then moved onto memory
    #mapping for accessing uncompressed data, ( sequential ought/should be used for receiving not accessing )
        #memory mapping starts after megafile_mask

    #fileGridsReformat(dataDir+testFile1, dataDir+outputFile1, 21600, 43200, [4800,6000])
    #fileMajorVoteDownscale(testFile,outputFile,21600,43200,8)
    #downsampleModeFile(testFile, outputFile,16,43200,21600)
    #downsampleFile(dataDir+testFile, dataDir+outputFile,20,43200,21600)

    # 1a CDS - ERA5 Climate Reanalysis
    CDSCSVtoCDSArray(dataDir+"CDS_ERA5/1_outputEra/")

# You can use a for loop with concatenation to go through the files instead of typing 18 data set names
# total precipitation is a forecast ( instead of a measurement ) from 5-6 am GST

CDSdates = ("20190101", "20190301", "20190501", "20190701", "20190901", "20191101") #dates
CDSdatas = ('2t', 'sst', 'tp') #these are called shortnames
    #total precipitation only forecasts 5-6 am GST and is in meters
provider = { 'NOAA':0, 'CDS':1, 'USGS_earth':2, 'NOAA_buoy':3, 'NOAA_nws':4, "OWM":5, "ISS":6, "NASA":7, "OSN":8 }
#dict for each provider
#providerNames = ( 'NOAA', 'CDS', 'USGS_earth', 'NOAA_buoy', 'NOAA_nws', "OWM", "ISS", "NASA", "OSN" )
# will grab from files automatically for 2) and 3), manual right now for testing 1)

#datasetsCDSDict = { "2t":"ERA_2mTemperature", "sst":"ERA5_SeaSurfaceTemperature", "tp":"ERA5_totalPrecipitation" }
datasetsCDS = [
    ('gfs_temp.grib', 'CDS', 'ERA_2mTemperature', '20190101'),
    ('era5_wind.grib', 'CDS', 'ERA5_SeaSurfaceTemperature', '20190101'),
    ('nam_precip.grib', 'CDS', 'ERA5_totalPrecipitation', '20190102'),
]

#Grib export for the ERA5 climate data
#in pyCharm because bash terminal does not support delimiter removal
#I can't tell whether to insert standard array zero columns for all array kinds or particular instance
    # initially do a specific case then parameterize

# this is automatic for Polars arrays
def categoricalEncodePrint(arrayOfStrs):
    for i in range(0,len(arrayOfStrs)):
        print(arrayOfStrs[i],i)

# standardProcess functions does the complete version of what main is meant to do: reformat, downsample the mask value,
# turn the mask value into an array to be sent to dataMain
# then process the CDS_Era5 values to be turned into a polars array then send to be sent to dataMain
# ( all data is completely formatted for the standardized array )
def standardProcess():

    return

# can be done with the instantiation of a numpy array, may be needed for regular python lists
def insertZeroColumns(array, pos, numberOfColumns):
    """
    for i in range(0, numberOfColumns):
        np.insert(array,[pos],np.zeros((array.shape[0],1)), axis=1)
        print(array.shape)
    """
    zeros = np.zeros((array.shape[0],numberOfColumns))
    newArr = np.insert(array,[pos],zeros,axis=1)

    return newArr

def CDSCSVtoCDSArray(inputFile):
    mainArray = np.asarray([[]])
    #build using polars and numpy, then optimize using either numpy or polars routines in some order

    i = 0
    polarsDataFrames = []
    for date in CDSdates:
        for datumType in CDSdatas: # a little gross, test for manual
                i+=1
                #readFile = open(inputFile+{date}+"_ERA5_"+{datumType}, 'rb')
                #with open(inputFile+{date}+"_ERA5_"+{datumType}+'.csv', 'r') as f:
                #    reader = csv.reader(f)
                reader = pl.read_csv(f"{inputFile}{date}_ERA5_{datumType}.csv")
                #print(reader)
                all_rows = np.asarray(reader)
                CDSArray = np.zeros((all_rows.shape[0],3),dtype='S10')
                mainArray = np.zeros((all_rows.shape[0],5+10),dtype='f4')
                standardizeCoordinates(all_rows,0,360,1,1)
                if(datumType == CDSdatas[0] or datumType == CDSdatas[1]):
                    standardizeTemp(all_rows,1,2)

                #standardizeCoordinates(mainArray,0,180,0,0) lat is already standardized

                #rowArray[0] = inputFile
                CDSArray[:,0] = "CDS_ERA5"
                CDSArray[:,1] = date
                CDSArray[:,2] = datumType

                mainArray[:,0] = all_rows[:,0]  # adds lat to lat column
                mainArray[:,1] = all_rows[:,1]  # adds long to long column
                if (datumType == CDSdatas[0]): # adds 2t temperature to 2t temperature column
                    mainArray[:,12] = all_rows[:,2]
                if (datumType == CDSdatas[1]): # adds seaside temperature to seaside temperature column
                    mainArray[:,13] = all_rows[:,2]
                if (datumType == CDSdatas[2]): # adds total precipitation to total precipitation column
                    mainArray[:,14] = all_rows[:,2]


                #mainArray = insertZeroColumns(mainArray, 2, 8)
                #print(mainArray, datumType, date, mainArray.shape)
                #print(mainArray[:,10:13], datumType, mainArray.shape)
                #print(CDSArray)

                #make polars dataframe for i/18
                polarsData = {}
                #print(mainArray.shape[1],CDSArray.shape[1])
                mainCols = mainArray.shape[1]
                CDSCols = CDSArray.shape[1]
                for k in range(0,CDSCols):
                    polarsData[str(k)] = CDSArray[:,k]
                for j in range(0,mainCols):
                    polarsData[(str(CDSCols + j))] = mainArray[:,j]

                polarsDataFrames.append(pl.DataFrame(polarsData))


                #add to bigger data frame to get concatenation of polarsarrays[i]
                if i==6:
                    print(polarsDataFrames)

    polarsDataMain = pl.concat(polarsDataFrames)
    print(polarsDataMain)

    #pOfStandardArray = + # pOfStandardArray is the concatenation of the identifiers and values arrays
    #return numpyArray

    #EQUIRECTTOLATLONG is exclusively used by the NOAA_ele array
def equirectFileToPolarsArray(fileInput):

    #provider,time,name, lat, long, x_equ, y_equ, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, map_val
    # 3 + ( 10 + 1 )

    with open("mask.raw", "rb") as f:
        raw_bytes = f.read()

    STRArray = np.zeros((1080*2160, 3), dtype='S10') # make ths STR array to be concatenated in polars array
    valArray = np.zeros((1080*2160, 10 + 1), dtype='f4') # makes the value array to be standardized

    arr = np.frombuffer(raw_bytes, dtype=np.uint8).reshape(1080*2160, 1) # makes the column array for values array

    valArray[:,10] = arr

    #either starts from 1 - 2180 or 0 - 2179 fully inclusive both
    for i in range(0,2160):
        for j in range(0, 1080):
            valArray[i*1080+j,2] = j
            valArray[i*1080+j,3] = i*1080+j

    #positionArr = arr.reshape(1080,2160)
    valArray = equirectToLatLong(valArray)
    valArray = gallpetersArray()
    valArray = robinsonArray()
    valArray = mercatorArray()
    valArray = equiArray()


    valArray = latLongtoProjectionSet(valArray)

    # then convert both to polars array, then concatenate STRArray + valArray to a mainPolarsArray for standardized array

    return

# both equiRectToLatLong latLongToProjectionSet take numpy arrays or python arrays
def equirectToLatLong(array):
    array[:,1] = ((array[:,3]-1080)/2160)*math.pi # conversion on a column for longitude
    array[:,0] = ((array[:,2]-540)/1080)*(math.pi/2) # conversion on a column for latitude

    return array

def latLongtoProjectionSet(array):




    return array


#reformats an ar.reshape[filesHeight,filesWidth] on a file to become ar.shape = [1]
def fileGridsReformat(inputFile, outputFile, height, width, gridHeights):
    # can make a general version that reformats a file given a 3D-array of files dim [[x_i,y_i]
    # where y_i = y_i+r or y_i = y_i-r, where x_i = x_i+1 or x_i = x_i-1 for entries in a 2D array
    # for now, just reformat .OS9a and .0S9b into a regular megafile
        # use default function pass for specific and general

    # make the program first then generalize and parameterize
    readBuffer = open(inputFile, 'rb')
    writeBuffer = open(outputFile,'wb')

    #16megafiles_mask has 933120000 ( 43200 x 21600 ) entries
    #16megafiles_mask_majorvote has 933120000 / 16 = 58320000 ( 10800 x 5400 ) entries

    # w, s := 0
    #read write til end of row grid Z, jump grid_Z.(x*y), read write til end of row grid Z+1, . . . jump grid_(Z+1).(x*y)
    #.... jump grid_(Z+3).(x*y), read write til end of row grid (Z+3)
    #
    # go back to start of grid Z, add one to s ( height )
    """
    for i in range(0,height): #implementation is easier because all files have same widths
        for k in range(0,width):
            for j in range(0,4):
                #print(i,j)
                writeBuffer.write(read_line(readBuffer, 10800, j*10800+i*43200 ))
        writeBuffer.flush()

    for i in range(0,height):
        for k in range(0,width):
            writeBuffer.write(read_line(readBuffer, 10800, i*height))

    for i in range(0,16):
        for k in range(0,width):
            for j in range(0,gridHeights[heightVal]):
                writeBuffer.write(read_line(readBuffer, 10800, ))
        writeBuffer.flush()
        if(i >= 8 and i < 12):
            heightVal = 1
        else:
            heightVal = 0
    """

    gridsTotal = [0, gridHeights[0]*width, gridHeights[1]*width, gridHeights[1]*width]
    offset = np.cumsum(gridsTotal)
    print(offset)
    """
    offset[0] = 0
    offset[1] = gridHeights[0]*10800*4
    offset[2] = gridHeights[0]*10800*4 + gridHeights[1]*10800*4
    offset[3] = gridHeights[0]*10800*4 + gridHeights[1]*10800*4 + gridHeights[1]*10800*4
    print(offset)
    """

    for j in range(0, gridHeights[0]):
        for i in range(0,4):
            local_i = i
            offsetPos = j*10800+i*(gridHeights[0]*10800)+offset[0]
            writeBuffer.write(read_line(readBuffer,10800,offsetPos))
            print(offsetPos, 1)

    for j in range(0, gridHeights[1]):
        for i in range(4,8):
            local_i = i - 4
            offsetPos = j*10800+local_i*(gridHeights[1]*10800)+offset[1]
            writeBuffer.write(read_line(readBuffer,10800,offsetPos))
            print(offsetPos, 2)

    for j in range(0, gridHeights[1]):
        for i in range(8,12):
            local_i = i - 8
            offsetPos = j*10800+local_i*(gridHeights[1]*10800)+offset[2]
            writeBuffer.write(read_line(readBuffer,10800,offsetPos))
            print(offsetPos, 3)

    for j in range(0, gridHeights[0]):
        for i in range(12,16):
            local_i = i - 12
            offsetPos = j*10800+local_i*(gridHeights[0]*10800)+offset[3]
            writeBuffer.write(read_line(readBuffer,10800,offsetPos))
            print(offsetPos, 4)

    writeBuffer.flush()





    #general file reformat from grid of 2D data(s)
    #figure out new file format dimensions from formatDims diagonals

    #file.seek(0,0) #absolute current cursor in file
    #file.seek(0, 1) #jump from current cursor in file

def fileGridsReformatVectorized(inputFile, outputFile, format):
    readBuffer = open(inputFile, 'rb')
    writeBuffer = open(outputFile, 'wb')

def equiToLatLong(height,width):

    return


#downsamples a file using majority vote
def fileMajorVoteDownscale(inputFile,outputFile,height,width,scaleAmount):

    readBuffer = open(inputFile, 'rb') #intialize buffers for regular file and downscaled file
    writeBuffer = open(outputFile, 'wb')

    for i in range(0,int(height/scaleAmount)):
        for j in range(0,int(width/scaleAmount)):
            print(i, j)
            downsampledVal = majorityvote_vectorized([0,1],read_block_vectorized(readBuffer, scaleAmount, j*scaleAmount+i*scaleAmount, width))

            writeBuffer.write(bytes(downsampledVal))
        writeBuffer.flush()


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

def downsampleFile(inputFile, outputFile, blockLength, width, height, dtype=np.uint8):
    # Optimizing mode downsampling with this large of a data requires expertise, so I will just pick every
    # N = blockLength, Nth pixel with height offsets in file ( the result is almost the same )
    fileName = open(inputFile, 'rb')
    fileMemoryMap = mmap.mmap(
        fileName.fileno(), length=0, access=mmap.ACCESS_READ
    )
    fileOneD = np.frombuffer(fileMemoryMap, dtype=np.uint8)
    fileTwoD = fileOneD.reshape(height, width)
    downsampled = fileTwoD[::blockLength,::blockLength].ravel()

    # you can use a for loop on fileOneD to get the downsample, though that is less efficient

    print(downsampled.shape)

    output_mmap = np.memmap(outputFile, dtype=np.uint8, mode='w+', shape=downsampled.shape)
    output_mmap[:] = downsampled[:]
    output_mmap.flush()
    del output_mmap


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

    result = fileTwoD.copy()


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

if __name__ == "__main__":
    main()