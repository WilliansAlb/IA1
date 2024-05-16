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

    def backpropagation(self, X, y):
        for epoch in range(self.epochs):
            for xi, yi in zip(X, y):
                # Forward propagation
                activations = self.forward_propagation(xi, self.weights, self.biases)
                output = activations[-1]
                print(output)

                # Error in output
                error = [yi[i] - output[i] for i in range(len(yi))]

                # Backward propagation
                deltas = [error[i] * self.sigmoid_derivative(output[i]) for i in range(len(error))]

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

# Ejemplo de uso:
network = NetworkV2(n_input=2, n_hidden=2, n_output=1, n_hidden_neurons=2, learning_rate=0.5, epochs=10000)
network.initialization()
X = [[0, 1], [1, 0], [0, 0], [1, 1]]
y = [[1], [1], [0], [0]]
network.backpropagation(X, y)

# Evaluar la red
for xi in X:
    output = network.forward_propagation(xi, network.weights, network.biases)[-1]
    print(f"Input: {xi} -> Output: {1 if output[0] > 0.5 else 0}")