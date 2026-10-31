import numpy as np
import random

class NeuralBrain:
    def __init__(self, num_inputs=5, weights=None, bias=None):
        self.num_inputs = num_inputs
        
        # Create new gene for bird
        if weights is not None:
            self.weights = np.array(weights, dtype=float)
        else:
            self.weights = np.random.uniform(-3.0, 3.0, size=self.num_input)

        # Create new bias
        if bias is not None:
            self.bias = float(bias)
        else:
            self.bias = random.uniform(-3.0, 3.0)

    def predict(self, inputs):
        assert len(inputs) == self.num_inputs, (
            f"Kích thước inputs ({len(inputs)}) không khớp với số nơ-ron ({self.num_inputs})!"
        )

        '''
		inputs[0] = bird.y              # vị trí chim (đang cao hay thấp?)
		inputs[1] = bird.velocity  		# đang rơi nhanh hay chậm?
		inputs[2] = dist_to_tube        # cách cột bao xa?
		inputs[3] = gap_top_y           # khe hở phía trên ở đâu?
		inputs[4] = gap_bottom_y        # khe hở phía dưới ở đâu?

		neuron: y = w * x + b
		-> y = w1 * x1 + w2 * x2 + w3 * x3 + w4 * x4 + w5 * x5 + b
		'''
        x = np.array(inputs, dtype=float)
        y = np.dot(self.weights, x) + self.bias

        # use sigmoid function to decide (output: 0.0 to 1.0)
		output = 1 / (1 + np.exp(-y))

        return output

    def get_chromosome(self):
        # [w1, w2, w3, w4, w5, bias]
        chromosome = list(self.weights)
        chromosome.append(self.bias)
        return chromosome


