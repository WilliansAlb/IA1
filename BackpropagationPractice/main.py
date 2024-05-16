from NetworkV2 import NetworkV2
import numpy as np


network = NetworkV2(n_input=2, n_hidden=2, n_hidden_neurons=3, n_output=1, epochs=1000, learning_rate=0.02)
network.initialization()
