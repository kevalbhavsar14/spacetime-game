import pygame as pg, sys
from laser import *
from ship import *
from player import PlayerShip
from gameInit import *

pg.display.set_caption('Spacetime')

player = PlayerShip(100, height/2)
enemies = []
lasers = []

jumpTime = 1

def main_loop(dt):
    pg.display.set_caption(f'Spacetime Jump - FPS : {1000//dt}')
    screen.fill((0, 0, 0))
    
    player.fly()
    player.update()
    player.draw()

    for enemy in enemies:
        enemy.persue(player)
        enemy.update()
        enemy.draw()
        if enemy.pos.y > height:
            enemies.remove(enemy)
    
    for laser in lasers:
        laser.update()
        laser.draw()
    
    if pg.key.get_pressed()[pg.K_q]:
        global jumpTime
        jumpTime += 1
        if jumpTime > 20: jumpTime = 20
        x = player.pos.x - 20
        y = player.pos.y - 40
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(x, y, 40, 10))
        pg.draw.rect(screen, (0, 255, 0), pg.Rect(x, y, jumpTime * 2, 10))

def time_jump(frames):
    for i in range(frames):
        player.update()
        for enemy in enemies:
            enemy.persue(player)
            enemy.update()
        for laser in lasers:
            laser.update()

def handle_events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == spawnEnemy:
            if len(enemies) < 6: enemies.append(spawnRandomShip())
        if event.type == spawnLaser:
            lasers.append(spawnRandomLaser())
                
        if event.type == pg.KEYUP:
            if event.key == pg.K_q:
                global jumpTime
                time_jump(jumpTime)
                jumpTime = 0

startTime = pg.time.get_ticks()
while True:
    endTime = startTime + 1
    startTime = pg.time.get_ticks()
    dt = startTime - endTime
    handle_events()
    main_loop(dt)
    pg.display.update()
    pg.time.Clock().tick(60)