#! /usr/bin/python

# Isaiah Grace
# 14 Sep 2020

import os
import json
import textwrap
import curses

# save the progress dict to a file
def saveProgress(choice, progress):
    # Save the progress thus far
    with open(choice + '.progress','w') as f:
        f.write(json.dumps(progress))

def mainCurses(stdscr, choice):
    # check for a progress file, if non, start from the begining
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

    # Figure out a good size for the text
    
    #formatLines = textwrap.wrap(file.readline(),width=columns)

    stdscr.clear()

    # create a window at the top to show progress, WPM, accuracy, etc
    infoWin = curses.newwin(5, curses.COLS - 1, 0, 0)
    infoWin.addstr(0,0,'info window')
    infoWin.noutrefresh()
    
    # create the window that will display the text 
    textWin = curses.newwin(curses.LINES - 6, curses.COLS - 1, 6, 0)

    # Main loop of the typing program
    while(True):
        line = file.readline()
        textWin.addstr(0,0,line)

        if progress['char'] != 0:
            textWin.addstr(0,0,line[:progress['char']], curses.A_BOLD)
            
        for char in line[progress['char']:-1]:
            while textWin.getkey() != char:
               pass
                       
            progress['char'] = progress['char'] + 1
            textWin.addstr(0,0,line[:progress['char']], curses.A_BOLD)
            textWin.noutrefresh()
            curses.doupdate()

        # We've completed a line, reflect this in the progress dict    
        line = file.readline()
        progress['line'] = progress['line'] + 1
        progress['char'] = 0
                                                
    file.close()
    saveProgress(choice, progress)



if __name__ == '__main__':
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

    curses.wrapper(mainCurses,choice)
    exit()
    
