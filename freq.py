#!/usr/bin/python3

import matplotlib.pyplot as plt
import json
import os
import numpy as np
import pprint as pp

files = [f for f in os.listdir('books') if f[-6:] == '.speed']

if not files:
    print("No files with the .speed extension found")
    exit()

print('Please select a .speed file to plot')
for idx, file in enumerate(files, start=1):
    print(idx, '-', file)

choice = 'books/' + files[int(input()) - 1]

data = []
with open(choice,'r') as f:
    while (line := f.readline()):
        data.append(json.loads(line))

last = data[-1]
typoFreq = [0] * 256
for i,charFreq in enumerate(last['charFreq']):
    if charFreq == 0:
        continue
    typoFreq[i] = round(last['typos'][i] / charFreq,4)

typos = []

for char,count in enumerate(last['typos']):
    if count == 0:
        continue
    
    typos.append((chr(char),
                  typoFreq[char],
                  count,
                  last['charFreq'][char],
                  (count * 1000) + (900 - last['charFreq'][char])))
    
typos.sort(key=lambda x:x[1],reverse=True)
typos.sort(key=lambda x:x[-1],reverse=True)

print("(char,  % miss, count, freq, score)")
for typo in typos:
    if typo[3] < 5:
        continue
    print("(   {},{:>8.2%},   {:>3d},  {:>3d}, {:>5d})".format(typo[0],typo[1],typo[2],typo[3],typo[4]))

