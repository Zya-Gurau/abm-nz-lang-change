import csv
import matplotlib.pyplot as plt

with open('prop_speaking.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    data=[]
    isFirst = True
    for row in spamreader:
        if isFirst == False:
            data.append(float(row[0]))
        isFirst = False

plt.plot(data)
plt.savefig('graph_two.png')
plt.show()