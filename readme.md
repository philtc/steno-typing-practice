This is a fork of Isaiah Grace's typing practice program.

# steno-typing-practice
This is a simple terminal program for practicing long-form typing with stenography.
 ![Screenshot](/img/main-1.png)

## Features
- Long-form typing (e.g. novels, books etc you can add yourself)
- Offline (no network required)
- Very few dependancies
- Text User Interface (TUI)
- Cursor highlights the current position
- Last word typed is displayed for visual feedback (useful for multi stroke words)
- Characters can be 'skipped' by pressing (or chording) the tab key
- Typed text is dimmed
- Skipped characters are underlined
- Difficult words can be saved to a text file

## Dependancies
The main program requires:
- python 3
- ncurses

(Optional) The freq and plot programs require:
- matplotlib
- numpy

## Usage
Download this repository:  
```git clone https://github.com/philtc/steno-typing-practice```  
  
Go to the new directory:  
```cd steno-typing-practice```  
  
(Optional) Put the source text you want to use in the books folder.  
  
Start the program:  
```python typing.py```  
  
Save difficult words by pressing ```CTRL-P```. These words will be saved to the savedWords.txt file.  
  
Exit with the ```esc``` key.