import pygame as pg, math
from ship import Ship
from emitter import Emitter

class PlayerShip(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 0))
        self.sprite = pg.image.load('sprites/playerShip.png').convert_alpha()
        self.flyParticles = Emitter((255, 255, 0), 10, 1)
    
    def update(self, m = 1):
        self.vel.y += 0.5
        super().update(m)
        self.angle = -self.vel.y * math.pi / 90
        self.particles.applyForce((-1, 0))

    def updateParticles(self, m = 1):
        self.particles(self.pos - pg.Vector2(20, 0))
        self.particles.update(m)
        self.flyParticles.update(m)
    
    def fly(self):
        if pg.key.get_pressed()[pg.K_SPACE]:
            self.vel.y = -5
            self.flyParticles(self.pos)