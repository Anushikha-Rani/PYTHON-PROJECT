# main.py
import pygame, sys
from self_driving_sim.car import Car
from self_driving_sim.population import Population
from self_driving_sim import car
from self_driving_sim.viz import draw_nn
from self_driving_sim.utils import WIDTH, HEIGHT
from self_driving_sim.utils import compute_sensors


import pygame
from self_driving_sim.utils import load_image
from self_driving_sim.dirty_manager import GameManager

def main():
    pygame.init()
    
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE  # hardware acceleration
    screen = pygame.display.set_mode((800, 600), flags, 16)
    pygame.display.set_caption("Optimized Pygame App")
    clock = pygame.time.Clock()

    bg_surf = load_image("background.jpg").convert()
    sprite_img = load_image("player.png").convert_alpha()

    manager = GameManager(screen, bg_surf, sprite_img)

    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION])

    running = True
    while running:
        # e.g., if your walls is a list of pygame.Rect
        car.sensors = compute_sensors(car, walls)


        dt = clock.tick(60) / 1000.0  # delta time in seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

        manager.update(dt)
        dirty = manager.draw()
        pygame.display.update(dirty)

    pygame.quit()

if __name__ == "__main__":
    main()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial",24)

MODE_SINGLE = 0
MODE_POP = 1

def main():
    mode = MODE_SINGLE
    pop = Population(size=20)
    current = 0

    while True:
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255,0,0), (WIDTH//2,0,10,HEIGHT))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            mode = MODE_POP if mode==MODE_SINGLE else MODE_SINGLE

        if mode==MODE_SINGLE:
            car = Car(); net = pop.nets[0]
            sensors = net.forward(car.sensors)
            car.update(sensors)
            pygame.draw.rect(screen, (0,0,255), car.get_rect())
            draw_nn(screen, net)
            screen.blit(FONT.render("Mode: SINGLE  (Press SPACE)", True, (255,255,255)), (10,10))

        else:
            pop.evaluate()
            best_i = pop.fitness.argmax()
            car = Car(); net = pop.nets[best_i]
            while car.alive:
                car.sensors = compute_sensors(car)
                car.update(net.forward(car.sensors))
            pygame.draw.rect(screen, (0,255,0), car.get_rect())
            draw_nn(screen, net)
            screen.blit(FONT.render(f"POP Mode: Gen Best Fitness={pop.fitness[best_i]:.1f}", True, (255,255,255)), (10,10))
            pop.evolve()

        pygame.display.flip()
        for evt in pygame.event.get():
            if evt.type in (pygame.QUIT, pygame.KEYDOWN) and evt.key==pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
        clock.tick(60)

if __name__=="__main__":
    main()
