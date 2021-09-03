import random
import pygame as pg
from data.gameInit import *

class Laser:
    def __init__(self, p1, p2) -> None:
        self.p1 = pg.Vector2(p1)
        self.p2 = pg.Vector2(p2)
        self.endSprite = pg.image.load('data/sprites/laserEnd.png').convert_alpha()

    def update(self, m = 1):
        self.p1.x -= 5 * m
        self.p2.x -= 5 * m

    def draw(self):
        pg.draw.line(screen, (255, 0, 0), self.p1, self.p2, 3)
        angle1 = (self.p2 - self.p1).angle_to(pg.Vector2(1, 0))
        angle2 = (self.p1 - self.p2).angle_to(pg.Vector2(1, 0))
        sprite1 = pg.transform.rotozoom(self.endSprite, angle1, 0.2)
        sprite2 = pg.transform.rotozoom(self.endSprite, angle2, 0.2)
        p1 = (self.p1.x - sprite1.get_width() / 2, self.p1.y - sprite1.get_height() / 2)
        p2 = (self.p2.x - sprite2.get_width() / 2, self.p2.y - sprite2.get_height() / 2)
        screen.blit(sprite1, p1)
        screen.blit(sprite2, p2)
    

def spawnRandomLaser():
    p1 = (random.randint(width, width * 2), random.randint(0, 440))
    p2 = (random.randint(width, width * 2), random.randint(0, 440))
    return Laser(p1, p2)