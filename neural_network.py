# neural_network.py
import numpy as np

class NeuralNetwork:
    def __init__(self, w1=None, b1=None, w2=None, b2=None):
        # Define network architecture
        self.input_size = 4
        self.hidden_size = 5
        self.output_size = 1

        # Initialize weights and biases
        if w1 is not None and b1 is not None and w2 is not None and b2 is not None:
            self.w1 = w1
            self.b1 = b1
            self.w2 = w2
            self.b2 = b2
        else:
            self.w1 = np.random.randn(self.input_size, self.hidden_size)
            self.b1 = np.random.randn(self.hidden_size)
            self.w2 = np.random.randn(self.hidden_size, self.output_size)
            self.b2 = np.random.randn(self.output_size)

    def forward(self, inputs):
        hidden = np.tanh(np.dot(inputs, self.w1) + self.b1)
        output = np.tanh(np.dot(hidden, self.w2) + self.b2)
        return output[0]  # Return scalar

    def get_parameters(self):
        return {
            'w1': self.w1.copy(),
            'b1': self.b1.copy(),
            'w2': self.w2.copy(),
            'b2': self.b2.copy()
        }

    def mutate(self, mutation_rate=0.1):
        mutation_mask_w1 = np.random.rand(*self.w1.shape) < mutation_rate
        self.w1 += np.random.randn(*self.w1.shape) * mutation_mask_w1

        mutation_mask_b1 = np.random.rand(*self.b1.shape) < mutation_rate
        self.b1 += np.random.randn(*self.b1.shape) * mutation_mask_b1

        mutation_mask_w2 = np.random.rand(*self.w2.shape) < mutation_rate
        self.w2 += np.random.randn(*self.w2.shape) * mutation_mask_w2

        mutation_mask_b2 = np.random.rand(*self.b2.shape) < mutation_rate
        self.b2 += np.random.randn(*self.b2.shape) * mutation_mask_b2
