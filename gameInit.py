import pygame as pg

pg.init()

size = width, height = 800, 500
screen = pg.display.set_mode(size)

spawnEnemy = pg.USEREVENT + 1
pg.time.set_timer(spawnEnemy, 5000)

spawnLaser = pg.USEREVENT + 2
pg.time.set_timer(spawnLaser, 3000)

background = pg.image.load('sprites/background.png').convert()