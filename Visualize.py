# importing the matplotlib library
import matplotlib.pyplot as plt
  
# values on x-axis
x = [11]
# values on y-axis
y = [19]

#open file to read
readFile = open("resultFile.csv", "r")

for line in open("resultFile.csv"):
    csv_row = line.split(';')
    x.append(float(csv_row[1]))
    y.append(float(csv_row[2]))


readFile.close()
  
plt.axis([0, 20, 0, 20])

# naming the x and y axis
plt.xlabel('x - axis')
plt.ylabel('y - axis')
  
# plotting a line plot with it's default size
plt.plot(x, y, 'r*')
plt.show()