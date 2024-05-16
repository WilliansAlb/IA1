import copy
import random


class Individual:
    def __init__(self, nodes, canvas, font, root):
        self.aptitude = 0
        self.gens = []
        self.nodes = nodes
        self.estimate = 0
        self.canvas = canvas
        self.font = font
        self.root = root
        self.randomize()

    def randomize(self):
        temporal = copy.deepcopy(self.nodes)
        for node in temporal:
            if len(node.outs) == 0:
                self.estimate += node.cars if node.cars is not None else 0
        for node in temporal:
            if len(node.outs) == 1:
                node.outs[0].generated = 100
                self.canvas.create_text(node.outs[0].square.x * 50 + 25, node.outs[0].square.y * 50 + 12, text=f"%{node.outs[0].generated}",
                                        fill="#FFC300", font=("FontAwesome", 12, "bold"), tags='generated')
                self.root.update()
            else:
                percentage = 100
                for out in node.outs:
                    if percentage > 1:
                        out.generated = random.randint(1, percentage)
                    else:
                        out.generated = 0
                    percentage -= out.generated
                    self.canvas.create_text(out.square.x * 50 + 25, out.square.y * 50 + 12, text=f"%{out.generated}",
                                            fill="#FFC300", font=("FontAwesome", 12, "bold"), tags='generated')
                    self.root.update()
        self.gens = temporal

    def evaluate_fitness(self):
        self.aptitude = 0
        for node in self.gens:
            node.in_cars = 0
            if len(node.ins) != 0:
                node.cars = 0
        for node in self.gens:
            if len(node.ins) == 0:
                self.recursive_evaluate(node)

    def recursive_evaluate(self, node):
        if len(node.outs) != 0:
            for out in node.outs:
                if node.cars * (out.generated / 100) > int(out.max_cars):
                    out.node.cars += 0
                else:
                    out.node.cars += int(node.cars * (out.generated / 100))
                out.node.in_cars += 1
                if out.node.in_cars == len(out.node.ins):
                    print(out.node.in_cars)
                    self.recursive_evaluate(out.node)
        else:
            self.aptitude += node.cars

    def draw_individual(self):
        for node in self.gens:
            for out in node.outs:
                self.canvas.create_text(out.square.x * 50 + 25, out.square.y * 50 + 12, text=f"%{out.generated}",
                                        fill="#FFC300", font=("FontAwesome", 12, "bold"), tags='generated')
                self.root.update()

    def recursive_generate(self, outs):
        percentage = 100
        if len(outs) != 0:
            if len(outs) == 1:
                outs[0].generated = 100
                self.recursive_generate(outs[0].node.outs)
            else:
                count = 0
                percentage = 100 - sum(int(out.max_percentage) for out in outs)
                for out in outs:
                    count = count + 1
                    percentage += int(out.max_percentage)
                    if count != len(outs):
                        generated = random.randint(int(out.max_percentage), percentage)
                        out.generated = generated
                        percentage -= generated
                    # print(f"Genera {out.generated} y se va al nodo {out.node.index}")
                    else:
                        out.generated = percentage
                    self.canvas.create_text(out.square.x * 50 + 25, out.square.y * 50 + 12, text=f"%{out.generated}",
                                            fill="#FFC300", font=("FontAwesome", 12, "bold"), tags='generated')
                    self.root.update()
                    self.recursive_generate(out.node.outs)
