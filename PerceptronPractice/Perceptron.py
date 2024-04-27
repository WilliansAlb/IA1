class Perceptron:
    def __init__(self, weight1, weight2, learning_factor, threshold):
        self.weight1 = weight1
        self.weight2 = weight2
        self.bias = - threshold
        self.learning_rate = learning_factor
        self.threshold = threshold

    @staticmethod
    def error(obtained, predicted):
        return predicted - obtained

    def delta_threshold(self, obtained, predicted):
        return -(self.learning_rate * self.error(obtained, predicted))

    def delta_weight(self, obtained, predicted, value):
        return self.learning_rate * self.error(obtained, predicted) * value

    def train(self, training_inputs, expected_outputs):
        iterations = 1
        while True:
            print(f"Iteration {iterations}")
            iterations += 1
            sum_percentage = 0
            for input_value, output in zip(training_inputs, expected_outputs):
                predicted = input_value[0] * self.weight1 + input_value[1] * self.weight2 + self.bias
                activate = 1 if predicted >= 0 else 0
                print(input_value, output)
                self.threshold = self.threshold + self.delta_threshold(activate, output)
                self.bias = - self.threshold
                self.weight1 = self.weight1 + self.delta_weight(activate, output, input_value[0])
                self.weight2 = self.weight2 + self.delta_weight(activate, output, input_value[1])
                sum_percentage += abs(((activate - output) / output * 100)) if output != 0 else 0
            print(sum_percentage)
            if sum_percentage == 0:
                break
        print("Trained")

    def test(self, x1, x2):
        return 1 if (self.weight1 * x1 + self.weight2 * x2 + self.bias) >= 0 else 0
