import tkinter as tk
import random
from Street import Street
from PIL import Image, ImageTk

# List of images
imagesHouse = ['city/house1.png', 'city/house2.png', 
          'city/house3.png', 'city/house4.png',
          'city/house5.png', 'city/house6.png',
          'city/house7.png', 'city/house8.png']
imagesTree = [ 'city/tree1.png', 'city/tree2.png', 'city/tree3.png',
        	'city/tree4.png', 'city/tree5.png']
imagesPool = ['city/pool1.png', 'city/pool2.png',
          'city/pool3.png', 'city/pool4.png']
streets = []
mode = "edition"
toUnite = []
selected = None
def place_street_image(event, canvas):
    # Get coordinates of the mouse click
    global mode, toUnite, selected
    x = event.x // 50 * 50
    y = event.y // 50 * 50
    xIndex = int(x/50)
    yIndex = int(y/50)
    # Place street image on canvas
    image = Image.open("city/cross2.png")
    adjacents = []
    if mode == "edition":
         toUnite = []
         canvas.delete("rect")
         streets[yIndex][xIndex] = Street(xIndex,yIndex,True,None,None)
         photo = ImageTk.PhotoImage(image)
         canvas.create_image(x, y, anchor=tk.NW, image=photo)
         canvas.street_images.append(photo)
    elif mode == "unite":
         if len(toUnite) < 2:
            if streets[yIndex][xIndex] == None:
                 return
            if len(toUnite) == 1:
                x0, y0 = toUnite[0].x, toUnite[0].y
                if (x0 == xIndex or y0 == yIndex):
                    if (x0 == xIndex):
                        for i in range(min(y0, yIndex)+1, min(y0, yIndex) + abs(y0 - yIndex)):
                            drawImageStreet(streets, canvas, x0, i, 90, "city/street1.png")
                    else:
                        for i in range(min(x0, xIndex)+1, min(x0, xIndex) + abs(x0 - xIndex)):
                            drawImageStreet(streets, canvas, i, y0, None, "city/street1.png")
                    toUnite = []
                    canvas.delete("rect")
                    return
            toUnite.append(streets[yIndex][xIndex])
            if len(toUnite) == 0:
                 canvas.rect1 = canvas.create_rectangle(xIndex*50, yIndex*50,xIndex*50 + 50, yIndex*50+ 50, outline = 'blue', tags="rect")
            else:
                 canvas.rect2 = canvas.create_rectangle(xIndex*50, yIndex*50,xIndex*50 + 50, yIndex*50+ 50, outline = 'blue', tags="rect")
         else:
             x1, y1 = xIndex, yIndex
             if (x1 == toUnite[0].x and y1 == toUnite[0].y) or (x1 == toUnite[1].x and y1 == toUnite[1].y):
                 toUnite = []
                 canvas.delete("rect")
                 return
             if (x1 == toUnite[0].x or y1 == toUnite[0].y) and (x1 == toUnite[1].x or y1 == toUnite[1].y):
                 if (x1 == toUnite[0].x and y1 == toUnite[1].y):
                     if toUnite[0].x < toUnite[1].x:
                         if toUnite[0].y < toUnite[1].y:drawImageStreet(streets, canvas, x1, y1, 270, "city/corner1.png")
                         else: drawImageStreet(streets, canvas, x1, y1, 180, "city/corner1.png")
                     else:
                         if toUnite[0].y < toUnite[1].y:drawImageStreet(streets, canvas, x1, y1, None, "city/corner1.png")
                         else: drawImageStreet(streets, canvas, x1, y1, 90, "city/corner1.png")
                 else:
                      if toUnite[0].y < toUnite[1].y:
                         if toUnite[0].x < toUnite[1].x:drawImageStreet(streets, canvas, x1, y1, 90, "city/corner1.png")
                         else: drawImageStreet(streets, canvas, x1, y1, 180, "city/corner1.png")
                      else:
                         if toUnite[0].x < toUnite[1].x:drawImageStreet(streets, canvas, x1, y1, None, "city/corner1.png")
                         else: drawImageStreet(streets, canvas, x1, y1, 270, "city/corner1.png")
             elif (x1 == toUnite[0].x or y1 == toUnite[0].y):
                 if x1 == toUnite[0].x: drawImageStreet(streets, canvas, x1,y1,90, "city/street1.png")
                 else: drawImageStreet(streets, canvas, x1, y1, None, "city/street1.png")
             elif (x1 == toUnite[1].x or y1 == toUnite[1].y):
                 if x1 == toUnite[1].x: drawImageStreet(streets, canvas, x1,y1,90, "city/street1.png")
                 else: drawImageStreet(streets, canvas, x1, y1, None, "city/street1.png")

def drawImageStreet(streets, canvas, x, y, rotation, image):
    image = Image.open(image)
    if rotation != None:
        image = image.rotate(rotation)
    streets[y][x] = Street(x,y,True,None,None)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(x * 50, y * 50, anchor=tk.NW, image=photo)
    canvas.street_images.append(photo)
def changeMode(newMode, button, buttons):
    global mode
    mode = newMode
    button.configure(bg="red", fg="yellow")
    for btn in buttons:
        if btn != button:
            btn.configure(bg="white", fg="black")
def create_canvas():
    root = tk.Tk()
    root.title("Random Image Canvas")
    # Create frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP)
    
    # Create buttons
    button1 = tk.Button(button_frame, text="Colocar Cruce")
    button2 = tk.Button(button_frame, text="Unir Cruces")
    button3 = tk.Button(button_frame, text="Configuración")
    buttons = [button1, button2, button3]
    button1.bind("<Button-1>", lambda event: changeMode("edition",button1,buttons))
    button1.pack(side=tk.LEFT)
    button2.bind("<Button-1>", lambda event: changeMode("unite",button2, buttons))
    button2.pack(side=tk.LEFT)
    button3.bind("<Button-1>", lambda event: changeMode("configurate",button3, buttons))
    button3.pack(side=tk.LEFT)
    # Create canvas with green background
    canvas = tk.Canvas(root, width=1000, height=600, bg="green")
    canvas.pack(side='bottom')
    # List to store references to images
    image_refs = []
    
    # Place images in grid
    for y in range(0, 600, 50):
        tempStreet = []
        for  x in range(0, 1000, 50):
            # Select random image
            randomArray = random.randint(1,100)
            array = imagesTree if randomArray >= 1 and randomArray < 50 else imagesHouse if randomArray >= 50 and randomArray < 95 else imagesPool
            image_path = random.choice(array)
            image = tk.PhotoImage(file=image_path)
            
            # Place image on canvas
            canvas.create_image(x, y, anchor=tk.NW, image=image)
            # Append reference to the list
            image_refs.append(image)
            tempStreet.append(None)
        streets.append(tempStreet)
    # Keep references to the images to prevent garbage collection
    canvas.image_refs = image_refs
    canvas.street_images = []
    canvas.bind("<Button-1>", lambda event: place_street_image(event, canvas))
    root.mainloop()

if __name__ == "__main__":
    create_canvas()
