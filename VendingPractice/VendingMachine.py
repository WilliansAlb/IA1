import threading
import time

class VendingMachine(threading.Thread):
    def __init__(self, initial, canvas, coin, pippu, porp, cabro, status):
        threading.Thread.__init__(self)
        self.perception = initial
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
            print(self.perception)
            if self.perception == 'COIN':
                self.canvas.itemconfigure(self.coin, state="hidden")
            if self.perception == 'PORP':
                self.canvas.itemconfigure(self.porp, state="normal")
            if self.perception == 'PIPPU':
                self.canvas.itemconfigure(self.pippu, state="normal")
            if self.perception == 'CABRO':
                self.canvas.itemconfigure(self.cabro, state="normal")
            time.sleep(1.5)