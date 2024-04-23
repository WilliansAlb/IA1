import tkinter as tk
import random
from Street import Street
from PIL import Image, ImageTk
from Node import Node, ConfigurationNode
from tkinter import font
import pickle
class Visual:
	def __init__(self, configuration, generational):
		self.canvas = None
		self.root = None
		self.configuration = configuration
		self.button_frame = None
		self.mode = "put"
		self.streets = []
		self.toJoin = []
		self.generational = generational
		self.initializate()
	def initializate(self):
		self.root = tk.Tk()
		self.font = font.Font(family="FontAwesome", size=10)
		self.root.title("Traffic Project")
      	# Create frame for buttons
		self.button_frame = tk.Frame(self.root)
		self.button_frame.pack(side=tk.TOP)
		self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="green")
		# Create buttons
		self.putCrossButton = tk.Button(self.button_frame, text="\uf637", font=(self.font,10,"bold"))
		self.joinCrossesButton = tk.Button(self.button_frame, text="\uf018", font=self.font)
		self.settingButton = tk.Button(self.button_frame, text="\uf1de", font=self.font)
		self.runButton = tk.Button(self.button_frame, text="\uf01e", font=self.font)
		self.saveButton = tk.Button(self.button_frame, text="\uf0c7", font=self.font)
		self.saveButton.bind("<Button-1>", lambda event: self.showModalSave())
		self.collectionButtons = [self.putCrossButton, self.joinCrossesButton, self.settingButton]
		self.putCrossButton.bind("<Button-1>", lambda event: self.changeMode("put"))
		self.putCrossButton.pack(side=tk.LEFT)
		self.joinCrossesButton.bind("<Button-1>", lambda event: self.changeMode("join"))
		self.joinCrossesButton.pack(side=tk.LEFT)
		self.settingButton.bind("<Button-1>", lambda event: self.changeMode("setting"))
		self.settingButton.pack(side=tk.LEFT)
		self.runButton.bind("<Button-1>", lambda event: self.run_generational())
		self.runButton.pack(side=tk.LEFT)
		self.saveButton.pack(side=tk.LEFT)
		self.putCrossButton.configure(bg="red", fg="yellow")
		self.canvas.pack(side='bottom')
		image_refs = []
		for y in range(0, 600, 50):
			tempStreet = []
			for  x in range(0, 1000, 50):
				randomArray = random.randint(1,100)
				array = self.configuration.imgTree if randomArray >= 1 and randomArray < 50 else self.configuration.imgHouse if randomArray >= 50 and randomArray < 95 else self.configuration.imgPool
				image_path = random.choice(array)
				image = tk.PhotoImage(file=image_path)
				self.canvas.create_image(x, y, anchor=tk.NW, image=image)
				image_refs.append(image)
				tempStreet.append(None)
			self.streets.append(tempStreet)
		# Keep references to the images to prevent garbage collection
		self.canvas.image_refs = image_refs
		self.canvas.street_images = []
		self.canvas.bind("<Button-1>", lambda event: self.click_map(event))
		self.root.mainloop()
	def showModalSave(self):
		input_dialog = tk.Toplevel(self.root)
		input_dialog.title("Nombre")
		label = tk.Label(input_dialog, font=self.font, text=f"¿Cómo se llamará el archivo?")
		label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
		entry = tk.Entry(input_dialog)
		entry.grid(row=0, column=1, padx=10, pady=5)
		def submit_inputs():
			inputs = entry.get()
			with open(f"{inputs}.pkl",'wb') as file:
				pickle.dump(self.generational.nodes, file)
			input_dialog.destroy()
		submit_button = tk.Button(input_dialog, text="Submit", command=submit_inputs)
		submit_button.grid(row=1, columnspan=2, padx=10, pady=10)
	def run_generational(self):
		for node in self.generational.nodes:
			for out in node.outs:
				for line in self.streets:
					for street in line:
						if street !=None and not street.isCross:
							if node == street.nodes[0] and out.node == street.nodes[1]:
								out.square = street
		self.generational.runModel(self.canvas, self.font, self.root)
	def click_map(self, event):
		x = event.x // 50 * 50
		y = event.y // 50 * 50
		xIndex = int(x/50)
		yIndex = int(y/50)
		if self.mode == "put":
			self.putNode(yIndex,xIndex, x, y)
		elif self.mode == "setting":
			self.settingNode(xIndex,yIndex)
		elif self.mode == "join":
			self.joinCrosses(yIndex,xIndex)
	def settingNode(self, x , y):
		street = self.streets[y][x]
		if street.isCross:
			if len(street.node.ins) == 0 or len(street.node.outs) == 0:
				input_dialog = tk.Toplevel(self.root)
				self.showModalCross(input_dialog, self.streets[y][x])
		else:
			for out in self.streets[y][x].nodes[0].outs:
				if out.node.index == self.streets[y][x].nodes[1].index:
					input_dialog = tk.Toplevel(self.root)
					self.showModalStreet(input_dialog, self.streets[y][x], out, f"{self.streets[y][x].nodes[0].index}&{self.streets[y][x].nodes[1].index}")
	def showModalCross(self, input_dialog, street):
		input_dialog.title("Datos Cruce")
		node = street.node
		input_entries = []
		label = tk.Label(input_dialog, font=self.font, text=f"{'\uf5e4 \uf090 ¿Cuántos autos entran?' if len(node.ins) == 0 else '\uf08b \uf5e4¿Cuántos autos se esperan que salgan?' }")
		label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
		entry = tk.Entry(input_dialog)
		entry.grid(row=0, column=1, padx=10, pady=5)
		if street.text != None: self.canvas.delete(street.text)
		def submit_inputs():
			inputs = entry.get()
			print("User entered:", inputs)
			node.cars = int(inputs)
			street.text = self.canvas.create_text(street.x * 50 + 25, street.y * 50+25, text=f"{'\uf5e4 \uf090' if len(node.ins) == 0 else '\uf08b \uf5e4' } \n {inputs}", fill="black", font=self.font)
			input_dialog.destroy()
		submit_button = tk.Button(input_dialog, text="Submit", command=submit_inputs)
		submit_button.grid(row=1, columnspan=2, padx=10, pady=10)
	def showModalStreet(self, input_dialog, street, node, tag):
		input_dialog.title("Datos Calle")
		input_entries = []
		max_cars = tk.Label(input_dialog, font=self.font, text=f"\uf5e4 Máximo")
		max_cars.grid(row=0, column=0, padx=10, pady=5, sticky="e")
		previous_cars = tk.StringVar()
		previous_cars.set(str(node.max_cars))
		entry_cars = tk.Entry(input_dialog, textvariable=previous_cars)
		entry_cars.grid(row=0, column=1, padx=10, pady=5)
		min_percentage = tk.Label(input_dialog, font=self.font, text=f"% Minimo")
		min_percentage.grid(row=1, column=0, padx=10, pady=5, sticky="e")
		previous_percentage = tk.StringVar()
		previous_percentage.set(str(node.max_percentage))
		entry_percentage = tk.Entry(input_dialog, textvariable=previous_percentage)
		entry_percentage.grid(row=1, column=1, padx=10, pady=5)
		self.canvas.delete(tag)
		def submit_inputs():
			street.text = self.canvas.create_text(street.x * 50 + 25, street.y * 50+25, text=f"\uf5e4 {entry_cars.get()} \n % {entry_percentage.get()}", fill="black", font=self.font, tags=tag)
			node.max_percentage = entry_percentage.get()
			node.max_cars = entry_cars.get()
			input_dialog.destroy()
		submit_button = tk.Button(input_dialog, text="Submit", command=submit_inputs)
		submit_button.grid(row=2, columnspan=2, padx=10, pady=10)
	def putNode(self, yIndex, xIndex, x, y):
		image = Image.open("city/cross2.png")
		self.toJoin = []
		self.canvas.delete("rect")
		if self.streets[yIndex][xIndex] == None:
			self.streets[yIndex][xIndex] = Street(xIndex,yIndex,True,None,None)
			photo = ImageTk.PhotoImage(image)
			self.canvas.create_image(x, y, anchor=tk.NW, image=photo)
			self.streets[yIndex][xIndex].image = photo
			if self.streets[yIndex][xIndex].node == None:
				newNode = Node(None,[],[], len(self.generational.nodes))
				self.generational.nodes.append(newNode)
				self.streets[yIndex][xIndex].node = newNode
	def drawImageStreet(self, x, y, rotation, image):
		image = Image.open(image)
		if rotation != None:
			image = image.rotate(rotation)
		self.streets[y][x] = Street(x,y,False,None,None)
		self.streets[y][x].nodes = [self.toJoin[0].node, self.toJoin[1].node]
		photo = ImageTk.PhotoImage(image)
		self.canvas.create_image(x * 50, y * 50, anchor=tk.NW, image=photo)
		self.canvas.street_images.append(photo)
	def joinCrosses(self, yIndex, xIndex):
		if len(self.toJoin) < 2:
			if self.streets[yIndex][xIndex] == None:
				return
			if len(self.toJoin) == 1:
				x0, y0 = self.toJoin[0].x, self.toJoin[0].y
				if (x0 == xIndex or y0 == yIndex):
					self.toJoin.append(self.streets[yIndex][xIndex])
					self.toJoin[0].node.outs.append(ConfigurationNode(self.toJoin[1].node,0,0,0))
					self.toJoin[1].node.ins.append(self.toJoin[0].node)
					if (x0 == xIndex):
						for i in range(min(y0, yIndex)+1, min(y0, yIndex) + abs(y0 - yIndex)):
							self.drawImageStreet(x0, i, 90, "city/street1.png")
							if y0 < yIndex: self.streets[i][x0].text = self.canvas.create_text(x0 * 50 + 25, i * 50+25, text=f"\uf309", fill="yellow", font=self.font)
							else: self.streets[i][x0].text = self.canvas.create_text(x0 * 50 + 25, i * 50+25, text=f"\uf30c", fill="yellow", font=self.font)
					else:
						for i in range(min(x0, xIndex)+1, min(x0, xIndex) + abs(x0 - xIndex)):
							self.drawImageStreet(i, y0, None, "city/street1.png")
							if x0 < xIndex: self.streets[y0][i].text = self.canvas.create_text(i * 50 + 25, y0 * 50+25, text=f"\uf30b", fill="yellow", font=self.font)
							else: self.streets[y0][i].text = self.canvas.create_text(i * 50 + 25, y0 * 50+25, text=f"\uf30a", fill="yellow", font=self.font)
					self.toJoin = []
					self.canvas.delete("rect")
					return
			self.toJoin.append(self.streets[yIndex][xIndex])
			if len(self.toJoin) == 1:
				self.canvas.rect1 = self.canvas.create_rectangle(xIndex*50, yIndex*50,xIndex*50 + 50, yIndex*50+ 50, outline = 'blue', tags="rect")
			elif len(self.toJoin) == 2:
				print(self.toJoin[0].node.outs)
				self.toJoin[0].node.outs.append(ConfigurationNode(self.toJoin[1].node,0,0,0))
				self.toJoin[1].node.ins.append(self.toJoin[0].node)
				xInitial, yInitial = self.toJoin[0].x, self.toJoin[0].y
				xDestiny, yDestiny = self.toJoin[1].x, self.toJoin[1].y
				xDifference = xInitial - xDestiny
				yDifference = yInitial - yDestiny
				left = xDifference >= 0
				up = yDifference >= 0
				self.toJoin[0].direction = [left,up]
				self.canvas.rect2 = self.canvas.create_rectangle(xIndex*50, yIndex*50,xIndex*50 + 50, yIndex*50+ 50, outline = 'blue', tags="rect")
		else:
			x1, y1 = xIndex, yIndex
			isCorner = False
			isHorizontal = False
			if (x1 == self.toJoin[0].x and y1 == self.toJoin[0].y) or (x1 == self.toJoin[1].x and y1 == self.toJoin[1].y):
				self.toJoin = []
				self.canvas.delete("rect")
				return
			if (x1 == self.toJoin[0].x or y1 == self.toJoin[0].y) and (x1 == self.toJoin[1].x or y1 == self.toJoin[1].y):
				isCorner = True
				if (x1 == self.toJoin[0].x and y1 == self.toJoin[1].y):
					if self.toJoin[0].x < self.toJoin[1].x: self.drawImageStreet(x1, y1, 270 if self.toJoin[0].y < self.toJoin[1].y else 180, "city/corner1.png")
					else: self.drawImageStreet(x1, y1, None if self.toJoin[0].y < self.toJoin[1].y else 90, "city/corner1.png")
				else:
					if self.toJoin[0].y < self.toJoin[1].y: self.drawImageStreet(x1, y1, 90 if self.toJoin[0].x < self.toJoin[1].x else 180, "city/corner1.png")
					else: self.drawImageStreet(x1, y1, None if self.toJoin[0].x < self.toJoin[1].x else 270, "city/corner1.png")
			elif x1 == self.toJoin[0].x or x1 == self.toJoin[1].x: self.drawImageStreet(x1,y1,90, "city/street1.png")
			elif y1 == self.toJoin[0].y or y1 == self.toJoin[1].y: 
				self.drawImageStreet(x1, y1, None, "city/street1.png")
				isHorizontal = True
			if self.streets[y1][x1] != None:
				self.streets[y1][x1].direction = self.toJoin[0].direction
				if not isCorner:
					if isHorizontal:
						self.streets[y1][x1].text = self.canvas.create_text(x1 * 50 + 25, y1 * 50+25, text=f"{'\uf30a' if self.toJoin[0].direction[0] else '\uf30b'}", fill="yellow", font=self.font, tags="direction")
					else: 
						self.streets[y1][x1].text = self.canvas.create_text(x1 * 50 + 25, y1 * 50+25, text=f"{'\uf30c' if self.toJoin[0].direction[1] else '\uf309'}", fill="yellow", font=self.font, tags="direction")
	def changeMode(self, newMode):
		self.mode = newMode
		for btn in self.collectionButtons:
			btn.configure(bg="white", fg="black")
		if self.mode == "put": self.putCrossButton.configure(bg="red", fg="yellow")
		if self.mode == "join": self.joinCrossesButton.configure(bg="red", fg="yellow")
		if self.mode == "setting": self.settingButton.configure(bg="red", fg="yellow")
		self.canvas.rects = []
		self.toJoin = []
		self.canvas.delete("rect")
		if self.mode == "setting":
			for street in self.streets:
				for j in street:
					if j!=None:
						self.canvas.rects.append(self.canvas.create_rectangle(j.x*50, j.y*50,j.x*50 + 50, j.y*50+ 50, outline = 'blue', tags="rect"))
		