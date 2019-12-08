import numpy as np

from . import model
from . import activation as act

class NeuralNetwork(model.Model):
    '''
    Simple feedforward neural network base. Inherits
    from model base, uses sigmoid activations.
    Additional flexibility to be added soon.
    '''
    def __init__(self, layers, epsilon=1, lmda=1, weights=None):
        # set internal parameters
        self.layers = layers
        self.epsilon = epsilon
        self.lmda = lmda
        self.weights = weights
        self.grad = []

        # convenient constants
        self.L = len(layers)

        # hack for now (as opposed to std non-rand init)
        if weights is None:
            self.weights = []
            self.init_weights()

    def __str__(self):
        return str(self.layers)

    @classmethod
    def from_weights(cls, weights):
        layers = []
        for block in weights:
            layers.append(block.shape[1]-1)
        layers.append(block.shape[0])
        return cls(layers, weights=weights)

    def init_weights(self):
        for i in range(self.L-1):
            # create weight state
            shape = (self.layers[i+1], self.layers[i]+1)

            # init weight array
            w = np.random.random(shape)
            w = self.epsilon*(2*w-1)
            self.weights.append(w)

            # create gradient array
            self.grad.append(np.zeros(shape))

    def forward(self, data):
        """
        Perform single forward pass through the network.
        To be used in training loop and for inference
        after training has completed. The output of the
        pass is returned by default.

        :data: input training data generator
        """
        # reset layer activations
        self.A = []

        # expect data to hold data points as rows
        # i.e. columns as features
        a = np.atleast_2d(data)

        for i, w in enumerate(self.weights):
            # create properly formatted activation
            ones = np.ones((len(a), 1))
            a = np.append(ones, a, 1)
            self.A.append(a)

            # push prior activations through current
            # layer weights
            z = np.dot(a, w.T)
            a = act.sigmoid(z)

        # return final activation/output
        return a

    def backward(self, out):
        """
        Perform single backward pass through the network.
        Uses backpropogation to update internal weights
        based on error gradients according to `cost()`
        method.
        """
        delta = out - Y
        self.grad[-1] += np.dot(delta.T, self.A[-1])
        for i in range(self.L-1, 0, -1):
            delta = delta[:,1:] if i != self.L-1 else delta
            delta = np.dot(delta, w[i])*act.dsigmoid(A[i])
            self.grad[i-1] += np.dot(delta[:,1:].T, self.A[i-1])

    def fit(self, data, batch_size=16):
            """
            Main training loop, uses `forward()` and
            `backward()` methods to perform  iterative
            improvement of model weights via backprop.
            Performs each iteration using specified batch
            size on the given data generator.

            :data: training data generator, DataLoader object
            :batch_size: size of batch to process
            """
            return forward(data)

    def predict(self, x):
        return self.forward(x)
