import threading
import time

class VendingMachine(threading.Thread):
    def __init__(self, initial, canvas, coin, pippu, porp, cabro, status):
        threading.Thread.__init__(self)
        self.perception = ""
        self.action = "SHOW-COIN"
        self.state = initial
        self.model_states = {
            "NO-COIN":  { 
                "SHOW-COIN": 
                    { "GET-COIN": "COIN" },
                },
            "COIN":  { 
                "SHOW-CODE": 
                    { "PORP": "SERVED-PORP", "PIPPU": "SERVED-PIPPU", "CABRO": "SERVED-CABRO" }
                },
            "SERVED-PORP":  { 
                "SERVING-PORP": 
                    { "SERVED": "NO-COIN" }
                },
            "SERVED-PIPPU":  { 
                "SERVING-PIPPU": 
                    { "SERVED": "NO-COIN" }
                },
            "SERVED-CABRO":  { 
                "SERVING-CABRO": 
                    { "SERVED": "NO-COIN" }
                }
        }
        self.model_actions = {
            "NO-COIN":  "SHOW-COIN" ,
            "COIN":  "SHOW-CODE",
            "SERVED-PORP":  "SERVING-PORP",
            "SERVED-PIPPU":  "SERVING-PIPPU",
            "SERVED-CABRO":  "SERVING-CABRO"
        }
        '''All code over is for the model, the code above es for visual components'''
        self.stop_event = threading.Event()
        self.canvas = canvas 
        self.coin = coin
        self.pippu = pippu
        self.porp = porp
        self.cabro = cabro
        self.status = status
    def stop(self):
             self.stop_event.set()
    def run(self):
        while not self.stop_event.is_set():
            self.updateStatus()
            self.doAction()
            '''The next call is for update Visual Graphics'''
            self.updateVisualGraphics()
            time.sleep(1)
    def updateStatus(self):
            if self.perception != "":
                print(self.state,self.action,self.perception)
                try:
                    self.state = self.model_states[self.state][self.action][self.perception]
                except KeyError:
                    self.state = "RESET"
            self.perception = ""
            if self.state == "RESET":
                self.state = "NO-COIN"
    def doAction(self):
        self.action = self.model_actions[self.state];
        if self.action == "SHOW-COIN":
            print("INSERTE MONEDA")
        elif self.action == "SHOW-CODE":
            print("ELIGE UNA BEBIDA")
        elif self.action == "SERVING-PORP":
            print("SIRVIENDO UNA PORP")
            self.perception = "SERVED"
        elif self.action == "SERVING-PIPPU":
            print("SIRVIENDO UNA PIPPU")
            self.perception = "SERVED"
        elif self.action == "SERVING-CABRO":
            print("SIRVIENDO UNA CABRO")
            self.perception = "SERVED"
    '''All code over is for the model, the code above es for visual components'''
    def reset(self):
        self.canvas.itemconfigure(self.porp, state="hidden")
        self.canvas.itemconfigure(self.pippu, state="hidden")
        self.canvas.itemconfigure(self.cabro, state="hidden")
        self.canvas.itemconfigure(self.coin, state="hidden")
    def updateVisualGraphics(self):
        if self.action == "SHOW-COIN":
            self.canvas.itemconfigure(self.status,text="INSERTE MONEDA")
            self.reset()
        elif self.action == "SHOW-CODE":
            self.canvas.itemconfigure(self.status,text="ELIGE UNA BEBIDA")
            self.canvas.itemconfigure(self.coin, state="normal")
        elif self.action == "SERVING-PORP":
            self.reset()
            self.canvas.itemconfigure(self.status,text="SIRVIENDO PORP")
            self.canvas.itemconfigure(self.porp, state="normal")
            self.canvas.itemconfigure(self.coin, state="hidden")
        elif self.action == "SERVING-PIPPU":
            self.reset()
            self.canvas.itemconfigure(self.status,text="SIRVIENDO PIPPU")
            self.canvas.itemconfigure(self.pippu, state="normal")
            self.canvas.itemconfigure(self.coin, state="hidden")
        elif self.action == "SERVING-CABRO":
            self.reset()
            self.canvas.itemconfigure(self.status,text="SIRVIENDO CABRO")
            self.canvas.itemconfigure(self.cabro, state="normal")
            self.canvas.itemconfigure(self.coin, state="hidden")