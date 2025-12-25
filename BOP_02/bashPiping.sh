

#start the programs

python "/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataTransform/t1_dataGrab1.py"
python "/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataTransform/t1_dataMain.py"

#setup pipes

python "/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataTransform/t1_dataGrab1.py" |  python "/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataTransform/t1_dataMain.py"
python "/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataTransform/t1_dataMain.py" |  processing-java --sketch="/home/user/Desktop/Owl & Stars/BashOrchestrationProgram_BOP/dataVisualization/aMain_visualization/aMain_visualization.pde" --run
