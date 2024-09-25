import matplotlib.pyplot as plt
import numpy as np
import csv


gen_one_data= []
gen_two_data = []
with open('gen_one.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    
    isFirst = True
    for row in spamreader:
        if isFirst == False:
            gen_one_data.append(float(row[1]))
        isFirst = False

with open('gen_two.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    
    isFirst = True
    for row in spamreader:
        if isFirst == False:
            gen_two_data.append(float(row[1]))
        isFirst = False

xbins = np.arange(0,1, 0.001)

plt.hist(gen_two_data, xbins,histtype='step')
plt.hist(gen_one_data, xbins,histtype='step')

plt.show()
