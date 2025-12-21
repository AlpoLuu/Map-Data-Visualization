import dataTransform
import numpy as np

def main():
    twoDArray = [[0,1,0],[1,1,0],[1,0,1]]
    voterVals = [0,1]
    twoDArr = np.asarray(twoDArray)
    vVls = np.asarray(voterVals)



    arrayFlat = twoDArr.ravel(order='C')
    #twoDArray 2D-array is flattened down-right to 1D, votervals is turned into an numpy array for operations

    matches = arrayFlat[:, np.newaxis] == vVls[np.newaxis, :]
    # axis is just a generalization of x,y,z,w, . . .; rows, columns, depths, . . . respectively
    print(matches)

if __name__ == "__main__":
    main()