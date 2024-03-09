import threading
import time

class Vacuum(threading.Thread):
    def __init__(self, squareA, squareB, methodForChangeImage):
        threading.Thread.__init__(self)
        self.perception = ""
        self.action = "NOTHING-LEFT"
        self.state = "WAIT-LEFT"
        self.position = "LEFT"
        self.squareA = squareA
        self.methodForChangeImage = methodForChangeImage
        self.squareB = squareB
        self.model_states = {
            "WAIT-LEFT":  { 
                "NOTHING-LEFT": 
                    { "CLEAN": "CLEAN-LEFT", "DIRTY": "DIRTY-LEFT" }
                },
            "WAIT-RIGHT":  { 
                "NOTHING-RIGHT": 
                    { "CLEAN": "CLEAN-RIGHT", "DIRTY": "DIRTY-RIGHT" }
                },
            "CLEAN-LEFT":  { 
                "MOVING-RIGHT": 
                    { "CLEAN": "WAIT-RIGHT", "DIRTY": "DIRTY-RIGHT" }
                },
            "CLEAN-RIGHT":  { 
                "MOVING-LEFT": 
                    { "CLEAN": "WAIT-LEFT", "DIRTY": "DIRTY-LEFT" }
                },
            "DIRTY-LEFT":  { 
                "CLEAN-LEFT": 
                    { "CLEAN": "WAIT-LEFT", "DIRTY": "DIRTY-LEFT" }
                },
            "DIRTY-RIGHT":  { 
                "CLEAN-RIGHT": 
                    { "CLEAN": "WAIT-RIGHT", "DIRTY": "DIRTY-RIGHT" }
                }
        }
        self.model_actions = {
            "WAIT-LEFT":  "NOTHING-LEFT" ,
            "WAIT-RIGHT":  "NOTHING-RIGHT",
            "CLEAN-RIGHT":  "MOVING-LEFT",
            "CLEAN-LEFT":  "MOVING-RIGHT",
            "DIRTY-LEFT":  "CLEAN-LEFT",
            "DIRTY-RIGHT":  "CLEAN-RIGHT"
        }
        self.stop_event = threading.Event()
    def stop(self):
             self.stop_event.set()
    def run(self):
        while not self.stop_event.is_set():
            self.readPerception()
            self.updateStatus()
            self.doAction()
            self.updateVisualGraphics()
            time.sleep(1)
    def updateStatus(self):
            if self.perception != "":
                print(self.state,self.action,self.perception, "---- "+self.position )
                try:
                    self.state = self.model_states[self.state][self.action][self.perception]
                except KeyError:
                    self.state = "RESET"
            self.perception = ""
            if self.state == "RESET":
                self.state = "WAIT-LEFT"
    def readPerception(self):
        if self.position == "LEFT":
             self.perception = "CLEAN" if self.squareA.isCleaned else "DIRTY"
        else:
             self.perception = "CLEAN" if self.squareB.isCleaned else "DIRTY"
    def doAction(self):
        self.action = self.model_actions[self.state];
        if self.action == "NOTHING-LEFT":
            print("NO HACE NADA")
        elif self.action == "NOTHING-RIGHT":
            print("NO HACE NADA")
        elif self.action == "CLEAN-LEFT":
            print("LIMPIANDO IZQUIERDA")
            self.squareA.isCleaned = True
        elif self.action == "CLEAN-RIGHT":
            print("LIMPIANDO DERECHA")
            self.squareB.isCleaned = True
        elif self.action == "MOVING-LEFT":
            print("MOVIENDOSE A LA IZQUIERDA")
            self.position = "LEFT"
        elif self.action == "MOVING-RIGHT":
            print("MOVIENDOSE A LA DERECHA")
            self.position = "RIGHT"
    def updateVisualGraphics(self):
         self.methodForChangeImage("LEFT", 0 if self.squareA.isCleaned else 1)
         self.methodForChangeImage("RIGHT", 0 if self.squareB.isCleaned else 1)
         self.methodForChangeImage(self.position, 2)
