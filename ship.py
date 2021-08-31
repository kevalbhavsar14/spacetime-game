import pygame as pg
import math, random
from gameInit import *
from laser import Laser
from emitter import Emitter

class Ship:
    def __init__(self, x, y, vel):
        self.angle = random.randint(0, 360)
        self.collisionRadius = 20
        vx = 5 *  math.cos(self.angle)
        vy = 5 * -math.sin(self.angle)
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(vel)
        self.sprite = pg.image.load('sprites/ship.png').convert_alpha()
        self.particles = Emitter((255, 100, 0), 10, 1)
    
    def update(self, m = 1):
        maxVel = 15
        if self.vel.length() > maxVel: self.vel.scale_to_length(maxVel)
        vel = pg.Vector2(self.vel)
        if self.vel.length() * m > 0: vel.scale_to_length(self.vel.length() * m)
        self.pos += vel
        self.angle = (self.vel.angle_to(pg.Vector2(1, 0))) * math.pi / 180
        self.updateParticles(m)
        
    def updateParticles(self, m = 1):
        self.particles(self.pos)
        self.particles.update(m)
    
    def persue(self, target):
        desiredVel = target.pos - self.pos
        self.vel += desiredVel.normalize()
    
    def collideShip(self, ship):
        p1 = (self.pos.x, self.pos.y)
        p2 = (ship.pos.x, ship.pos.y)
        d = math.dist(p1, p2)
        return d < self.collisionRadius + ship.collisionRadius

    def collideLaser(self, laser: Laser):
        pos = (self.pos.x, self.pos.y)
        p1 = (laser.p1.x, laser.p1.y)
        p2 = (laser.p2.x, laser.p2.y)
        d = math.dist(p1, p2)
        d1 = math.dist(pos, p1)
        d2 = math.dist(pos, p2)
        if d1 < self.collisionRadius or d2 < self.collisionRadius:
            return True
        return d > d1 + d2 - self.collisionRadius / 4
    
    def draw(self):
        sprite = pg.transform.rotozoom(self.sprite, self.angle * 180 / math.pi, 0.2)
        x = self.pos.x - sprite.get_width() / 2
        y = self.pos.y - sprite.get_height() / 2
        screen.blit(sprite, (x, y))

def spawnRandomShip():
    x = random.randint(width, width * 2)
    y = random.randint(-height, 0)
    angle = random.uniform(0, (math.pi * 2))
    vx = 5 *  math.cos(angle)
    vy = 5 * -math.sin(angle)
    return Ship(x, y, (vx, vy))
