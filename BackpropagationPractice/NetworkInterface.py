import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from Network import Network


class NetworkInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Neural Network Configuration")
        self.parameters = {
            "ENTRADAS": tk.IntVar(value=2),
            "CAPAS OCULTAS": tk.IntVar(value=2),
            "# NEURONAS OCULTAS": tk.IntVar(value=2),
            "SALIDAS": tk.IntVar(value=1),
            "ITERACIONES": tk.IntVar(value=100000),
            "FACTOR DE APRENDIZAJE": tk.DoubleVar(value=0.02),
            "SIGMOID": tk.BooleanVar(value=False),
            "STEP": tk.BooleanVar(value=False)
        }
        self.network = None
        self.learning = None
        self.left_frame = ttk.Frame(self.root)
        self.create_widgets()

    def create_widgets(self):
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N)

        right_frame = ttk.Frame(self.root)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N)

        # Create input fields for each parameter
        row = 0
        for param, var in self.parameters.items():
            label = ttk.Label(right_frame, text=param)
            label.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)

            if isinstance(var, tk.BooleanVar):
                button = ttk.Checkbutton(right_frame, variable=var, text="")
                button.grid(row=row, column=1, padx=5, pady=5)
            elif isinstance(var, tk.IntVar):
                entry = ttk.Entry(right_frame, textvariable=var)
                entry.grid(row=row, column=1, padx=5, pady=5)
            elif isinstance(var, tk.DoubleVar):
                entry = ttk.Entry(right_frame, textvariable=var)
                entry.grid(row=row, column=1, padx=5, pady=5)

            row += 1
        self.learning = tk.Label(right_frame, text="algo")
        self.learning.grid(row=row, column=0, padx=5, pady=5)
        # Button to submit the form
        submit_button = ttk.Button(right_frame, text="Submit", command=self.submit)
        submit_button.grid(row=row + 1, column=0, columnspan=2, pady=10)

    def create_graph(self, frame):
        weights = self.network.weights if self.network is not None else []
        architecture = [self.parameters["ENTRADAS"].get(),
                        self.parameters["CAPAS OCULTAS"].get(),
                        self.parameters["# NEURONAS OCULTAS"].get(),
                        self.parameters["SALIDAS"].get()]

        # Create a networkx graph
        G = nx.DiGraph()

        # Add nodes
        for layer, num_nodes in enumerate(architecture):
            for node in range(num_nodes):
                G.add_node(f'L{layer}_N{node}')

        # Add edges with weights
        for layer in range(1, len(architecture)):
            for i in range(architecture[layer]):
                for j in range(architecture[layer - 1]):
                    G.add_edge(f'L{layer - 1}_N{j}', f'L{layer}_N{i}', weight=weights[layer - 1][i][j])

        # Draw the graph using matplotlib
        fig, ax = plt.subplots(figsize=(6, 6))
        pos = self.get_graph_positions(architecture)

        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", ax=ax)

        # Draw edge labels (weights)
        edge_labels = {(u, v): f'{d["weight"]:.2f}' for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        # Display the graph in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

    def get_graph_positions(self, architecture):
        pos = {}
        layer_gap = 1
        node_gap = 1
        for layer, num_nodes in enumerate(architecture):
            for node in range(num_nodes):
                pos[f'L{layer}_N{node}'] = (layer * layer_gap, node * node_gap)
        return pos

    def submit(self):
        # Print the parameter values (or you can handle them as needed)
        for param, var in self.parameters.items():
            print(f"{param}: {var.get()}")
        self.network = Network(n_input=self.parameters["ENTRADAS"].get(),
                               n_hidden=self.parameters["CAPAS OCULTAS"].get(),
                               n_hidden_neurons=self.parameters["# NEURONAS OCULTAS"].get(),
                               n_output=self.parameters["SALIDAS"].get(),
                               epochs=self.parameters["ITERACIONES"].get(),
                               learning_rate=self.parameters["FACTOR DE APRENDIZAJE"].get())
        self.network.initialization()
        X = [[0, 1], [1, 0], [0, 0], [1, 1]]
        y = [[1], [1], [0], [0]]
        self.network.backpropagation(X, y, self)
