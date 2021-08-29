import random
import pygame as pg
from gameInit import *

class Laser:
    def __init__(self, p1, p2) -> None:
        self.p1 = pg.Vector2(p1)
        self.p2 = pg.Vector2(p2)

    def update(self):
        self.p1.x -= 5
        self.p2.x -= 5

    def draw(self):
        pg.draw.line(screen, (255, 0, 0), self.p1, self.p2, 2)
        pg.draw.circle(screen, (255, 255, 255), self.p1, 5)
        pg.draw.circle(screen, (255, 255, 255), self.p2, 5)
    

def spawnRandomLaser():
    p1 = (random.randint(width, width * 2), random.randint(0, height))
    p2 = (random.randint(width, width * 2), random.randint(0, height))
    return Laser(p1, p2)