import struct #python has all data types as objects, primitives are good for data
import pyarrow as pa
import polars as pl

import socket
import struct

#

import pyarrow.ipc as ipc
import sys
from sympy import false

#from dataMain import standardArray
import dataMain

#datafile is for archived 1.
#datastream is for pulling from files, cloud and api 2.
# 3. will be done in its own .py

#datamain.py is where all the data aggregates to be sent to processing ide

    # 2. will extract values then use stream buffer or shared python to send the arrays to be standardized

# stream from archived has its own function for testing, and to test schema operations

running = True
toSend = True
sendCode = []
counter = 0


mainDir = f"/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP"
outPipeDir = f"{mainDir}/temp/pyFROMpro_response_pipe"
inPipeDir = f"{mainDir}/temp/pyFROMpro_request_pipe_map"

""""
options = ipc.IpcWriteOptions(
    compression=None,
    use_legacy_format=False,
    metadata_version=ipc.MetadataVersion.V5,
    use_threads=True,
    emit_dictionary_deltas=True,
    min_space_savings=0.0
)"""

def run(inputArr):
    """

    if (counter == 1000):
        counter = 0

    if (checkPipe()[0] == True) and (sendCode := checkPipe()[1]):  # checks request pipe if it contains info
        toSend = True

    if (toSend == True):  # if tosend is true then sends the new array to the py-pro pipe

        write_to_file(generate_to_send(inputArr, sendCode), outPipeDir)
        toSend = False

    if (checkRun("processing", "terminal", "pyCharm") == false):  # ends entire program if count of any programs change
        running = false
    """

    pass
    #write_to_file( generate_to_send(inputArr, sendCode) , outPipeDir)

def main():
    standardArray = dataMain.makeArray()

    all_unique = (
            standardArray["0"].unique().to_list()
            + standardArray["1"].unique().to_list()
            + standardArray["2"].unique().to_list()
    )
    print (all_unique)

    #print(standardArray)

    """
    dsArray = dsToZoom(standardArray, 4, "0", "NOAA_ele")
    del standardArray
    """

    betterArray = grabSome(standardArray)
    del standardArray

    print(betterArray)

    with open(outPipeDir, "w") as f:
        betterArray.write_csv(f)


    #savedArray = dataMain.standardArray.to_arrow() # supports string and float in one array while being efficient

    #while(running == True and counter == 0): # running program variable
    #    run(standardArray)

def grabSome(arrowArr):
    targets = pl.DataFrame({
        "0": ["NOAA_ele", "CDS_ERA5","CDS_ERA5","CDS_ERA5"],
        "1": ["20090101","20190101","20190101","20190101"],
        "2": ["map", "2t", "sst","tp"],
    })

    filtered = arrowArr.join(targets, on=["0", "1", "2"], how="semi")
    return filtered

def dsToZoom2(arrowArr, downscaleAMount, inColumn, filterItem):
    df = arrowArr.with_row_index("__idx")

    # 1)
    map_rows = df.filter(pl.col(inColumn) == filterItem)
    other_rows = df.filter(pl.col(inColumn) != filterItem)

    result = (
        pl.concat([other_rows, map_rows])
        .sort("__idx")
        .drop("__idx")
    )

    return result

def dsToZoom(arrowArr, downscaleAmount, inColumn, filterItem):
    df = arrowArr.with_row_index("__idx")

    map_rows = df.filter(pl.col(inColumn) == filterItem)
    other_rows = df.filter(pl.col(inColumn) != filterItem)

    map_rows_downsampled = map_rows.gather_every(downscaleAmount)

    result = (
        pl.concat([other_rows, map_rows_downsampled])
        .sort("__idx")
        .drop("__idx")
    )

    return result

if __name__ == "__main__":
    main()