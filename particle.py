import pygame as pg, math, random
from gameInit import *

class Particle:
    def __init__(self, pos, velMag, lifeSpan, color) -> None:
        self.pos = pg.Vector2(pos)
        angle = random.uniform(0, math.pi * 2)
        vx = velMag *  math.cos(angle)
        vy = velMag * -math.sin(angle)
        self.vel = pg.Vector2(vx, vy)
        self.acc = pg.Vector2(0, 0)
        self.maxLifeSpan = lifeSpan
        self.lifeSpan = lifeSpan
        # self.color = [color[0], color[1], color[2], 255]
        self.sprite = pg.Surface((5, 5))
        self.sprite.fill(color)
    
    def update(self, m = 1):
        self.vel += self.acc
        vel = pg.Vector2(self.vel)
        if self.vel.length() * m > 0: vel.scale_to_length(self.vel.length() * m)
        self.pos += vel
        self.acc.update(0, 0)
        self.lifeSpan -= 1
    
    def applyForce(self, force):
        self.acc += pg.Vector2(force)
    
    def draw(self):
        # self.color[3] = int(self.lifeSpan * 200 / self.maxLifeSpan)
        # pg.draw.rect(screen, self.color, pg.Rect(self.pos.x, self.pos.y, 5, 5))
        self.sprite.set_alpha(int(self.lifeSpan * 200 / self.maxLifeSpan))
        screen.blit(self.sprite, (self.pos.x, self.pos.y))
