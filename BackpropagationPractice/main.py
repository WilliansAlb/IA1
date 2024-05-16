from NetworkV2 import NetworkV2
import numpy as np


network = NetworkV2()
# Define the network architecture (number of neurons in each layer)
architecture = [2, 3, 4, 1]  # Including input and output layers

# Randomly initialize weights and biases for each layer
weights, biases = network.generate_random_weights_and_biases(architecture)

# Perform forward propagation for each input
output = network.forward_propagation([0, 1], weights, biases)

print(f"Input: 1 -> Output: {output}")
