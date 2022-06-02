import numpy as np
import matplotlib
import matplotlib.pyplot as plt

data = []
mapSizeX = 20
mapSizeY = 20
cellSize = 2

#read the config file to get the map size
lineCount = 1
for line in open("Input/config.txt", "r"):
	if '#' in line:
		continue
	elif lineCount == 3:
		#cellSize
		cellSize = int(line)
	elif lineCount == 4:
		#size of the scenario
		sp = line.split(',')
		mapSizeX = int(sp[0])
		mapSizeY = int(sp[1])
	lineCount += 1

#open file to read
for line in open("resultCellFile.txt"):
	stripLine = line.replace('\n', '')
	strip = stripLine.split(',')
	dataTemp = []

	for af in strip:
		dataTemp.append(float(af))

	data.append(dataTemp)

harvest = np.array(data)

print(harvest)

fig, ax = plt.subplots()
im = ax.imshow(harvest)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(mapSizeX/cellSize))
ax.set_yticks(np.arange(mapSizeY/cellSize))

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(int(mapSizeX/cellSize)):
	for j in range(int(mapSizeY/cellSize)):
		text = ax.text(j, i, harvest[i, j],
						ha="center", va="center", color="w")

ax.set_title("HeatMap")
fig.tight_layout()
plt.show()