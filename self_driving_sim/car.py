# car.py
import pygame, math, numpy as np
from self_driving_sim.utils import WIDTH, HEIGHT, OBSTACLE_COLOR


class Car:
    def __init__(self):
        self.pos = np.array([WIDTH//3, HEIGHT//2], dtype=float)
        self.angle = 0.0
        self.speed = 0.0
        self.max_speed = 5.0
        self.sensors = [0.0]*7
        self.alive = True
        self.distance = 0.0
        self.time_alive = 0.0

    def update(self, outputs):
        if not self.alive: return
        turn_l, turn_r, move = outputs
        self.angle += (turn_r - turn_l) * 5.0
        self.speed = move * self.max_speed
        rad = math.radians(self.angle)
        self.pos += np.array([math.cos(rad), math.sin(rad)]) * self.speed
        self.distance += self.speed
        self.time_alive += 1/60.0
        self.check_collision()

    def check_collision(self):
        x, y = int(self.pos[0]), int(self.pos[1])
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT) or pygame.Surface.get_at(pygame.display.get_surface(), (x,y)) == OBSTACLE_COLOR:
            self.alive = False

    def get_rect(self):
        return pygame.Rect(self.pos[0]-10, self.pos[1]-15, 20, 30)
