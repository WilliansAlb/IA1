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
        self.run_data = None
        self.streets = []
        self.toJoin = []
        self.generational = generational
        self.root = tk.Tk()
        self.font = font.Font(family="FontAwesome", size=10)
        self.putCrossButton = None
        self.joinCrossesButton = None
        self.settingButton = None
        self.runButton = None
        self.saveButton = None
        self.stopButton = None
        self.collectionButtons = []
        self.initialize()

    def initialize(self):
        self.root.title("Traffic Project")
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP)
        self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="#77dd77")
        # Create buttons
        self.putCrossButton = tk.Button(self.button_frame, text="\uf637", font=(self.font, 10, "bold"))
        self.joinCrossesButton = tk.Button(self.button_frame, text="\uf018", font=self.font)
        self.settingButton = tk.Button(self.button_frame, text="\uf1de", font=self.font)
        self.runButton = tk.Button(self.button_frame, text="\uf01e", font=self.font)
        self.stopButton = tk.Button(self.button_frame, text="\uf256", font=self.font)
        self.saveButton = tk.Button(self.button_frame, text="\uf0c7", font=self.font)
        self.saveButton.bind("<Button-1>", lambda event: self.show_modal_save())
        self.collectionButtons = [self.putCrossButton, self.joinCrossesButton, self.settingButton]
        self.putCrossButton.bind("<Button-1>", lambda event: self.change_mode("put"))
        self.putCrossButton.pack(side=tk.LEFT)
        self.joinCrossesButton.bind("<Button-1>", lambda event: self.change_mode("join"))
        self.joinCrossesButton.pack(side=tk.LEFT)
        self.settingButton.bind("<Button-1>", lambda event: self.change_mode("setting"))
        self.settingButton.pack(side=tk.LEFT)
        self.runButton.bind("<Button-1>", lambda event: self.run_generational())
        self.runButton.pack(side=tk.LEFT)
        self.stopButton.bind("<Button-1>", lambda event: self.stop_generational())
        self.stopButton.pack(side=tk.LEFT)
        self.saveButton.pack(side=tk.LEFT)
        self.putCrossButton.configure(bg="red", fg="#DAF7A6")
        self.run_data = tk.Label(self.root, font=(self.font, 14, "bold"), text=f"Traffic Project", anchor="center")
        self.run_data.pack(side='bottom')
        self.canvas.pack(side='bottom')
        image_refs = []
        for y in range(0, 600, 50):
            temp_street = []
            for x in range(0, 1000, 50):
                random_array = random.randint(1, 100)
                array = self.configuration.imgTree if 1 <= random_array < 70 else (
                    self.configuration.imgHouse) if 70 <= random_array < 99 else self.configuration.imgPool
                image_path = random.choice(array)
                image = tk.PhotoImage(file=image_path)
                self.canvas.create_image(x, y, anchor=tk.NW, image=image)
                image_refs.append(image)
                temp_street.append(None)
            self.streets.append(temp_street)
        # Keep references to the images to prevent garbage collection
        self.canvas.image_refs = image_refs
        self.canvas.street_images = []
        self.canvas.bind("<Button-1>", lambda event: self.click_map(event))
        self.root.mainloop()

    def stop_generational(self):
        self.generational.stop = True

    def show_modal_save(self):
        input_dialog = tk.Toplevel(self.root)
        input_dialog.title("Name")
        label = tk.Label(input_dialog, font=self.font, text=f"What will the file be called?")
        label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(input_dialog)
        entry.grid(row=0, column=1, padx=10, pady=5)

        def submit_inputs():
            inputs = entry.get()
            with open(f"{inputs}.pkl", 'wb') as file:
                pickle.dump(self.generational.nodes, file)
            input_dialog.destroy()

        submit_button = tk.Button(input_dialog, text="SAVE", command=submit_inputs)
        submit_button.grid(row=1, columnspan=2, padx=10, pady=10)

    def run_generational(self):
        self.canvas.delete("rect")
        self.show_modal_run()

    def click_map(self, event):
        x = event.x // 50 * 50
        y = event.y // 50 * 50
        x_index = int(x / 50)
        y_index = int(y / 50)
        if self.mode == "put":
            self.put_node(y_index, x_index, x, y)
        elif self.mode == "setting":
            self.setting_node(x_index, y_index)
        elif self.mode == "join":
            self.join_crosses(y_index, x_index)

    def setting_node(self, x, y):
        street = self.streets[y][x]
        if street.isCross:
            if len(street.node.ins) == 0 or len(street.node.outs) == 0:
                input_dialog = tk.Toplevel(self.root)
                self.show_modal_cross(input_dialog, self.streets[y][x])
        else:
            for out in self.streets[y][x].nodes[0].outs:
                if out.node.index == self.streets[y][x].nodes[1].index:
                    input_dialog = tk.Toplevel(self.root)
                    self.show_modal_street(input_dialog, self.streets[y][x], out,
                                           f"{self.streets[y][x].nodes[0].index}&{self.streets[y][x].nodes[1].index}")

    def show_modal_cross(self, input_dialog, street):
        input_dialog.title("Cross Data")
        node = street.node
        label = tk.Label(input_dialog, font=self.font,
                         text=f"{'\uf5e4 \uf090 How many cars enter the street?' if len(node.ins) == 0 else '\uf08b \uf5e4 How many cars leave the street?'}")
        label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(input_dialog)
        entry.grid(row=0, column=1, padx=10, pady=5)
        if street.text is not None:
            self.canvas.delete(street.text)

        def submit_inputs():
            inputs = entry.get()
            print("User entered:", inputs)
            node.cars = int(inputs)
            street.text = self.canvas.create_text(street.x * 50 + 25, street.y * 50 + 25,
                                                  text=f"{'\uf5e4 \uf090' if len(node.ins) == 0 else '\uf08b \uf5e4'} \n {inputs}",
                                                  fill="white", font=self.font)
            input_dialog.destroy()

        submit_button = tk.Button(input_dialog, text="Submit", command=submit_inputs)
        submit_button.grid(row=1, columnspan=2, padx=10, pady=10)

    def show_modal_street(self, input_dialog, street, node, tag):
        input_dialog.title("Street Data")
        max_cars = tk.Label(input_dialog, font=self.font, text=f"\uf5e4 Max")
        max_cars.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        previous_cars = tk.StringVar()
        previous_cars.set(str(node.max_cars))
        entry_cars = tk.Entry(input_dialog, textvariable=previous_cars)
        entry_cars.grid(row=0, column=1, padx=10, pady=5)
        min_percentage = tk.Label(input_dialog, font=self.font, text=f"% Min")
        min_percentage.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        previous_percentage = tk.StringVar()
        previous_percentage.set(str(node.max_percentage))
        entry_percentage = tk.Entry(input_dialog, textvariable=previous_percentage)
        entry_percentage.grid(row=1, column=1, padx=10, pady=5)
        self.canvas.delete(tag)

        def submit_inputs():
            label = f"\uf5e4 {entry_cars.get()} \n % {entry_percentage.get()}"
            x = street.x * 50 + 25
            y = street.y * 50 + 25
            street.text = self.canvas.create_text(x, y, text=label, fill="white", font=self.font, tags=tag)
            node.max_percentage = entry_percentage.get()
            node.max_cars = entry_cars.get()
            input_dialog.destroy()

        submit_button = tk.Button(input_dialog, text="Submit", command=submit_inputs)
        submit_button.grid(row=2, columnspan=2, padx=10, pady=10)
    def show_modal_run(self):
        input_dialog = tk.Toplevel(self.root)
        input_dialog.title("Run Data")
        population_size = tk.Label(input_dialog, font=self.font, text=f"\uf471 Size")
        population_size.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        previous_population = tk.StringVar()
        previous_population.set(str(self.generational.population))
        entry_population = tk.Entry(input_dialog, textvariable=previous_population)
        entry_population.grid(row=0, column=1, padx=10, pady=5)

        label_mutation = tk.Label(input_dialog, font=(self.font, 14, "bold"), text=f"% Mutation Rate", anchor="center")
        label_mutation.grid(row=1, columnspan=2, padx=10, pady=10)

        for_each_generations = tk.Label(input_dialog, font=self.font, text=f"\uf0c0 For each (generations)")
        for_each_generations.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        previous_for_each = tk.StringVar()
        previous_for_each.set(str(self.generational.for_each_m_generation))
        entry_for_each = tk.Entry(input_dialog, textvariable=previous_for_each)
        entry_for_each.grid(row=2, column=1, padx=10, pady=5)

        do_mutations = tk.Label(input_dialog, font=self.font, text=f"\uf67b Do (mutations)")
        do_mutations.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        previous_mutations = tk.StringVar()
        previous_mutations.set(str(self.generational.do_n_mutation))
        entry_mutations = tk.Entry(input_dialog, textvariable=previous_mutations)
        entry_mutations.grid(row=3, column=1, padx=10, pady=5)

        label_mutation = tk.Label(input_dialog, font=(self.font, 14, "bold"), text=f"\uf140 Completion Criteria")
        label_mutation.grid(row=4, columnspan=2, padx=10, pady=10)

        button_mutation = None
        button_mutation = tk.Button(input_dialog, font=self.font, text="\uf0c0" if self.generational.generation_based_end else '%')
        button_mutation.bind("<Button-1>", lambda event: self.switch_mutation(button_mutation))
        button_mutation.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        previous_completion_criteria = tk.StringVar()
        previous_completion_criteria.set(str(self.generational.completion_criteria))
        entry_criteria = tk.Entry(input_dialog, textvariable=previous_completion_criteria)
        entry_criteria.grid(row=5, column=1, padx=10, pady=5)

        def submit_inputs():
            self.generational.population = int(entry_population.get())
            self.generational.completion_criteria = int(entry_criteria.get())
            input_dialog.destroy()
            for node in self.generational.nodes:
                for out in node.outs:
                    for line in self.streets:
                        for street in line:
                            if street is not None and not street.isCross:
                                if node == street.nodes[0] and out.node == street.nodes[1]:
                                    out.square = street
            self.generational.run_model(self.canvas, self.font, self.root, self.run_data)

        submit_button = tk.Button(input_dialog, text="RUN", command=submit_inputs)
        submit_button.grid(row=6, columnspan=2, padx=10, pady=10)

    def switch_mutation(self, button):
        self.generational.generation_based_end = not self.generational.generation_based_end
        button.config(text="\uf0c0 Generations" if self.generational.generation_based_end else '% Efficiency')
    def put_node(self, y_index, x_index, x, y):
        image = Image.open("city/cross2v2.png")
        self.toJoin = []
        self.canvas.delete("rect")
        if self.streets[y_index][x_index] is None:
            self.streets[y_index][x_index] = Street(x_index, y_index, True, None, None)
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(x, y, anchor=tk.NW, image=photo)
            self.streets[y_index][x_index].image = photo
            if self.streets[y_index][x_index].node is None:
                new_node = Node(None, [], [], len(self.generational.nodes))
                self.generational.nodes.append(new_node)
                self.streets[y_index][x_index].node = new_node

    def draw_image_street(self, x, y, rotation, image):
        image = Image.open(image)
        if rotation is not None:
            image = image.rotate(rotation)
        self.streets[y][x] = Street(x, y, False, None, None)
        self.streets[y][x].nodes = [self.toJoin[0].node, self.toJoin[1].node]
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(x * 50, y * 50, anchor=tk.NW, image=photo)
        self.canvas.street_images.append(photo)

    def join_crosses(self, y_index, x_index):
        if len(self.toJoin) < 2:
            if self.streets[y_index][x_index] is None:
                return
            if len(self.toJoin) == 1:
                x0, y0 = self.toJoin[0].x, self.toJoin[0].y
                if x0 == x_index or y0 == y_index:
                    self.toJoin.append(self.streets[y_index][x_index])
                    self.toJoin[0].node.outs.append(ConfigurationNode(self.toJoin[1].node, 0, 0, 0))
                    self.toJoin[1].node.ins.append(self.toJoin[0].node)
                    if x0 == x_index:
                        for i in range(min(y0, y_index) + 1, min(y0, y_index) + abs(y0 - y_index)):
                            self.draw_image_street(x0, i, 90, "city/street1v2.png")
                            if y0 < y_index:
                                self.streets[i][x0].text = self.canvas.create_text(x0 * 50 + 25, i * 50 + 25,
                                                                                   text=f"\uf309", fill="#DAF7A6",
                                                                                   font=(self.font, 8))
                            else:
                                self.streets[i][x0].text = self.canvas.create_text(x0 * 50 + 25, i * 50 + 25,
                                                                                   text=f"\uf30c", fill="#DAF7A6",
                                                                                   font=(self.font, 8))
                    else:
                        for i in range(min(x0, x_index) + 1, min(x0, x_index) + abs(x0 - x_index)):
                            self.draw_image_street(i, y0, None, "city/street1v2.png")
                            if x0 < x_index:
                                self.streets[y0][i].text = self.canvas.create_text(i * 50 + 25, y0 * 50 + 25,
                                                                                   text=f"\uf30b", fill="#DAF7A6",
                                                                                   font=(self.font, 8))
                            else:
                                self.streets[y0][i].text = self.canvas.create_text(i * 50 + 25, y0 * 50 + 25,
                                                                                   text=f"\uf30a", fill="#DAF7A6",
                                                                                   font=(self.font, 8))
                    self.toJoin = []
                    self.canvas.delete("rect")
                    return
            self.toJoin.append(self.streets[y_index][x_index])
            if len(self.toJoin) == 1:
                self.canvas.rect1 = self.canvas.create_rectangle(x_index * 50, y_index * 50, x_index * 50 + 50,
                                                                 y_index * 50 + 50, outline='blue', tags="rect")
            elif len(self.toJoin) == 2:
                print(self.toJoin[0].node.outs)
                self.toJoin[0].node.outs.append(ConfigurationNode(self.toJoin[1].node, 0, 0, 0))
                self.toJoin[1].node.ins.append(self.toJoin[0].node)
                x_initial, y_initial = self.toJoin[0].x, self.toJoin[0].y
                x_destiny, y_destiny = self.toJoin[1].x, self.toJoin[1].y
                x_difference = x_initial - x_destiny
                y_difference = y_initial - y_destiny
                left = x_difference >= 0
                up = y_difference >= 0
                self.toJoin[0].direction = [left, up]
                self.canvas.rect2 = self.canvas.create_rectangle(x_index * 50, y_index * 50, x_index * 50 + 50,
                                                                 y_index * 50 + 50, outline='blue', tags="rect")
        else:
            x1, y1 = x_index, y_index
            is_corner = False
            is_horizontal = False
            if (x1 == self.toJoin[0].x and y1 == self.toJoin[0].y) or (
                    x1 == self.toJoin[1].x and y1 == self.toJoin[1].y):
                self.toJoin = []
                self.canvas.delete("rect")
                return
            if (x1 == self.toJoin[0].x or y1 == self.toJoin[0].y) and (
                    x1 == self.toJoin[1].x or y1 == self.toJoin[1].y):
                is_corner = True
                if x1 == self.toJoin[0].x and y1 == self.toJoin[1].y:
                    if self.toJoin[0].x < self.toJoin[1].x:
                        self.draw_image_street(x1, y1, 270 if self.toJoin[0].y < self.toJoin[1].y else 180,
                                               "city/corner1v2.png")
                    else:
                        self.draw_image_street(x1, y1, None if self.toJoin[0].y < self.toJoin[1].y else 90,
                                               "city/corner1v2.png")
                else:
                    if self.toJoin[0].y < self.toJoin[1].y:
                        self.draw_image_street(x1, y1, 90 if self.toJoin[0].x < self.toJoin[1].x else 180,
                                               "city/corner1v2.png")
                    else:
                        self.draw_image_street(x1, y1, None if self.toJoin[0].x < self.toJoin[1].x else 270,
                                               "city/corner1v2.png")
            elif x1 == self.toJoin[0].x or x1 == self.toJoin[1].x:
                self.draw_image_street(x1, y1, 90, "city/street1v2.png")
            elif y1 == self.toJoin[0].y or y1 == self.toJoin[1].y:
                self.draw_image_street(x1, y1, None, "city/street1v2.png")
                is_horizontal = True
            if self.streets[y1][x1] is not None:
                self.streets[y1][x1].direction = self.toJoin[0].direction
                if not is_corner:
                    if is_horizontal:
                        self.streets[y1][x1].text = self.canvas.create_text(x1 * 50 + 25, y1 * 50 + 25,
                                                                            text=f"{'\uf30a' if self.toJoin[0].direction[0] else '\uf30b'}",
                                                                            fill="#DAF7A6", font=(self.font, 8),
                                                                            tags="direction")
                    else:
                        self.streets[y1][x1].text = self.canvas.create_text(x1 * 50 + 25, y1 * 50 + 25,
                                                                            text=f"{'\uf30c' if self.toJoin[0].direction[1] else '\uf309'}",
                                                                            fill="#DAF7A6", font=(self.font, 8),
                                                                            tags="direction")

    def change_mode(self, new_mode):
        self.mode = new_mode
        for btn in self.collectionButtons:
            btn.configure(bg="white", fg="black")
        if self.mode == "put":
            self.putCrossButton.configure(bg="red", fg="#DAF7A6")
        if self.mode == "join":
            self.joinCrossesButton.configure(bg="red", fg="#DAF7A6")
        if self.mode == "setting":
            self.settingButton.configure(bg="red", fg="#DAF7A6")
        self.canvas.rects = []
        self.toJoin = []
        self.canvas.delete("rect")
        if self.mode == "setting":
            for line in self.streets:
                for street in line:
                    if street is not None:
                        self.canvas.rects.append(
                            self.canvas.create_rectangle(street.x * 50,
                                                         street.y * 50,
                                                         street.x * 50 + 50,
                                                         street.y * 50 + 50,
                                                         outline='blue', tags="rect"))
