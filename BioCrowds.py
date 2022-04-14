from AgentClass import AgentClass
from Vector3Class import Vector3
from CellClass import CellClass
from MarkerClass import MarkerClass

#markers density
PORC_QTD_Marcacoes = 0.8

#50FPS
timeStep = 0.02

#agents
agents:list[AgentClass] = []

#cells
cells:list[CellClass] = []

#size of each square cell (Ex: 2 -> cell 2x2)
cellSize = 2

#goal
goal = Vector3(5, 19, 0)

#size of the scenario
mapSize = Vector3(20, 20, 0)

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
		cells[i].CreateMarkers()
		#print("Qnt created: ", len(cells[i].markers))

#save markers in file
def SaveMarkers():
	markerFile = open("markers.csv", "w")
	for i in range(0, len(cells)):
		for j in range(0, len(cells[i].markers)):
			markerFile.write(cells[i].id + ";" + str(cells[i].markers[j].position.x) + ";" + str(cells[i].markers[j].position.y) + ";" + str(cells[i].markers[j].position.z) + "\n")
	markerFile.close()

CreateMap()
CreateMarkers()
SaveMarkers()

#for each cell, find its neighbors
for i in range(0, len(cells)):
	cells[i].FindNeighbor(cells)

#create one agent
agents.append(AgentClass(1, goal, 2, 1.2, Vector3(12, 0, 0)))
agents.append(AgentClass(2, goal, 2, 1.2, Vector3(14, 6, 0)))

#for each agent, find its initial cell
for i in range(0, len(agents)):
	minDis = 5
	for c in range(0, len(cells)):
		dist = Vector3.Distance(agents[i].position, cells[c].position)
		if dist < minDis:
			minDis = dist
			agents[i].cell = cells[c]

#open file to write
resultFile = open("resultFile.csv", "w")

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

	for i in range(0, len(cells)):
		for j in range(0, len(cells[i].markers)):
			if cells[i].markers[j].taken:
				print("Error taken")
			if cells[i].markers[j].owner is not None:
				print("Error owner")
	
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
		agentGoal = agents[i].goal
		agentMarkers = agents[i].markers

		#vector for each marker
		for j in range(0, len(agentMarkers)):
			#add the distance vector between it and the agent
			#print (agents[i].position, agentMarkers[j].position)
			newX = agentMarkers[j].position.x - agents[i].position.x
			newY = agentMarkers[j].position.y - agents[i].position.y
			newZ = agentMarkers[j].position.z - agents[i].position.z
			agents[i].vetorDistRelacaoMarcacao.append(Vector3(newX, newY, newZ))

		#print("total", len(agents[i].vetorDistRelacaoMarcacao))
		#calculate the movement vector
		agents[i].CalculateMotionVector()
  
		print(agents[i].m)
        #calculate speed vector
		agents[i].CalculateSpeed()

		#walk
		agents[i].Walk(timeStep)

		#write in file
		resultFile.write(str(agents[i].id) + ";" + str(agents[i].position.x) + ";" + str(agents[i].position.y) + ";" + str(agents[i].position.z) + "\n")

		#verify agent position, in relation to the goal. If arrived, bye
		dist = Vector3.Distance(agents[i].goal, agents[i].position)
		print(agents[i].id, " -- Dist: ", dist, " -- Radius: ", agents[i].radius, " -- Agent: ", agents[i].position.x, agents[i].position.y, [goal.x, goal.y, goal.z])
		#print(agents[i].speed.x, agents[i].speed.y)
		if dist < agents[i].radius / 4:
			agentsToKill.append(i)

		i += 1

	#die!
	if len(agentsToKill) > 0:
		for i in range(0, len(agentsToKill)):
			agents.pop(agentsToKill[i])


#close file
resultFile.close()