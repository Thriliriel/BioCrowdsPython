from os import path
import argparse
from AgentClass import AgentClass
from Parsing.ParserJSON import ParserJSON
from Parsing.ParserTXT import ParserTXT
from Vector3Class import Vector3
from CellClass import CellClass
from MarkerClass import MarkerClass
from GoalClass import GoalClass
from ObstacleClass import ObstacleClass

#default values
#size of the scenario
mapSize = Vector3(20, 20, 0)
#markers density
PORC_QTD_Marcacoes = 0.65
#FPS (default: 50FPS)
timeStep = 0.02
#size of each square cell (Ex: 2 -> cell 2x2)
cellSize = 2
#using path planning?
pathPlanning = True
#using json input
jsonInputFile = ''

goals:list[GoalClass] = []
agents:list[AgentClass] = []
obstacles:list[ObstacleClass] = []
cells:list[CellClass] = []

#create the cells and markers
def CreateMap():
	i = j = 0
	while i < mapSize.x:
		while j < mapSize.y:
			cells.append(CellClass(str(i)+"-"+str(j), Vector3(i, j, 0), cellSize, PORC_QTD_Marcacoes, []))
			j += cellSize
		i += cellSize
		j = 0

#create markers
def CreateMarkers():
	for i in range(0, len(cells)):
		cells[i].CreateMarkers(obstacles)
		#print("Qnt created: ", len(cells[i].markers))

#save markers in file
def SaveMarkers():
	markerFile = open("markers.csv", "w")
	for i in range(0, len(cells)):
		for j in range(0, len(cells[i].markers)):
			markerFile.write(cells[i].id + ";" + str(cells[i].markers[j].position.x) + ";" + str(cells[i].markers[j].position.y) + ";" + str(cells[i].markers[j].position.z) + "\n")
	markerFile.close()

arg_parser = argparse.ArgumentParser(description="BioCrowds Python.")
arg_parser.add_argument('--f', metavar="F", type=str, default = '', help='Input File Name.')
args = vars(arg_parser.parse_args())


#parse the JSON input
if args['f'] != '':
	mapSize, goals, agents, obstacles = ParserJSON.ParseFile(args['f'])
	CreateMap()
	CreateMarkers()
	SaveMarkers()


#read the config files if no JSON is defined
if args['f'] == '':
	PORC_QTD_Marcacoes, timeStep, cellSize, mapSize, pathPlanning = ParserTXT.ParseConfigurationFile()
	goals = ParserTXT.ParseGoals()
	agents = ParserTXT.ParseAgents(goals, pathPlanning)
	obstacles = ParserTXT.ParseObstacles()
	CreateMap()
	CreateMarkers()
	SaveMarkers()

#for each goal, vinculate the cell
for i in range(0, len(goals)):
	totalDistance = cellSize * 2
	for j in range(0, len(cells)):
		distance = Vector3.Distance(goals[i].position, cells[j].position)

		#if distance is lower than total, change
		if distance < totalDistance:
			totalDistance = distance
			goals[i].cell = cells[j]

#for each cell, find its neighbors
for i in range(0, len(cells)):
	cells[i].FindNeighbor(cells)

#for each agent, find its initial cell
for i in range(0, len(agents)):
	minDis = 5
	for c in range(0, len(cells)):
		dist = Vector3.Distance(agents[i].position, cells[c].position)
		if dist < minDis:
			minDis = dist
			agents[i].cell = cells[c]

#for each agent, calculate the path, if true
if pathPlanning:
	for i in range(0, len(agents)):
		agents[i].FindPath()

#open file to write
resultFile = open("resultFile.csv", "w")

simulationFrame = 0

#walking loop
while True:
	#if no agents anymore, break
	if len(agents) == 0:
		break

	#for each agent, we reset their info
	for i in range(0, len(agents)):
		agents[i].ClearAgent()
	#print("markers", len(agents[0].markers))
	#reset the markers
	for i in range(0, len(cells)):
		for j in range(0, len(cells[i].markers)):
			cells[i].markers[j].ResetMarker()
	
	#find nearest markers for each agent
	for i in range(0, len(agents)):
		agents[i].FindNearMarkers()
	#	print(sum([len(c.markers) for c in cells]), len(agents[i].markers))

	#/*to find where the agent must move, we need to get the vectors from the agent to each auxin he has, and compare with 
	#   the vector from agent to goal, generating a angle which must lie between 0 (best case) and 180 (worst case)
	#   The calculation formula was taken from the Bicho´s mastery tesis and from Paravisi algorithm, all included
	#   in AgentController.
	#   */

	#   /*for each agent, we:
	#   1 - verify existence
	#   2 - find him 
	#   3 - for each marker near him, find the distance vector between it and the agent
	#   4 - calculate the movement vector (CalculateMotionVector())
	#   5 - calculate speed vector (CalculateSpeed())
	#   6 - walk (Walk())
	#   7 - verify if the agent has reached the goal. If so, destroy it
	#   */

	agentsToKill = []
	i = 0
	while i < len(agents):
		agentMarkers = agents[i].markers

		#vector for each marker
		for j in range(0, len(agentMarkers)):
			#add the distance vector between it and the agent
			#print (agents[i].position, agentMarkers[j].position)
			agents[i].vetorDistRelacaoMarcacao.append(Vector3.Sub_vec(agentMarkers[j].position, agents[i].position))

		#print("total", len(agents[i].vetorDistRelacaoMarcacao))
		#calculate the movement vector
		agents[i].CalculateMotionVector()

		#print(agents[i].m)
        #calculate speed vector
		agents[i].CalculateSpeed()

		#walk
		agents[i].Walk(timeStep)

		#write in file
		resultFile.write(str(agents[i].id) + ";" + str(agents[i].position.x) + ";" + str(agents[i].position.y) + ";" + str(agents[i].position.z) + "\n")

		#verify agent position, in relation to the goal. If arrived, bye
		dist = Vector3.Distance(agents[i].goal.position, agents[i].position)
		#print(agents[i].id, " -- Dist: ", dist, " -- Radius: ", agents[i].radius, " -- Agent: ", agents[i].position.x, agents[i].position.y)
		#print(agents[i].speed.x, agents[i].speed.y)
		if dist < agents[i].radius / 4:
			agentsToKill.append(i)

		i += 1

	#die!
	if len(agentsToKill) > 0:
		for i in range(0, len(agentsToKill)):
			agents.pop(agentsToKill[i])
	print("Simulation Frame:", simulationFrame, end='\r')
	simulationFrame += 1

simulationTime = (simulationFrame+1) * timeStep
print(f'Total Simulation Time: {simulationTime} "seconds. ({simulationFrame+1} frames)')

#close file
resultFile.close()
