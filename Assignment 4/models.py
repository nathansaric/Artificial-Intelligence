# =============================
# Student Names: Hannah Larsen, Nathan Saric
# Group ID: Group 13
# Date: April 17, 2022
# =============================

import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        weights = self.get_weights()
        return nn.DotProduct(weights, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        prediction = nn.as_scalar(self.run(x))

        if (prediction >= 0): # Non-negative -> returns 1
            return 1
        else: # Negative -> returns -1
            return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        # Setting our misclassified boolean to true as default
        misclassified = True

        # Continue the training process until the training accuracy is 100%
        while misclassified:
            # Stop the training process when the training accuracy is 100%
            misclassified = False

            # Iterate through the dataset using batch_size = 1
            for (x, y) in dataset.iterate_once(1):
                
                # If a given prediction is not equal to its corresponding output label
                if self.get_prediction(x) != nn.as_scalar(y):
                    # Update the weights of self
                    self.get_weights().update(nn.as_scalar(y), x)
                    # Continue the training process
                    misclassified = True

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize the model parameters
        """
        Tried multiple variations of parameters and this combo was the closest I could get
        to 0.02. After multiple runs, it gets a loss of around 0.019
        """
        self.batch_size = 40          # Variable: between 1 and the size of the dataset
        self.learning_rate = -0.1     # Variable: between 0.001 and 1
        self.num_layers = 3           # Variable: between 1 and 3
        self.layers = []          
        self.parameters = [        
            nn.Parameter(1, 300),   # w1
            nn.Parameter(300, 100), # w2
            nn.Parameter(100, 1),   # w3
            nn.Parameter(1, 300),   # b1
            nn.Parameter(1, 100),   # b2
            nn.Parameter(1, 1)]     # b3

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        # Iterate through the number of layers in the model    
        for layer in range(self.num_layers):

            # The very first layer we do not apply the element-wise Rectified Linear Unit, 
            # instead we apply the linear transformation and add a bias vector to each feature vector. 
            if (layer == 0):
                self.layers.append(nn.AddBias(nn.Linear(x, self.parameters[layer]), self.parameters[layer + self.num_layers]))
            # All of the following layers we apply the element-wise Rectified Learner Unit, 
            # in addition to applying the linear transformation and adding a bias vector to each feature vector.  
            else:
                self.layers.append(nn.AddBias(nn.Linear(nn.ReLU(self.layers[-1]), self.parameters[layer]), self.parameters[layer + self.num_layers]))

        # Return the final layer of the model containing the predicted y-values
        return (self.layers[-1])

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        return (nn.SquareLoss(self.run(x), y))

    def train(self, dataset):
        """
        Trains the model.
        """
        # Setting our loss to 1 as default
        loss = 1

        # Continue the training process until a loss of at least 0.015 is acheived
        while (loss >= 0.015):

            # Iterate through the dataset using batch_size = 100
            for (x, y) in dataset.iterate_once(self.batch_size):
                # Obtain the gradient of the loss with respect to the parameters
                gradients = nn.gradients(self.parameters, self.get_loss(x, y))
                # Calculate the new loss (as a scalar value)
                loss = nn.as_scalar(self.get_loss(x, y))

                # Updating the weights for each parameter in the model
                for parameter in range(len(self.parameters)):
                    self.parameters[parameter].update(self.learning_rate, gradients[parameter])

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize the model parameters
        """ 
        Opted to change params as follows: 
        Batch size: 80
        x: 300
        y: 75
        After running it three times with the autograder, we recieved results as follows:
        Run 1: accuracy = 97.56%
        Run 2: accuracy = 97.76%
        Run 3: accuracy = 97.84% 
        """
        self.batch_size = 80         # Variable: between 1 and the size of the dataset
        self.learning_rate = -0.1    # Variable: between 0.001 and 1 -> was giving errors when we set to positive, but works fine as -0.1
        self.num_layers = 3          # Variable: between 1 and 3
        self.layers = []
        self.parameters = [         
            nn.Parameter(784, 300),  # w1
            nn.Parameter(300, 75),   # w2
            nn.Parameter(75, 10),    # w3
            nn.Parameter(1, 300),    # b1
            nn.Parameter(1, 75),     # b2
            nn.Parameter(1, 10)]     # b3

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        # Iterate through the number of layers in the model    
        for layer in range(self.num_layers):

            # The very first layer we do not apply the element-wise Rectified Linear Unit, 
            # instead we apply the linear transformation and add a bias vector to each feature vector. 
            if layer == 0:
                self.layers.append(nn.AddBias(nn.Linear(x, self.parameters[layer]), self.parameters[layer + self.num_layers]))
            # All of the following layers we apply the element-wise Rectified Learner Unit, 
            # in addition to applying the linear transformation and adding a bias vector to each feature vector.
            else:
                self.layers.append(nn.AddBias(nn.Linear(nn.ReLU(self.layers[-1]), self.parameters[layer]), self.parameters[layer + self.num_layers]))

        # Return the final layer of the model containing the predicted scores (logits)
        return (self.layers[-1])

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        return (nn.SoftmaxLoss(self.run(x), y))

    def train(self, dataset):
        """
        Trains the model.
        """
        # Continue the training process until a validation accuracy of at least 97.5% is acheived
        while (dataset.get_validation_accuracy() <= 0.98):

            # Iterate through the dataset using batch_size = 100
            for (x, y) in dataset.iterate_once(self.batch_size):
                # Obtain the gradient of the loss with respect to the parameters
                gradients = nn.gradients(self.parameters, self.get_loss(x, y))

                # Updating the weights for each parameter in the model
                for parameter in range(len(self.parameters)):
                    self.parameters[parameter].update(self.learning_rate, gradients[parameter])