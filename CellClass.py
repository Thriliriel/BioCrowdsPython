import math
import random
from Vector3Class import Vector3
from MarkerClass import MarkerClass

class CellClass:
    def __init__(self, id, position, cellRadius, density = 0.65, markers = []):
        self.id = id
        self.position = position
        self.markers = markers
        self.density = density
        self.markerRadius = 0.1
        self.cellRadius = cellRadius
        self.neighborCells = []
        self.qntMarkers = 0

    def DartThrow(self):
        #flag to break the loop if it is taking too long (maybe out of space)
        flag = 0
        #print("Qnt create: ", self.qntMarkers)
        i = 0
        while i < self.qntMarkers:
            x = random.uniform(self.position.x, self.position.x + self.cellRadius)
            y = random.uniform(self.position.y, self.position.y + self.cellRadius)

            #print(self.id, x, y)

            #check distance from other markers to see if can instantiante
            canInst = True
            for m in range (0, len(self.markers)):
                distance = Vector3.Distance(self.markers[m].position, Vector3(x, y, 0))
                if distance < self.markerRadius:
                    canInst = False
                    break

            #can i?
            if canInst:
                self.markers.append(MarkerClass(Vector3(x, y, 0)))
                flag = 0
            #else, try again
            else:
                flag += 1
                i -= 1

            #if flag is above qntMarkers (*2 to have some more), break;
            if flag > self.qntMarkers * 2:
                #reset flag
                flag = 0
                print(self.id)
                break

            i += 1

    def CreateMarkers(self):
        self.density *= (self.cellRadius) / (2.0 * self.markerRadius)
        self.density *= (self.cellRadius) / (2.0 * self.markerRadius)
        self.qntMarkers = math.floor(self.density)
        #print("Self - " + str(self.qntMarkers))
        self.DartThrow()

    #find the neighbor cells
    def FindNeighbor(self, allCells):
        #for each cell, check if the distance is lower or equal the hyp of the drawn square between the center of the cells
        for i in range(len(allCells)):
            distance = Vector3.Distance(self.position, allCells[i].position)

            #if distance is zero, it is the same cell, ignore it
            if distance > 0:
                #now, check if the distance is inside the boundaries 
                #(for example: cellRadius = 2, max distance = sqrt(8) = 2.sqrt(2))
                if distance <= 0.1 + math.sqrt(math.pow(self.cellRadius, 2) + math.pow(self.cellRadius, 2)):
                    self.neighborCells.append(allCells[i])

        #print(self.id, len(self.neighborCells))