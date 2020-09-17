#! /usr/bin/python

# Isaiah Grace
# 14 Sep 2020

import os
import json
import textwrap
import curses
import time

# save the progress dict to a file
def saveProgress(choice, progress):
    # Save the progress thus far
    with open(choice + '.progress','w') as f:
        f.write(json.dumps(progress))

def accuracy(progress):
    if progress['char'] == 0 or len(progress['errors']) == 0:
        return 100
    return 100 - (100 * len(progress['errors']) / progress['char'])

    
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
                    'char' : 0,
                    'errors': []}

    
    file = open(choice,'r')
    
    stdscr.clear()
    
    # Move ahead to the current line
    for i in range(progress['line']):
        if file.readline() == '':
            stdscr.addstr(0,0,'Progress file is at end of text')
            stdscr.addstr(1,0,'Press any key to exit')
            stdscr.refresh()
            stdscr.getkey()
            return

    # Figure out a good size for the text
    
    #formatLines = textwrap.wrap(file.readline(),width=columns)

    

    # create a window at the top to show progress, WPM, accuracy, etc
    infoWin = curses.newwin(5, curses.COLS - 1, 0, 0)
    infoWin.addstr(0,0,'Paragraph:')
    infoWin.addstr(1,0,'Character:')
    infoWin.addstr(2,0,'Errors   :')
    infoHalf = curses.COLS // 2
    infoWin.addstr(0, infoHalf, 'Accuracy:')
    infoWin.addstr(1, infoHalf, 'Time    :')
    infoWin.addstr(2, infoHalf, 'CPM     :')
    infoWin.addstr(3, infoHalf, 'WPM     :')
    infoWin.noutrefresh()
    
    # create the window that will display the text 
    textWin = curses.newwin(curses.LINES - 6, curses.COLS - 1, 6, 0)

        
    # Main loop of the typing program
    while(True):
        line = file.readline()
        if line == '':
            textWin.addstr(0,0,"Congratulations! You've reached the end of the text!")
            textWin.addstr(1,0,"press r to restart the progress file, press any other key to exit.")
            textWin.noutrefresh()
            curses.doupdate()
            char = textWin.getkey()
            if char == 'r' or char == 'R':
                progress['line'] = 0
                progress['char'] = 0
                progress['errors'] = []
            break
        
        textWin.addstr(0,0,line)
        infoWin.addstr(0,12,'{:03d}'.format(progress['line']))
        infoWin.addstr(1,12,'{:03d}'.format(progress['char']))
        infoWin.addstr(2,12,'{:03d}'.format(len(progress['errors'])))
        infoWin.addstr(0, infoHalf + 11, '{:05.2f}%'.format(accuracy(progress)))
        infoWin.noutrefresh()

        textWin.move(0,0)
        
        if progress['char'] != 0:
            for i, char in enumerate(line[:progress['char']]):
                if i in progress['errors']:
                    style = curses.A_STANDOUT
                else:
                    style = curses.A_BOLD
                textWin.addch(char, style)
                
            #textWin.addstr(0,0,line[:progress['char']], curses.A_BOLD)

        textWin.noutrefresh()
        curses.doupdate()

        progress['startTime'] = time.time()
        
        for char in line[progress['char']:-1]:
            try:
                typo = False
                while textWin.getkey() != char:
                    typo = True
            except KeyboardInterrupt as e:
                saveProgress(choice, progress)
                raise e
                       
            if typo:
                style = curses.A_STANDOUT
                progress['errors'].append(progress['char'])
            else:
                style = curses.A_BOLD
                
            progress['char'] = progress['char'] + 1

            textWin.addch(char, style)
            textWin.noutrefresh()

            # print some things to the info window
            y,x = textWin.getyx()
            infoWin.addstr(1,12,'{:03d}'.format(progress['char']))
            infoWin.addstr(2,12,'{:03d}'.format(len(progress['errors'])))
            infoWin.addstr(0, infoHalf + 11, '{:05.2f}%'.format(accuracy(progress)))
            infoWin.addstr(1, infoHalf + 11, time.strftime("%M:%S",time.gmtime(time.time() - progress['startTime'])))
            infoWin.noutrefresh()

            textWin.move(y,x)
            
            curses.doupdate()

        # We've completed a line, reflect this in the progress dict    
        progress['line'] = progress['line'] + 1
        progress['char'] = 0
        progress['errors'] = []

        infoWin.addstr(4,0,'you have finished a line. Press space twice to move to the next line. Press q to stop')
        infoWin.noutrefresh()
        curses.doupdate()
        
        infoWin.addstr(4,0,' ' * (curses.COLS - 2))
        
        textWin.clear()
                                                
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
        choice = choice + 1

    choice = files[int(input('enter number: ')) - 1]

    print('Using', choice, 'as practice text')

    curses.wrapper(mainCurses,choice)
        
