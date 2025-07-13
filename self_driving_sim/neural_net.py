# neural_net.py
import numpy as np

class NeuralNet:
    def __init__(self):
        self.w1 = np.random.randn(7,14)*0.1
        self.w2 = np.random.randn(14,8)*0.1
        self.w3 = np.random.randn(8,3)*0.1

    def leaky_relu(self, x): return np.where(x>0, x, x*0.01)
    def sigmoid(self, x): return 1/(1+np.exp(-x))

    def forward(self, x):
        x = np.array(x)
        self.z1 = self.leaky_relu(x.dot(self.w1))
        self.z2 = self.leaky_relu(self.z1.dot(self.w2))
        self.out = self.sigmoid(self.z2.dot(self.w3))
        return self.out
