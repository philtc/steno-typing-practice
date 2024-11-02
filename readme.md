 ![Screenshot](/img/main-1.png)

This is a fork of Isaiah Grace's typing practice program.

# steno-typing-practice
This is a simple terminal program for practicing typing with stenography.

## Features
- Long-form typing based on written text of your choosing
- Offline
- Very few dependancies
- Text User Interface (TUI)
- Cursor highlights the current position
- Last word typed is displayed for visual feedback (useful for multi stroke words)
- Characters can be 'skipped' by pressing (or chording) the TAB key
- Typed text is dimmed
- Skipped characters are underlined

## Dependancies
The main program requires:
- python 3
- ncurses

(Optional) The freq and plot programs require:
- matplotlib
- numpy

## Usage
Download this repository  
```git clone https://github.com/philtc/steno-typing-practice```  
Change to the directory you just downloaded  
```cd steno-typing-practice```  
(Optional) Put the source text you want to use in the books folder.  
Start the program  
```python typing.py```