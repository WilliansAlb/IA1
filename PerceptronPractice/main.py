from Perceptron import Perceptron
if __name__ == '__main__':
    perceptron = Perceptron(0.2, 0.6, 0.2, 0.4)
    perceptron.train([[0, 1], [1, 0], [0, 0], [1, 1]], [1, 1, 0, 1])
    print(perceptron.test(0, 0))
    print(perceptron.test(0, 1))
    print(perceptron.test(1, 0))
    print(perceptron.test(1, 1))
