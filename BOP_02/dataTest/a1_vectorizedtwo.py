import numpy as np

def main():
    arr1 = np.asarray(np.arange(0,24))
    arr3 = arr1.reshape((2,4,3,1))
    arr4 = arr3.reshape((6,4))
    arrN = np.asarray(np.arange(0,64)).reshape(8,8)
    #np.reshape((2,2,4))

    arrA =  np.asarray(np.arange(0,4)).reshape(2,2)
    arrB = np.asarray(np.arange(4,8)).reshape(2,2)
    arrC = np.asarray(np.arange(8,12)).reshape(2,2)
    arrD = np.asarray(np.arange(12,16)).reshape(2,2)
    arrMega = np.concatenate((arrA, arrB, arrC, arrD), axis=0)

    #cumsum test
    arrC = [0,1,2,2]
    arrW = np.cumsum(arrC)
    print(arrW)

    #np.reshape(arr1, (12,2))
    #np.reshape(arr3, (6,4))

    #print("\n", arr3[:,3,:,:])
    #print("\n", arr4[:,3])
    #print("\n", arr1[2:4])

    #arr3[:,:,:,0] the axis=3 "contains" all values on axis 3 which "has" all values

    #transposing axes is different than swapping a column or grid
    #axes define the form of the matrix whereas the elements are the contents
    #swapaxis, moveaxis are different operations than transpose axis
    downsampledArr = arrN[::2,::2]

    arr6 = np.asarray(np.arange(8*4)) # I want blocks of 4x4
    arr7 = arr6.reshape(2,2,8)
    # I want to swap arr7[1,0,:] and arr7[0,1,:]

    arr8 = arr7.transpose(1,0,2)
    print(arr8[1,:,:], arr8.shape)
    print(arr7[1,:,:])
    print(downsampledArr,downsampledArr.shape, "\n")
    print(arrMega, arrMega.shape)

if __name__ == "__main__":
    main()