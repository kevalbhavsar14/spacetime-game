import pygame as pg, sys
from data.laser import *
from data.ship import *
from data.player import PlayerShip
from data.gameInit import *
from data.emitter import Emitter

pg.display.set_caption('Spacetime Breaker')

player = PlayerShip(200, height/2)
enemies = []
lasers = []

hsfile = open('data/files/highscore', 'r+')

score = 0
highscore = int(hsfile.read())
gameIsRunning = False

timeParticles = Emitter((0, 255, 0), 10, 5, 50)
explosions = [Emitter((255, 255, 0), 30, 5, 50), Emitter((255, 0, 0), 30, 3, 30)]
jumpTime = 1
jumpCD = 0
movementMul = 1
groundX = 0

bgm = bgMusic.play(-1)
bgm.set_volume(0.5)

def main_loop():
    global jumpTime, movementMul, groundX, jumpCD, score, highscore, gameIsRunning
    screen.blit(background, (0, 0))
    
    if player.lives > 0: player.fly()
    player.update(movementMul)
    player.draw()

    for enemy in enemies:
        enemy.pursue(player)
        enemy.update(movementMul)
        enemy.draw()
        enemy.playSound(player.pos)
        if enemy.pos.y > 440 or enemy.pos.x < 0:
            explosions[0](enemy.pos)
            # enemy.flySound.stop()
            enemies.remove(enemy)
        if player.collideShip(enemy) and player.invincibleTime <= 0:
            explosions[0](enemy.pos)
            explosions[0](player.pos)
            # enemy.flySound.stop()
            enemies.remove(enemy)
            player.lives -= 1
            explosions[1]((30 + (player.lives) * 40, 30))
            player.activateShield()
    
    for laser in lasers:
        laser.update(movementMul)
        laser.draw()
        if player.collideLaser(laser) and player.invincibleTime <= 0:
            explosions[0](player.pos)
            player.lives -= 1
            explosions[1]((30 + (player.lives) * 40, 30))
            player.explodeSound.play()
            player.activateShield()
        if laser.p1.x < 0 and laser.p2.x < 0:
            lasers.remove(laser)
    
    if player.lives <= 0:
        movementMul = 1
        jumpTime = 1
    
    if pg.key.get_pressed()[pg.K_q] and jumpCD <= 0 and player.lives > 0:
        jumpTime += 1
        pg.mixer.pause()
        bgm.set_volume(0)
        bgm.unpause()
        if jumpTime > 20: time_jump(jumpTime)

    if jumpCD > 0: jumpCD -= dt
    movementMul = 1 / jumpTime

    score += dt
    highscore = max(score, highscore)
    hsfile.seek(0)
    hsfile.write(str(int(highscore)))

    if player.pos.y > 440:
        explosions[0](player.pos)
        player.lives = 0
        pg.mixer.stop()
        player.explodeSound.play()
        gameIsRunning = False
    
    timeParticles.update()
    for explosion in explosions:
        explosion.update()
    explosions[1].applyForce((0, 0.1))

    groundX = (groundX - 5 * movementMul) % width
    screen.blit(ground, (groundX, 0))
    screen.blit(ground, (groundX - width, 0))

def time_jump(frames):
    global groundX, jumpTime, jumpCD
    pg.mixer.unpause()
    timeJumpSound.play()
    bgm.set_volume(0.5)
    for i in range(frames):
        # player.update()
        for enemy in enemies:
            # enemy.persue(player) 
            enemy.update()
        for laser in lasers:
            laser.update()
        groundX = (groundX - 5 * movementMul) % width
    jumpTime = 1
    jumpCD = frames / 10
    timeParticles(player.pos)
    for enemy in enemies:
        timeParticles(enemy.pos)
    for laser in lasers:
        timeParticles(laser.p1)
        timeParticles(laser.p2)

