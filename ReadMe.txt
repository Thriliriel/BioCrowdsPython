BioCrowds - Python Edition

Basic functionalities of BioCrowds are present, like define a Goal, create agents and place obstacles. You can change all information you need in the files inside "Input" folder, namely:

config.txt - basic configurations, like the density of markers and the size of the environment.
obstacles.txt - configuration of the obstacles.
agents.txt - configuration of the agents.
goals.txt - configuration of the goals.

Once the configuration is done, you can run the BioCrowds.py file to start the simulation. Once it is finished, two files are generated: markers.csv and resultFile.csv. The first one stores all the markers generated for the simulation, while the second one stores the positions of all agents throughout the simulation. 

This basic version has no real-time visualization of the simulation. However, it is possible to visualize some things. The VisualizeMarkers.py file allows to see all the markers set in the environment. Can be used to check if the scenario was correctly generated, with obstacles and everything. The Visualize.py file allows to see the trajectory followed by all agents during the last simulation.