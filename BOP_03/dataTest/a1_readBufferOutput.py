import dataTransform

def main():
    array = []
    inputPath = f'/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/dataTest/a1_dataBlockBinary'
    #datablockbinary is 16x16 grid of binary

    readBuffer = open(inputPath,'rb')
    readBuffer.seek(0,0)

    array.append(str(readBuffer.read(8)))
    readBuffer.seek(0, 0)
    print(readBuffer.read(8), array)


if __name__ == "__main__":
    main()