def draw_interface(): 
    global gameIsRunning
    if gameIsRunning:
        if pg.key.get_pressed()[pg.K_q] and jumpCD <= 0 and player.lives > 0:
            x = player.pos.x - 20
            y = player.pos.y - 40
            pg.draw.rect(screen, (255, 255, 255), pg.Rect(x, y, 40, 10))
            pg.draw.rect(screen, (0, 255, 0), pg.Rect(x, y, jumpTime * 2, 10))
        highscoreText = gameFont.render(f'Hi-score : {int(highscore)}', False, (255, 255, 255))
        scoreText = gameFont.render(f'Score : {int(score)}', False, (255, 255, 255))
        screen.blit(scoreText, (width - scoreText.get_width() - 10, 0))
        screen.blit(highscoreText, (width - highscoreText.get_width() - 30 - scoreText.get_width(), 0))
        screen.blit(timeJumpIcon, (10, 60))
        screen.blit(gameFont.render('Q', False, (255, 255, 255)), (60, 62))
        if jumpCD > 0:
            cd = pg.Surface((40, 40))
            cd.fill((0, 0, 0))
            cd.set_alpha(200)
            screen.blit(cd, (10, 60))
            w, h = gameFont.size(f'{round(jumpCD, 1)}')
            cdText = gameFont.render(f'{round(jumpCD, 1)}', False, (255, 255, 255))
            screen.blit(cdText, (10 + timeJumpIcon.get_width()/2 - w/2 + 2, 60 + timeJumpIcon.get_height()/2 - h/2 - 2))
        for i in range(player.lives):
            screen.blit(lifeIcon, (10 + i * 40, 10))
    else:
        if player.lives > 0:
            screen.blit(startText, (width/2 - startText.get_width() / 2 + 150, 360))
            screen.blit(logo, (width/2 - logo.get_width() / 2 + 150, 0))
        else:
            w, h = titleFont.size(f'Score : {int(score)}')
            hw, hh = gameFont.size(f'HighScore : {int(highscore)}')
            screen.blit(crashText, (width/2 - crashText.get_width()/2 - 10, height/2 - crashText.get_height()/2 - 30))
            screen.blit(titleFont.render(f'Score : {int(score)}', False, (255, 255, 255)), (width/2 - w/2 - 10, height/2 - h/2))
            screen.blit(gameFont.render(f'HighScore : {int(highscore)}', False, (255, 255, 255)), (width/2 - hw/2 - 10, height/2 - hh/2 + 40))
            screen.blit(endText, (width/2 - endText.get_width() / 2 - 10, 300))

def startScreen():
    global groundX
    screen.blit(background, (0, 0))

    player.updateParticles()
    player.draw()

    groundX = (groundX - 5 * movementMul) % width
    screen.blit(ground, (groundX, 0))
    screen.blit(ground, (groundX - width, 0))

def handle_events():
    global jumpTime, jumpCD, gameIsRunning, player, score, movementMul
    for event in pg.event.get():
        if event.type == pg.QUIT:
            hsfile.close()
            sys.exit()
        if gameIsRunning:
            if event.type == spawnEnemy:
                if len(enemies) < 6: enemies.append(spawnRandomShip())
            if event.type == spawnLaser:
                lasers.append(spawnRandomLaser())
            if event.type == pg.KEYUP and jumpCD <= 0:
                if event.key == pg.K_q and player.lives > 0:
                    time_jump(jumpTime)
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if player.lives > 0:
                        gameIsRunning = True
                elif event.key == pg.K_RETURN:
                    reset()

def reset():
    global player, score, movementMul, jumpTime, jumpCD, bgm
    enemies.clear()
    lasers.clear()
    player = PlayerShip(200, height/2)
    score = 0
    movementMul = 1
    jumpTime = 1
    jumpCD = 0
    timeParticles.particles.clear()
    for explosion in explosions:
        explosion.particles.clear()
    pg.mixer.stop()
    player.flySound.play(-1)
    bgm = bgMusic.play(-1)
    bgm.set_volume(0.5)

startTime = pg.time.get_ticks()
while True:
    endTime = startTime + 1
    startTime = pg.time.get_ticks()
    dt = (startTime - endTime) / 1000
    pg.display.set_caption(f'Spacetime Breaker - FPS : {round(1/dt, 2)}')
    handle_events()
    if gameIsRunning:
        main_loop()
    elif player.lives > 0:
        startScreen()
    draw_interface()
    pg.display.update()
    pg.time.Clock().tick(75)