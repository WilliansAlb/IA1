import random
import math


class NetworkV2:
    def __init__(self, n_input, n_hidden, n_output, n_hidden_neurons, learning_rate, epochs, is_sigmoid=True, is_step=True):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_output = n_output
        self.n_hidden_neurons = n_hidden_neurons
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.biases = None
        self.is_sigmoid = is_sigmoid
        self.is_step = is_step

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def sigmoid_derivative(x):
        return x * (1 - x)

    # Forward propagation function for n hidden layers
    def forward_propagation(self, x, weights, biases):
        # Initialize input activations
        activations = [x]
        x_prev = x
        for W, b in zip(weights, biases):
            x_new = []
            for w_n, b_n in zip(W, b):
                activation = self.neuron_activation_function(w_n, x_prev, b_n[0])
                x_new.append(self.sigmoid(activation))
            activations.append(x_new)
            x_prev = x_new
        return activations

    @staticmethod
    def neuron_activation_function(neuron_weights, x, bias):
        z = 0
        for w_m, x_m in zip(neuron_weights, x):
            z += w_m * x_m
        return z + bias

    def generate_random_weights_and_biases(self, architecture):
        weights = [self.generate_random_matrix(architecture[i], architecture[i - 1]) for i in range(1, len(architecture))]
        biases = [self.generate_random_matrix(architecture[i], 1) for i in range(1, len(architecture))]
        return weights, biases

    def backpropagation(self, x, y):
        for epoch in range(self.epochs):
            for xi, yi in zip(x, y):
                # Forward propagation
                activations = self.forward_propagation(xi, self.weights, self.biases)
                output = activations[-1]

                # Error in output
                error_total = [yi[i] - output[i] for i in range(len(yi))]
                print(error_total)
                # another thing
                # Backward propagation
                deltas = [error_total[i] * self.sigmoid_derivative(output[i]) for i in range(len(error))]

                # Adjust weights and biases for output layer
                for i in range(len(self.weights[-1])):
                    for j in range(len(self.weights[-1][i])):
                        self.weights[-1][i][j] += self.learning_rate * deltas[i] * activations[-2][j]
                    self.biases[-1][i][0] += self.learning_rate * deltas[i]

                # Propagate errors back through hidden layers
                for l in range(len(self.weights) - 2, -1, -1):
                    new_deltas = []
                    for i in range(len(self.weights[l])):
                        error = sum(self.weights[l + 1][j][i] * deltas[j] for j in range(len(deltas)))
                        delta = error * self.sigmoid_derivative(activations[l + 1][i])
                        new_deltas.append(delta)
                        for j in range(len(self.weights[l][i])):
                            self.weights[l][i][j] += self.learning_rate * delta * activations[l][j]
                        self.biases[l][i][0] += self.learning_rate * delta
                    deltas = new_deltas

    @staticmethod
    def generate_random_matrix(rows, cols):
        return [[random.gauss(0, 1) for _ in range(cols)] for _ in range(rows)]

    def initialization(self):
        architecture = [self.n_input]
        for _ in range(self.n_hidden):
            architecture.append(self.n_hidden_neurons)
        architecture.append(self.n_output)
        # Randomly initialize weights and biases for each layer
        self.weights, self.biases = self.generate_random_weights_and_biases(architecture)

        # Perform forward propagation for each input
        output = self.forward_propagation([0, 1], self.weights, self.biases)
        print(f"Input: 1 -> Output: {output}")

