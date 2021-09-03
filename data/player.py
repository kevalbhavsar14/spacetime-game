import pygame as pg, math
from data.ship import Ship
from data.emitter import Emitter
from data.gameInit import screen

class PlayerShip(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 0))
        self.sprite = pg.image.load('data/sprites/playerShip.png').convert_alpha()
        self.sheildSprite = pg.image.load('data/sprites/sheild.png').convert_alpha()
        self.flyParticles = Emitter((255, 255, 0), 10, 1)
        self.invincibleTime = 0
        self.lives = 3
        self.angle = 0
        self.flySound.set_volume(0.1)
    
    def update(self, m = 1):
        self.vel.y += 0.5
        super().update(m)
        self.angle = -self.vel.y * math.pi / 90
        if self.invincibleTime > 0: self.invincibleTime -= 1

    def updateParticles(self, m = 1):
        self.particles(self.pos - pg.Vector2(20, 0))
        self.particles.applyForce((-1, 0))
        self.particles.update(m)
        self.flyParticles.update(m)
    
    def fly(self):
        if pg.key.get_pressed()[pg.K_SPACE] and self.pos.y > 50:
            self.vel.y = -5
            self.flyParticles(self.pos)
            self.flySound.set_volume(0.2)
        else:
            self.flySound.set_volume(0.1)

    
    def activateShield(self):
        self.invincibleTime = 120
    
    def draw(self):
        sprite = pg.transform.rotozoom(self.sprite, self.angle * 180 / math.pi, 0.2)
        sheildSprite = pg.transform.rotozoom(self.sheildSprite, 0, 0.2)
        w, h = sprite.get_width(), sprite.get_height()
        x = self.pos.x - w / 2
        y = self.pos.y - h / 2
        if self.invincibleTime > 0 and self.lives > 0: screen.blit(sheildSprite, (x + w/2 - sheildSprite.get_width()/2, y + h/2 - sheildSprite.get_height()/2))
        screen.blit(sprite, (x, y))