import csv
import matplotlib.pyplot as plt
data=[]
x_points = []
with open('prop_speaking.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    
    isFirst = True
    for row in spamreader:
        if isFirst == False:
            data.append(float(row[0]))
        isFirst = False

j = 0
for i in range(0,50):
    if i < 25:
        j+=1
    if i >= 25:
        j+=1
    x_points.append(j)

    


plt.plot(x_points, data)
plt.savefig('graph_two.png')
plt.show()