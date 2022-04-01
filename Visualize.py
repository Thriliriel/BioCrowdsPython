# importing the matplotlib library
import matplotlib.pyplot as plt
  
# values on x-axis
x = []
# values on y-axis
y = []

#open file to read
readFile = open("resultFile.csv", "r")

for line in open("resultFile.csv"):
    csv_row = line.split(';')
    x.append(csv_row[1])
    y.append(csv_row[2])


readFile.close()
  
# naming the x and y axis
plt.xlabel('x - axis')
plt.ylabel('y - axis')
  
# plotting a line plot with it's default size
print("Plot in it's default size: ")
plt.plot(x, y)
plt.show()