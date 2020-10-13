#! /usr/bin/python

# Isaiah Grace
# 17 Sep 2020

import os
import json
import curses
import time
import textwrap

class Typing():
    def __init__(self):
        pass

    def start(self):
        curses.wrapper(self._start)

    def _start(self, stdscr):
        ## initilize the curses environment, and create our windows
        stdscr.clear()
        self.infoWin = curses.newwin(5, curses.COLS - 1, 0, 0)
        self.textWin = curses.newwin(curses.LINES - 6, curses.COLS - 1, 6, 0)

        # These two lines will allow full escape sequences to be read in by getkey
        # and will reduce the delay to 1ms for pressing ESC key
        self.textWin.keypad(True)
        #curses.set_escdelay(1) # TODO: Uncomment this when 3.9 is released for Arch
        
        self.infoHalf = curses.COLS // 2

        self.printInfoStatic()
        
        ## prompt user to select the practice text
        # find .txt files in the current directory
        dirFiles = os.listdir()
        files = [f for f in dirFiles if f[-4:] == '.txt']

        if not files:
            self.textWin.addstr(0,0,'please supply at least one .txt file in the current directory')
            self.textWin.addstr(1,0,'press any key to exit')
            self.textWin.noutrefresh()
            curses.doupdate()
            self.textWin.getkey()
            return

        # prompt the user for a selection:
        self.textWin.addstr(0,0,'Please select a practice text:')
        for idx, file in enumerate(files, start=1):
            self.textWin.addstr(idx , 0, str(idx) + ' - ' +  str(file))

        self.textWin.addstr(len(files) + 1, 0, 'enter a number:')
        self.textWin.noutrefresh()
        curses.doupdate()
        choice = files[int(self.textWin.getkey()) - 1]

        self.file = open(choice, 'r')
        self.fileName = choice
        self.progressFile = choice + '.progress'
        
        self.textWin.clear()
        self.textWin.addstr(0, 0, 'Using ' + choice + ' as practice text')
        
        ## read in a progress file, or start from beginning if none exists
        if self.progressFile in dirFiles:
            self.textWin.addstr(2,0,'Found progress file')
            with open(self.progressFile,'r') as f:
                self.progress = json.load(f)
        else:
            self.textWin.addstr(2,0,'Did not find a progress file, starting from the begining')
            self.resetProgress()
            
        ## read ahead in the practice text to the current position as defined in the progress dict
        for i in range(self.progress['line']):
            # Its totally okay if we read off the end of the file
            # we'll just read in empty strings, and our typingLoop function will take care of it
            self.file.readline()
        
        self.textWin.addstr(4,0,'Ready to start at paragraph {:03d}'.format(self.progress['line']))
        self.textWin.addstr(6,0,'Press any key to begin')
        self.textWin.noutrefresh()
        curses.doupdate()
        self.textWin.getkey()

        # Start the main typing loop, this will run until the user is done typing
        try:
            self.typingLoop()
        finally:
            # This finally makes sure that we always save the progress when exiting
            self.saveProgress()
        

    def typingLoop(self):
        typing = True
        while(typing):
            line, typing = self.readLine()
            if not typing:
                break

            self.progress['startTime'] = time.time()
            self.progress['oldChars'] = self.progress['char']
            self.progress['oldErrors'] = len(self.progress['errors'])
            self.progress['words'] = 0
            self.printInfoDynamic()

            self.textWin.clear()
            self.textWin.addstr(0,0,line)
            self.textWin.move(0,0)
        
            if self.progress['char'] != 0:
                self.printProgress(line)
                
            self.textWin.noutrefresh()
            curses.doupdate()
        
            for char in line[self.progress['char']:]:
                # If this is the last char in the line,
                # save the speed stats so that the typist can look at the screen before the next paragraph
                if self.progress['char'] == len(line) - 1:
                    self.writeInfo()
                    
                # Because we used textwrap, we may have \n in our line
                if char == '\n':
                    self.textWin.addch('\n')
                    self.textWin.noutrefresh()
                    curses.doupdate()
                    self.progress['char'] = self.progress['char'] + 1
                    continue
                
                typo = False
                while (key := self.textWin.getkey()) != char:
                    typo = True
                    if key == '\x1b':
                        raise KeyboardInterrupt('Escape closed the program')
                if typo:
                    style = curses.A_STANDOUT
                    self.progress['errors'].append(self.progress['char'])
                else:
                    style = curses.A_BOLD
                
                self.progress['char'] = self.progress['char'] + 1

                if char == ' ':
                    self.progress['words'] = self.progress['words'] + 1
                
                self.textWin.addch(char, style)
                
                # print some things to the info window
                self.printInfoDynamic()
            
                self.textWin.noutrefresh()
                curses.doupdate()

            # We've completed a line, reflect this in the progress dict    
            self.progress['line'] = self.progress['line'] + 1
            self.progress['char'] = 0
            self.progress['oldChars'] = 0,
            self.progress['words'] = 0,
            self.progress['errors'] = []

            # save the progress for good measure
            self.saveProgress()
            

    def readLine(self):
        line = self.file.readline()
        if not line:
            self.textWin.clear()
            self.textWin.addstr(0,0,"Congratulations! You've reached the end of the text!")
            self.textWin.addstr(1,0,"press r to restart the practice text, press any other key to save and exit.")
            self.textWin.noutrefresh()
            curses.doupdate()
            char = self.textWin.getkey()
            if char == 'r' or char == 'R':
                self.resetProgress()
                self.file.seek(0)
                line = self.file.readline()
            else:
                return (line, False)
        line = ' \n'.join(textwrap.wrap(line,curses.COLS - 3))
        return (line, True)

        
    def resetProgress(self):
        self.progress = {'line': 0,
                         'char': 0,
                         'oldChars': 0,
                         'words': 0,
                         'errors': [],
                         'startTime': 0
                         }
        
            
    def saveProgress(self):
        with open(self.progressFile, 'w') as f:
            json.dump(self.progress, f)


    def writeInfo(self):
        info = {}
        info['line'] = self.progress['line']
        info['chars'] = self.progress['char'] - self.progress['oldChars']
        info['words'] = self.progress['words']
        info['errors'] = len(self.progress['errors']) - self.progress['oldErrors']
        info['accuracy'] = round(self.getAccuracy(), 2)
        info['CPM'] = round(self.getCPM(), 2)
        info['WPM'] = round(self.getWPM(), 2)
        info['time'] = round(time.time() - self.progress['startTime'], 3)
        
        with open(self.fileName + '.speed', 'a') as f:
            json.dump(info, f)
            f.write('\n')

        
    def getAccuracy(self):
        if self.progress['char'] == 0 or len(self.progress['errors']) == 0:
            return 100
        return 100 - (100 * len(self.progress['errors']) / self.progress['char'])


    def getCPM(self):
        return (self.progress['char'] - self.progress['oldChars']) / ((time.time() - self.progress['startTime'] + 0.001) / 60)

    
    def getWPM(self):
        return self.progress['words'] / ((time.time() - self.progress['startTime'] + 0.001) / 60)

    
    def printInfoStatic(self):
        # The left column of info:
        self.infoWin.addstr(0, 0, 'Paragraph:')
        self.infoWin.addstr(1, 0, 'Character:')
        self.infoWin.addstr(2, 0, 'Errors   :')
        
        # The right column of info:
        self.infoWin.addstr(0, self.infoHalf, 'Accuracy:')
        self.infoWin.addstr(1, self.infoHalf, 'Time    :')
        self.infoWin.addstr(2, self.infoHalf, 'CPM     :')
        self.infoWin.addstr(3, self.infoHalf, 'WPM     :')
        
        self.infoWin.noutrefresh()

        
    def printInfoDynamic(self):
        # Save the cursor position so we can put it back where it belongs when were done
        y,x = self.textWin.getyx()

        self.infoWin.addstr(0, 12, '{:03d}'.format(self.progress['line']))
        self.infoWin.addstr(1, 12, '{:03d}'.format(self.progress['char']))
        self.infoWin.addstr(2, 12, '{:03d}'.format(len(self.progress['errors'])))
        
        self.infoWin.addstr(0, self.infoHalf + 11, '{:05.2f}%'.format(self.getAccuracy()))
        self.infoWin.addstr(1, self.infoHalf + 11, time.strftime("%M:%S", time.gmtime(time.time() - self.progress['startTime'])))
        self.infoWin.addstr(2, self.infoHalf + 11, '{:03.0f}'.format(self.getCPM()))
        self.infoWin.addstr(3, self.infoHalf + 11, '{:03.0f}'.format(self.getWPM()))
                            
        # Set the cursor position back to what it was before we added some text
        self.textWin.move(y,x)
        self.infoWin.noutrefresh()
        self.textWin.noutrefresh()


    def printProgress(self, line):
        for i, char in enumerate(line[:self.progress['char']]):
            if i in self.progress['errors']:
                style = curses.A_STANDOUT
            else:
                style = curses.A_BOLD
            self.textWin.addch(char, style)


    
if __name__ == '__main__':
    typing = Typing()
    typing.start()
