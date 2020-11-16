# typing-practice
This is a very simple curses based typing practice program. Supply a source text and then type it our paragraph by paragraph to practice touch-typing. I wrote this myself because the web-based ones didn't have good support for typing out long source texts (like full books), and I wanted to play around with curses.

# Windows
This python program uses ncurses to create a text user interface (TUI). To run on a Windows OS, I recommend using the Windows Subsystem for Linux (WSL). However my brother did get this to work directly from a windows command line. **In windows you will have to use ESC to quit.** There is a 1 second delay before the program exits. This is a relic of old tele-types with slow baud rates. It's just one of those things that never changed.

# Linux
Just type ```./typing.py``` or ```python typing.py``` and go! Use ESC or CTRL+C to exit.

# Setup
Be sure to supply a .txt file as the source text you will be typing. You can check out the mobydick branch to see my progress and use it as an example source file (```git checkout mobydick```). Simply delete the .progress file to re-start the source text from the beginning.

# typing interface setup
* you don't have to press backspace when you type the wrong key
* you do have to press the right key to continue
* typed text appears in a different color
* the cursor is highlighted and highlights the current position
* errors are displayed after you type them
 
