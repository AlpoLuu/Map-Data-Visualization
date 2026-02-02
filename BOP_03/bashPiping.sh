
bopDir='/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP' # cleaner code
#alias can have undercases, variables must always be full-case

#start the programs
#we're taking files converting them to arrays then importing to next python program, once there's no need we can stop the program
#python "{$bopDir}/dataTransform/t1_dataFile.py"
# need to check that array is made in the main() then run dataMain
#python "{$bopDir}/dataTransform/t1_dataMain.py"




# stop datafile and datamain here

#setup pipes

#python "/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataTransform/t1_dataGrab1.py" |  python "/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataTransform/t1_dataFile.py"
#python "/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataTransform/t1_dataMain.py" |  processing-java --sketch="/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataVisualization/aMain_visualization/aMain_visualization.pde" --run


mainRun(){
       rm -f "$bopDir/temp/pyFROMpro_request_pipe_map"
       rm -f "$bopDir/temp/pyFROMpro_response_pipe"
       mkfifo "$bopDir/temp/pyFROMpro_request_pipe_map"
       mkfifo "$bopDir/temp/pyFROMpro_response_pipe"

       #datafile and datamain need to be sequenced by array creation
       #python3 "$bopDir/dataTransform/t1_function.py"
       #python3 "$bopDir/dataTransform/a_projectionfunctions.py"
       #python3 "$bopDir/dataTransform/dataFile.py"
       #python3 "$bopDir/dataTransform/dataMain.py"

       cat < "$bopDir/temp/pyFROMpro_response_pipe" > "$bopDir/dataVisualization/output.csv" &
       python3 "$bopDir/dataTransform/dataStream.py"

       #if do 

       # builds and runs in the bash script, if no build other paired .pde do not run
      
       processing-java --sketch="$bopDir/dataVisualization/aMain_visualization" --output="$bopDir/dataVisualization/sketch_built" --build
       processing-java --sketch="$bopDir/dataVisualization/aMain_visualization" --run

       #detect if processing/pycharm/bash-terminal closes; if it does then all programs ( bound x y z by shared bend )

       #How do I check if ALL programs are running?
              #it needs to be either on Processing or PyCharm: though pyCharm may be best
}

mainRun

#------ Scrapped Functions


archivedRun(){ # might be scrapped
       # setup the pipelines

       mkfifo /tmp/pyFROMpro_request_pipe_map
       #mkfifo /tmp/pyFROMpro_request_pipe_maindata
       #mkfifo /tmp/pyFROMpro_request_pipe_bigdata
       # cat /tmp/proTOpy_request_pipe | tee pycharmProcess (sys.stdin)

       mkfifo /tmp/proFROMpy_response_pipe # I have to route this to system.in in processing somehow
       # cat /tmp/pyTOpro_response_pipe | tee processingProcess (system.in)

       # you go from pycharm to file ( through bash as pipe ) to processing 

       # ONLY UPDATE BASED ON NON-REDUNDANT GUI INTERACTIONS to keep pipes clean
       # divide pipe runs by program run number, line per request
              # in a request ( in str ): zoom, position
              # computations for figuring out tiles to display, compression default ( downsample from array )

       # py ------ pro --request state change-- pro-gui ( interaction in pro-gui )
       # py <---request data ( through request pipe ) --- pro ------  pro-gui
       # sent data is compressed, processing checks tiles to display through zoom and position ( compression and tiling )
       # py ----(send data)---> pro ----- pro-gui 
       # py ------- pro -- change state ---> pro-gui
       # py ------ pro ------ pro-gui ( new display for new data, continually re-displays every second, updating data display is intervaled every second)
       # GUI and MAPDISPLAY is updated every 20 frames or atleast >10 frames per second for interactivity       

       #we're taking files converting them to arrays then importing to next python program, once there's no need we can stop the .py
       #import may break 
       #python "{$bopDir}/dataTransform/t1_datafile.py"
       #python "{$bopDir}/dataTransform/t1_dataMain.py"

       # need to check that array is made in the main() then run dataMain
       python "{$bopDir}/dataTransform/t1_dataStream.py"
       # stop datafile and datamain here after array has been completed for data streaming
       
       head -n 5 /tmp/status_pipe >> bopDir/headHistory
       rm /tmp/status_pipe          
}

