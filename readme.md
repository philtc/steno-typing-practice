# book-type
chose book txt file in current working directory and then load progress from progress file

# typing interface setup
you don't have to press backspace when you type the wrong key
you do have to press the right key to continue
typed text apears in green
the cursor is blue and highlights the current position
the text yet to be typed is red


# which language to use?
 1. C, fast, and fun to program in. But verbose...
 2. C++, a little easier to manage data structures
 3. python, very easy to type, but not as fun...
 
ideally this program could run on my phone inside the termux environment...
 
# C 

## main
1. run initial setup
2. parse args??
3. run menu function...
4. start the typing environment
	
should I parse args, or just have a menu...
I think just making a menu is the easiest way to go...

## menu:
	list text source files in folder
	take a selection from the user and return the file pointer to the main function
	
## typing:
	will be the main environment managing the local buffer
	reading from the file, both progress and typing text.
	saving progress to a file
	

