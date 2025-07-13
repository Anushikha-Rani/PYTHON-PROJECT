# utils.py
import pygame, math
import numpy as np
import pygame

def line_rect_collision(start: pygame.Vector2, end: pygame.Vector2, rect: pygame.Rect):
    """Return point of collision or None using clipline."""
    clipped = rect.clipline(start.x, start.y, end.x, end.y)
    if clipped:
        x1, y1 = clipped[0]
        return pygame.Vector2(x1, y1)
    return None

def compute_sensors(car, walls, sensor_range=200, angles=(-90, -45, 0, 45, 90)):
    """Cast rays from car at given angles; return normalized distances [0.0–1.0]."""
    readings = []
    pos = pygame.Vector2(car.x, car.y)
    for offset in angles:
        rad = math.radians(car.angle + offset)
        end = pos + pygame.Vector2(math.cos(rad), math.sin(rad)) * sensor_range

        min_d = sensor_range
        for w in walls:
            pt = line_rect_collision(pos, end, w)
            if pt:
                d = pos.distance_to(pt)
                if d < min_d:
                    min_d = d

        readings.append(min_d / sensor_range)  # Normalize
    return readings

def load_image(path):
    """Load and convert image for fast blitting."""
    img = pygame.image.load(path)
    return img


WIDTH, HEIGHT = 1200, 700
OBSTACLE_COLOR = (255, 0, 0)

def compute_sensors(car):
    angles = [-90,-60,-30,0,30,60,90]
    out = []
    for ao in angles:
        for d in range(1,100):
            x = int(car.pos[0] + math.cos(math.radians(car.angle+ao))*d)
            y = int(car.pos[1] + math.sin(math.radians(car.angle+ao))*d)
            if not (0<=x<WIDTH and 0<=y<HEIGHT) or pygame.Surface.get_at(pygame.display.get_surface(),(x,y))==OBSTACLE_COLOR:
                break
        out.append(d/100.0)
    return out

def compute_fitness(car):
    center_bonus = max(0, 1 - abs((car.pos[1] - HEIGHT/2)/(HEIGHT/2))) * 50
    safe_bonus = sum(car.sensors)/len(car.sensors) * 10
    return car.distance + car.time_alive*10 + center_bonus + safe_bonus
# ...existing code...

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT))  # Add this line

    class DummyCar:
        def __init__(self):
            self.pos = [WIDTH//2, HEIGHT//2]
            self.angle = 0
            self.sensors = [1, 0.8, 0.5, 0.2, 0.1, 0.9, 0.7]
            self.distance = 100
            self.time_alive = 5

    car = DummyCar()
    print("Sensors:", compute_sensors(car))
    print("Fitness:", compute_fitness(car))