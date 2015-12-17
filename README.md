# Cave Exploration
Imagine a cave with treasure hidden in one or several places. The challenge is to explore the entire cave in as few steps as possible.  This program runs such a simulation. As the explorer reaches a dead end she back tracks until a fresh path becomes available. When treasure is found, the path from the starting point to the treasure is noted. The simulation ends when all available spaces in the cave have been explored.

#Set up
This program was built on Python 2.7 and uses the standard library plus numpy 1.10.1
To install numpy `pip install -r requirements.txt`

#Usage
To use this program run python main.py.  You will be prompted to select a cave file. Several examples can be found in /caves.  The simulation will then begin. To advance one step press the step button. When the exploration is completed, press the quit button to end the program.


