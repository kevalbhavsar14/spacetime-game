import pygame as pg, math
from ship import Ship

class PlayerShip(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 0))
        self.sprite = pg.image.load('sprites/playerShip.png').convert_alpha()
    
    def update(self):
        self.vel.y += 0.5
        super().update()
        self.angle = -self.vel.y * math.pi / 90
    
    def fly(self):
        if pg.key.get_pressed()[pg.K_SPACE]:
            self.vel.y = -5