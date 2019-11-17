from . import model

class NeuralNetwork(model.Model):
  '''
  Simple feedforward neural network base. Inherits
  from model base, uses sigmoid activations.
  Additional flexibility to be added soon.
  '''
  def __init__(self, layers, epsilon=1, lmda=1):
    self.layers = layers
    self.epsilon = epsilon
    self.lmda = lmda
    
    self.init_weights(layers, epsilon)

  def init_weights(layers, epsilon):
    this.weights = []
    for i in range(len(layers)-1):
      w = np.random.rand(layers[i+1], layers[i]+1)
      w = w * 2*epsilon - epsilon
      this.weights.append(w)

  def forward(self):
      """
      Perform single forward pass through the network.
      To be used in training loop and for inference
      after training has completed. The output of the
      pass is returned by default.
      """
      pass

  def backward(self):
      """
      Perform single backward pass through the network.
      Uses backpropogation to update internal weights
      based on error gradients according to `cost()`
      method.
      """
      pass

  def fit(self, data, batch_size=16):
      """
      Main training loop, uses `forward()` and 
      `backward()` methods to perform  iterative
      improvement of model wieghts via backprop.
      Performs each iteration using specified batch
      size on the given data generator.

      :data: training data generator, DataLoader object 
      :batch_size: size of batch to process 
      """
      pass

  def predict(self, x):
    return self.forward(x)
