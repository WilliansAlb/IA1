import random
import math


class Network:
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

    def forward_propagation(self, x, weights, biases):
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
        z = sum(w_m * x_m for w_m, x_m in zip(neuron_weights, x))
        return z + bias

    def generate_random_weights_and_biases(self, architecture):
        weights = [self.generate_random_matrix(architecture[i], architecture[i - 1]) for i in range(1, len(architecture))]
        biases = [self.generate_random_matrix(architecture[i], 1) for i in range(1, len(architecture))]
        return weights, biases

    @staticmethod
    def generate_random_matrix(rows, cols):
        return [[random.gauss(0, 1) for _ in range(cols)] for _ in range(rows)]

    def initialization(self):
        architecture = [self.n_input]
        for _ in range(self.n_hidden):
            architecture.append(self.n_hidden_neurons)
        architecture.append(self.n_output)
        self.weights, self.biases = self.generate_random_weights_and_biases(architecture)

    def backpropagation(self, x, y, visual=None):
        for epoch in range(self.epochs):
            for xi, yi in zip(x, y):
                activations = self.forward_propagation(xi, self.weights, self.biases)
                output = activations[-1]

                error = [yi[i] - output[i] for i in range(len(yi))]

                status = '>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, self.learning_rate, error[0])
                print(status)

                deltas = [error[i] * self.sigmoid_derivative(output[i]) for i in range(len(error))]

                for i in range(len(self.weights[-1])):
                    for j in range(len(self.weights[-1][i])):
                        self.weights[-1][i][j] += self.learning_rate * deltas[i] * activations[-2][j]
                    self.biases[-1][i][0] += self.learning_rate * deltas[i]

                for layer in range(len(self.weights) - 2, -1, -1):
                    new_deltas = []
                    for neuron in range(len(self.weights[layer])):
                        error = sum(self.weights[layer + 1][j][neuron] * deltas[j] for j in range(len(deltas)))
                        delta = error * self.sigmoid_derivative(activations[layer + 1][neuron])
                        new_deltas.append(delta)
                        for w in range(len(self.weights[layer][neuron])):
                            self.weights[layer][neuron][w] += self.learning_rate * delta * activations[layer][w]
                        self.biases[layer][neuron][0] += self.learning_rate * delta
                    deltas = new_deltas

                if visual is not None:
                    print(visual.learning)
                    visual.learning.config(text=status)
