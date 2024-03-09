import tkinter as tk
from Square import Square
from Vacuum import Vacuum

def main():
	global key, button_clean, button_dirty, button_vacuum, buttonA, buttonB 
	root = tk.Tk()
	root.title("Aspiradora")
	size = 500
	squareLeft = Square('LEFT')
	squareRight = Square('RIGHT')
	button_clean = tk.PhotoImage(file="./../square.png")
	button_dirty = tk.PhotoImage(file="./../dirty.png")
	button_vacuum = tk.PhotoImage(file="./../vacuum.png")
	buttonA = tk.Button(root, text="A", image=button_vacuum, width=size, height=size, command=lambda: select('LEFT',squareLeft))
	buttonB = tk.Button(root, text="B", image=button_clean, width=size, height=size, command=lambda: select('RIGHT',squareRight))
	vacuum = Vacuum(squareA=squareLeft, squareB=squareRight, methodForChangeImage=changeImage)
	buttonA.pack(side='left')
	buttonB.pack(side='left')
	vacuum.start()
	root.mainloop()
	vacuum.stop()
	vacuum.join()
    
def select(keyPressed, squareToDirt):
    global key, button_clean, button_dirty, button_vacuum
    key = keyPressed
    changeImage(key,1)
    print('dirtying '+key)
    squareToDirt.isCleaned = False
        
def changeImage(square, state):
	global key, button_clean, button_dirty, button_vacuum, buttonA, buttonB
	image = button_clean
	if state == 1:
		image = button_dirty
	elif state == 2:
		image = button_vacuum 
	if square == 'LEFT':
		if buttonA:
			buttonA.config(image=image)
	elif square == 'RIGHT':
		if buttonB:
			buttonB.config(image=image)

if __name__ == "__main__":
    main()