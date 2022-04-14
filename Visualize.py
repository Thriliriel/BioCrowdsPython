# importing the matplotlib library
import matplotlib.pyplot as plt
  
# values on x-axis
x = []
# values on y-axis
y = []

#goals
for line in open("Input/goals.txt", "r"):
	if '#' in line:
		continue

	#create goal
	gl = line.split(',')
	x.append(float(gl[1]))
	y.append(float(gl[2]))

#open file to read
for line in open("resultFile.csv"):
    csv_row = line.split(';')
    x.append(float(csv_row[1]))
    y.append(float(csv_row[2]))
  
plt.axis([0, 20, 0, 20])

# naming the x and y axis
plt.xlabel('x - axis')
plt.ylabel('y - axis')
  
# plotting a line plot with it's default size
plt.plot(x, y, 'r*')
plt.show()