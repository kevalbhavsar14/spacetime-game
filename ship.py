import pygame as pg
import math, random
from gameInit import *

from pygame.math import Vector2

class Ship:
    def __init__(self, x, y, vel):
        self.angle = random.randint(0, 360)
        self.collisionRadius = 20
        vx = 5 *  math.cos(self.angle)
        vy = 5 * -math.sin(self.angle)
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(vel)
        self.sprite = pg.image.load('sprites/ship.png').convert_alpha()
    
    def update(self):
        maxVel = 15
        if self.vel.length() > maxVel: self.vel.scale_to_length(maxVel)
        self.pos += self.vel
        self.angle = (self.vel.angle_to(Vector2(1, 0))) * math.pi / 180
    
    def persue(self, target):
        desiredVel = target.pos - self.pos
        self.vel += desiredVel.normalize()
    
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
