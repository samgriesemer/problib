class Model():
  '''
  Base model class for machine learning algorithms. Outlines
  a `fit()` method for training on (internal?) data, and a 
  `predict()` method for inference on test data. This is a
  very light and incomplete blueprint, leaving all definitions
  to subclassing models.
  '''
  def __init__(self):
    pass

  def fit(self, data):
    pass

  def predict(self, x):
    pass
