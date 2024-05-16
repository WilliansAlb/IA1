import random
import math


class NetworkV2:
    def __init__(self):
        pass

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    # Forward propagation function for n hidden layers
    def forward_propagation(self, x, weights, biases):
        # Initialize input activations
        x_prev = x

        # Loop through each hidden layer
        for W, b in zip(weights, biases):
            activations = []
            for w_n, b_n in zip(W, b):
                z = 0
                for w_m, x_m in zip(w_n, x_prev):
                    z += w_m * x_m
                activations.append(z + b_n[0])
            x_new = []
            for activate in activations:
                x_new.append(self.sigmoid(activate))
            x_prev = x_new
        return x_prev[0]

    def generate_random_weights_and_biases(self, architecture):
        weights = [self.generate_random_matrix(architecture[i], architecture[i - 1]) for i in range(1, len(architecture))]
        biases = [self.generate_random_matrix(architecture[i], 1) for i in range(1, len(architecture))]
        return weights, biases

    @staticmethod
    def generate_random_matrix(rows, cols):
        return [[random.gauss(0, 1) for _ in range(cols)] for _ in range(rows)]

