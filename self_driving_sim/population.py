# population.py
import numpy as np, random
from self_driving_sim.car import Car
from self_driving_sim.neural_net import NeuralNet
from self_driving_sim.utils import compute_sensors, compute_fitness

class Population:
    def __init__(self, size=20):
        self.size = size
        self.nets = [NeuralNet() for _ in range(size)]
        self.fitness = np.zeros(size)

    def evaluate(self):
        for i, net in enumerate(self.nets):
            car = Car()
            while car.alive and car.time_alive < 20.0:
                car.sensors = compute_sensors(car)
                out = net.forward(np.array(car.sensors))
                car.update(out)
            self.fitness[i] = compute_fitness(car)

    def evolve(self):
        idx = np.argsort(self.fitness)[::-1]
        top = idx[:self.size//5]
        new_nets = []
        for _ in range(self.size):
            p1, p2 = random.sample(list(top), 2)
            child = NeuralNet()
            child.w1 = (self.nets[p1].w1 + self.nets[p2].w1)/2
            child.w2 = (self.nets[p1].w2 + self.nets[p2].w2)/2
            child.w3 = (self.nets[p1].w3 + self.nets[p2].w3)/2
            # mutation:
            child.w1 += np.random.randn(*child.w1.shape)*0.1
            child.w2 += np.random.randn(*child.w2.shape)*0.1
            child.w3 += np.random.randn(*child.w3.shape)*0.1
            new_nets.append(child)
        self.nets = new_nets
