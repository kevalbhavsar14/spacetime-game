import pygame as pg

pg.init()

size = width, height = 800, 500
screen = pg.display.set_mode(size)

pg.display.set_icon(pg.image.load('data/sprites/icon.png').convert_alpha())

spawnEnemy = pg.USEREVENT + 1
pg.time.set_timer(spawnEnemy, 5000)

spawnLaser = pg.USEREVENT + 2
pg.time.set_timer(spawnLaser, 3000)

background = pg.image.load('data/sprites/background.png').convert()
ground = pg.image.load('data/sprites/ground.png').convert_alpha()

gameFont = pg.font.Font('data/font/CUFEL.otf', 30)
titleFont = pg.font.Font('data/font/CUFEL.otf', 50)

timeJumpIcon = pg.image.load('data/sprites/timeJumpIcon1.png').convert_alpha()
timeJumpIcon = pg.transform.rotozoom(timeJumpIcon, 0, 0.4)

timeJumpSound = pg.mixer.Sound('data/sounds/timeJump.wav')
timeJumpSound.set_volume(0.5)

lifeIcon = pg.image.load('data/sprites/lifeIcon1.png').convert_alpha()
lifeIcon = pg.transform.rotozoom(lifeIcon, 0, 0.4)

logo = pg.image.load('data/sprites/logo.png').convert_alpha()
crashText = titleFont.render('You crashed!', False, (255, 255, 0))
startText = gameFont.render('Press space to start', False, (255, 255, 255))
endText = gameFont.render('Press enter to return', False, (255, 255, 255))

bgMusic = pg.mixer.Sound('data/sounds/bgMusic.wav')