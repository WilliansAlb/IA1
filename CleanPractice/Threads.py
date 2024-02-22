import threading
import time
import tkinter as tk
class UserThread(threading.Thread):
    
    def __init__(self,squareA,squareB):
        threading.Thread.__init__(self)
        self.key = None
        self.squareA = squareA
        self.squareB = squareB
        self.root = None
        self.button_clean = None
        self.button_dirty = None
        self.button_vacuum = None
        self.buttonA = None
        self.buttonB = None
        self.size = 500

    def run(self):
        self.root = tk.Tk()
        self.root.title("Aspiradora")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.button_clean = tk.PhotoImage(file="square.png")
        self.button_dirty = tk.PhotoImage(file="dirty.png")
        self.button_vacuum = tk.PhotoImage(file="vacuum.png")
        self.buttonA = tk.Button(self.root, text="A", image=self.button_vacuum, width=self.size, height=self.size, command=lambda: self.select('A',self.squareA))
        self.buttonB = tk.Button(self.root, text="B", image=self.button_clean, width=self.size, height=self.size, command=lambda: self.select('B',self.squareB))
        self.buttonA.pack(side='left')
        self.buttonB.pack(side='left')
        self.root.mainloop()
    
    def on_closing(self):
        print("closing")
        self.key = "Q"
        self.root.destroy()
    
    def select(self, key, squareToDirt):
        self.key = key
        self.changeImage(key,1)
        print('dirtying '+key)
        squareToDirt.isCleaned = False
    
    def changeImage(self, square, state):
        image = self.button_clean
        if state == 1:
            image = self.button_dirty
        elif state == 2:
            image = self.button_vacuum 
        if square == 'A':
            if self.buttonA:
                self.buttonA.config(image=image)
        elif square == 'B':
            if self.buttonB:
                self.buttonB.config(image=image)

class VacuumThread(threading.Thread):
    def __init__(self, userThread, squareA, squareB, vacuum):
        threading.Thread.__init__(self)
        self.squareA = squareA
        self.squareB = squareB
        self.vacuum = vacuum
        self.userThread = userThread;

    def run(self):
        while True:
            if self.userThread.key == 'Q':
                break
            if self.vacuum.isStupid:
                self.vacuum.verifiedStupid(self.squareA, self.squareB, self.userThread)
            else:
                self.vacuum.verifiedIntelligence(self.squareA, self.squareB, self.userThread)
            time.sleep(2)