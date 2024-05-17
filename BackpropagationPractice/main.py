from Network import Network
from NetworkInterface import NetworkInterface
import tkinter as tk

if __name__ == '__main__':
    visual = True

    if not visual:
        network = Network(n_input=2, n_hidden=2, n_hidden_neurons=2, n_output=1, epochs=100000, learning_rate=0.02)
        network.initialization()
        X = [[0, 1], [1, 0], [0, 0], [1, 1]]
        y = [[1], [1], [0], [0]]
        network.backpropagation(X, y)
        for xi in X:
            output = network.forward_propagation(xi, network.weights, network.biases)[-1]
            print(f"Input: {xi} -> Output: {1 if output[0] > 0.5 else 0}")
    else:
        root = tk.Tk()
        app = NetworkInterface(root)
        root.mainloop()
