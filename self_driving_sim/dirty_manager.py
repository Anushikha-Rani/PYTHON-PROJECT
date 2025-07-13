import pygame
from pygame.sprite import DirtySprite, LayeredDirty

class PlayerSprite(DirtySprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=(400, 300))
        self.dirty = 1  # always considered dirty initially

    def update(self, dt):
        # Example: move via arrow keys
        vx = vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: vx -= 200 * dt
        if keys[pygame.K_RIGHT]: vx += 200 * dt
        if keys[pygame.K_UP]: vy -= 200 * dt
        if keys[pygame.K_DOWN]: vy += 200 * dt

        if vx or vy:
            self.rect.move_ip(vx, vy)
            self.dirty = 1

class GameManager:
    def __init__(self, screen, bg_surf, player_img):
        self.screen = screen
        self.background = bg_surf
        self.all_sprites = LayeredDirty()
        self.all_sprites.clear(screen, bg_surf)
        self.player = PlayerSprite(player_img)
        self.all_sprites.add(self.player)

    def handle_event(self, event):
        pass  # extend as needed

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self):
        # clear previous sprites, redraw only dirty ones
        self.all_sprites.clear(self.screen, self.background)
        rects = self.all_sprites.draw(self.screen)
        return rects
