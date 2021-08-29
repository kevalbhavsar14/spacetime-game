import pygame as pg, sys
from laser import *
from ship import *
from player import PlayerShip
from gameInit import *
from emitter import Emitter

pg.display.set_caption('Spacetime')

player = PlayerShip(100, height/2)
enemies = []
lasers = []

timeParticles = Emitter((0, 255, 0), 10, 5, 10)
jumpTime = 1
movementMul = 1

def main_loop():
    global jumpTime, movementMul
    pg.display.set_caption(f'Spacetime Jump - FPS : {1000//(dt+0.01)}')
    screen.blit(background, (0, 0))
    
    player.fly()
    player.update(movementMul)
    player.draw()

    for enemy in enemies:
        enemy.persue(player)
        enemy.update(movementMul)
        enemy.draw()
        if enemy.pos.y > height or enemy.pos.x < 0:
            enemies.remove(enemy)
    
    for laser in lasers:
        laser.update(movementMul)
        laser.draw()
        if laser.p1.x < 0 and laser.p2.x < 0:
            lasers.remove(laser)
    
    if pg.key.get_pressed()[pg.K_q]:
        jumpTime += 1
        if jumpTime > 20: jumpTime = 20
        x = player.pos.x - 20
        y = player.pos.y - 40
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(x, y, 40, 10))
        pg.draw.rect(screen, (0, 255, 0), pg.Rect(x, y, jumpTime * 2, 10))
    movementMul = 1 / jumpTime
    timeParticles.update() 

def time_jump(frames):
    for i in range(frames):
        # player.update()
        for enemy in enemies:
            enemy.persue(player)
            enemy.update()
        for laser in lasers:
            laser.update()

def handle_events():
    global jumpTime
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == spawnEnemy:
            if len(enemies) < 6: enemies.append(spawnRandomShip())
        if event.type == spawnLaser:
            lasers.append(spawnRandomLaser())
        if event.type == pg.KEYUP:
            if event.key == pg.K_q:
                time_jump(jumpTime)
                jumpTime = 1
                timeParticles(player.pos)
                for enemy in enemies:
                    timeParticles(enemy.pos)
                for laser in lasers:
                    timeParticles(laser.p1)
                    timeParticles(laser.p2)
    

startTime = pg.time.get_ticks()
while True:
    endTime = startTime + 1
    startTime = pg.time.get_ticks()
    dt = startTime - endTime
    handle_events()
    main_loop()
    pg.display.update()
    pg.time.Clock().tick(70) 