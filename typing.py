# Isaiah Grace
# 14 Sep 2020

import os
import json
import textwrap

# save the progress dict to a file
def saveProgress(choice, progress):
    # Save the progress thus far
    with open(choice + '.progress','w') as f:
        f.write(json.dumps(progress))


# find .txt files in the current directory
dirFiles = os.listdir()
files = [f for f in dirFiles if f[-4:] == '.txt']

if not files:
    print('please supply at least one .txt file in the current directory')
    exit()

# prompt the user for a selection:
print('Please select a practice text:')
choice = 1
for file in files:
    print(choice, '-', file)

choice = files[int(input('enter number: ')) - 1]

print('Using', choice, 'as practice text')

print('Searching for a progress file...')
if choice + '.progress' in dirFiles:
    print('Found progress file')
    with open(choice + '.progress','r') as f:
        progress = json.load(f)
else:
    print('Did not find a progress file, starting from the begining')
    progress = {'line' : 0,
                'char' : 0}
    
file = open(choice,'r')

# Move ahead to the current line
for i in range(progress['line']):
    file.readline()

rows, columns = [int(x) for x in os.popen('stty size', 'r').read().split()]
if columns > 70:
    columns = 70
    
[print(line) for line in textwrap.wrap(file.readline(),width=columns)]


file.close()
saveProgress(choice, progress)
