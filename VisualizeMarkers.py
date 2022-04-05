# importing the matplotlib library
import matplotlib.pyplot as plt
  
# values on x-axis
x = []
# values on y-axis
y = []

#open file to read
for line in open("markers.csv"):
    csv_row = line.split(';')

    #just one cell
    if csv_row[0] != "0-0":
        continue

    x.append(float(csv_row[1]))
    y.append(float(csv_row[2]))
    
#x = [3, 1, 2, 5]
#y = [5, 2, 4, 7]

plt.plot(x, y, 'r*')
plt.axis([0, 4, 0, 4])

#for i, j in zip(x, y):
#   plt.text(i, j+0.5, '({}, {})'.format(i, j))

plt.show()