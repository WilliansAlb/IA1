import tkinter as tk
from VendingMachine import VendingMachine

def insert_coin():
    global canvas, coin, status, vending
    vending.perception = "COIN"

def select(drink):
    global status, canvas, vending
    vending.perception = drink

def main():
    global vending_machine, coin, pippu, canvas, porp, cabro, status, vending
    root = tk.Tk()
    root.title("Vending Machine")
    factor = 1.5
    canvas_width = 665 // factor
    canvas_height = 916 // factor
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    vending_machine_img = tk.PhotoImage(file="./imgs/VendingMachine.png")
    coin_img = tk.PhotoImage(file="./imgs/Coin.png")
    pippu_img = tk.PhotoImage(file="./imgs/Cabro.png")
    porp_image = tk.PhotoImage(file="./imgs/Porp.png")
    cabro_image = tk.PhotoImage(file="./imgs/Pippu.png")
    
    vending_machine_img = vending_machine_img.zoom(2)
    coin_img = coin_img.zoom(2)
    pippu_img = pippu_img.zoom(2)
    porp_img = porp_image.zoom(2)
    cabro_img = cabro_image.zoom(2)
    
    vending_machine_img = vending_machine_img.subsample(3)
    coin_img = coin_img.subsample(3)
    pippu_img = pippu_img.subsample(3)
    porp_img = porp_img.subsample(3)
    cabro_img = cabro_img.subsample(3)

    canvas.create_image(0, 0, anchor=tk.NW, image=vending_machine_img)
    coin = canvas.create_image(0, 0, anchor=tk.NW, image=coin_img, state="hidden")
    pippu = canvas.create_image(0, 0, anchor=tk.NW, image=pippu_img, state="hidden")
    porp = canvas.create_image(0, 0, anchor=tk.NW, image=porp_img, state="hidden")
    cabro = canvas.create_image(0, 0, anchor=tk.NW, image=cabro_img, state="hidden")

    coin_area = canvas.create_rectangle(107/factor, 765/factor, 177/factor, 840/factor, outline="")
    pippu_area = canvas.create_rectangle(252/factor, 516/factor, 419/factor, 591/factor, outline="")
    porp_area = canvas.create_rectangle(54/factor, 516/factor, 219/factor, 591/factor, outline="")
    cabro_area = canvas.create_rectangle(447/factor, 516/factor, 615/factor, 591/factor, outline="")
    status = canvas.create_text(90/factor, 648/factor, anchor=tk.W, text="INSERTE MONEDA", fill="white", font=("Arial", 8), width=95)
    canvas.tag_bind(coin_area, "<Button-1>", lambda event: insert_coin())
    canvas.tag_bind(pippu_area, "<Button-1>", lambda event: select('PIPPU'))
    canvas.tag_bind(porp_area, "<Button-1>", lambda event: select('PORP'))
    canvas.tag_bind(cabro_area, "<Button-1>", lambda event: select('CABRO'))
    vending = VendingMachine("NO-COIN", canvas, coin, pippu, porp, cabro, status)
    vending.start()
    root.mainloop()
    vending.stop()
    vending.join()

if __name__ == "__main__":
    main()