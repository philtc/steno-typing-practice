import matplotlib.pyplot as plt
import json
import os
import numpy as np

files = [f for f in os.listdir('books') if f[-6:] == '.speed']

if not files:
    print("No files with the .speed extension found")
    exit()

print('Please select a .speed file to plot')
for idx, file in enumerate(files, start=1):
    print(idx, '-', file)

choice = files[int(input()) - 1]

data = []
with open(choice,'r') as f:
    while (line := f.readline()):
        data.append(json.loads(line))

x = []
y = []
for datum in data:
    x.append(int(datum['line']))
    y.append(int(datum['WPM']))


# Plot the data
fig = plt.figure()

ax = fig.add_subplot(1,1,1)
ax.plot(x,y,'.')


m, b = np.polyfit(x, y, 1)
y_fit = [m * xi + b for xi in x]
#ax.plot(x,y_fit)

plt.xlabel('paragraph')
plt.ylabel('WPM')

plt.ylim((0,100))

major_ticks = np.arange(0,101,10)
minor_ticks = np.arange(0,101,5)

ax.set_yticks(major_ticks)
#ax.set_yticks(minor_ticks, minor=True)
ax.grid(which='both')                         

plt.show()
