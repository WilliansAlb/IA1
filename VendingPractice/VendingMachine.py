import threading
import time

class VendingMachine(threading.Thread):
    def __init__(self, initial, canvas, coin, pippu, porp, cabro, status):
        threading.Thread.__init__(self)
        self.perception = ""
        self.state = initial
        self.stop_event = threading.Event()
        self.canvas = canvas 
        self.coin = coin
        self.pippu = pippu
        self.porp = porp
        self.cabro = cabro
        self.status = status
        self.model_states = {
            "NO-COIN":  { "COIN": "COIN", "PORP": "RESET", "PIPPU": "RESET", "CABRO": "RESET" },
            "COIN":  { "COIN": "COIN", "PORP": "SERVING-PORP", "PIPPU": "SERVING-PIPPU", "CABRO": "SERVING-CABRO" },
            "SERVING-PORP":  { "COIN": "COIN", "PORP": "RESET", "PIPPU": "RESET", "CABRO": "RESET" },
            "SERVING-PIPPU":  { "COIN": "COIN", "PORP": "RESET", "PIPPU": "RESET", "CABRO": "RESET" },
            "SERVING-CABRO":  { "COIN": "COIN", "PORP": "RESET", "PIPPU": "RESET", "CABRO": "RESET" }
        }
        self.model_actions = {
            "NO-COIN":  "SHOW-COIN" ,
            "COIN":  "SHOW-CODE",
            "SERVING-PORP":  "SERVING-PORP",
            "SERVING-PIPPU":  "SERVING-PIPPU",
            "SERVING-CABRO":  "SERVING-CABRO"
        }
    def stop(self):
             self.stop_event.set()
    def run(self):
        while not self.stop_event.is_set():
            self.updateStatus()
            self.doAction()
            time.sleep(1)
    def updateStatus(self):
            if self.perception != "":
                self.state = self.model_states[self.state][self.perception]
            if self.state == "RESET":
                self.state = "NO-COIN"
    def doAction(self):
        newAction = self.model_actions[self.state];
        if newAction == "SHOW-COIN":
            self.canvas.itemconfigure(self.status,text="INSERTE MONEDA")
            self.reset()
        elif newAction == "SHOW-CODE":
            self.canvas.itemconfigure(self.status,text="ELIGE UNA BEBIDA")
            self.canvas.itemconfigure(self.coin, state="normal")
        elif newAction == "SERVING-PORP":
            self.reset()
            self.canvas.itemconfigure(self.status,text="SIRVIENDO PORP")
            self.canvas.itemconfigure(self.porp, state="normal")
            self.canvas.itemconfigure(self.coin, state="hidden")
        elif newAction == "SERVING-PIPPU":
            self.reset()
            self.canvas.itemconfigure(self.status,text="SIRVIENDO PIPPU")
            self.canvas.itemconfigure(self.pippu, state="normal")
            self.canvas.itemconfigure(self.coin, state="hidden")
        elif newAction == "SERVING-CABRO":
            self.reset()
            self.canvas.itemconfigure(self.status,text="SIRVIENDO CABRO")
            self.canvas.itemconfigure(self.cabro, state="normal")
            self.canvas.itemconfigure(self.coin, state="hidden")
    def reset(self):
        self.canvas.itemconfigure(self.porp, state="hidden")
        self.canvas.itemconfigure(self.pippu, state="hidden")
        self.canvas.itemconfigure(self.cabro, state="hidden")
        self.canvas.itemconfigure(self.coin, state="hidden")