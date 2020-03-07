from matrix import Matrix
from math import exp
def sigmoid(x):
    return 1 / (1 + exp(x))
class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.weights_ih = Matrix(self.hidden_nodes, self.input_nodes)
        self.weights_ho = Matrix(self.output_nodes, self.hidden_nodes)
        self.weights_ih.randomize()
        self.weights_ho.randomize()
        self.bias_h = Matrix(self.hidden_nodes, 1)
        self.bias_o = Matrix(self.output_nodes, 1)
        self.bias_h.randomize()
        self.bias_o.randomize()
    def feed_forward(self, input_list):
        inputs = Matrix.fromList(input_list)
        print(inputs)
        hidden = Matrix.multiply(self.weights_ih, inputs)
        Matrix.add(hidden, self.bias_h)
        hidden.map_matrix(sigmoid)

        output = Matrix.multiply(self.weights_ho, hidden)
        Matrix.add(output, self.bias_o)
        output.map_matrix(sigmoid)
        
        return output
nn = NeuralNetwork(2, 2, 1)
inputs = [1, 0]
output = nn.feed_forward(inputs)
print(output)
        
