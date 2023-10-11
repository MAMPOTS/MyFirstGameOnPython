import pygame as pg
import pygame.draw
import random

from Being import *
import sys

pg.font.init()


def activgame():
    global Money
    move()
    outalien()
    shot()


def fpause():
    global gameplay, pause
    keys = pg.key.get_pressed()
    screen.fill((255,255,255))
    if keys[pg.K_RETURN]:
        pause = False


def restart():
    global alien_list_in_game, bullets, player, bullets_left, Money, bg_x, gameplay
    alien_list_in_game.clear()
    bullets.clear()
    player.x, player.y = 150, 150
    bullets_left = 5
    player.HP = 100
    Money = 0
    bg_x = 0
    gameplay = True


def move():
    global player, pause
    keys = pg.key.get_pressed()
    if keys[pg.K_UP] and player.y > 0:
        player.y -= player.Speed
    if keys[pg.K_DOWN] and player.y < 650:
        player.y += player.Speed
    if keys[pg.K_LEFT] and player.x > 0:
        player.x -= player.Speed
    if keys[pg.K_RIGHT] and player.x < 1100:
        player.x += player.Speed
    if keys[pg.K_p]:
        pause = True


def shot():
    global bullets, player, alien_list_in_game, Money
    if bullets:
        for (i, el) in enumerate(bullets):
            screen.blit(player.return_bulletimage(), (el.x, el.y))
            el.x += 4

            if el.x > 1250:
                bullets.pop(i)

            if alien_list_in_game:
                for (index, alien_el) in enumerate(alien_list_in_game):
                    if el.colliderect(alien_el.return_rect()):
                        alien_el.HP -= player.Attack
                        bullets.pop(i)
                        if alien_el.HP <= 0:
                            alien_list_in_game.pop(index)
                            Money += alien_el.Pmoney


def outalien():
    global alien_list_in_game, gameplay, player, Money
    if alien_list_in_game:
        for (i, el) in enumerate(alien_list_in_game):
            screen.blit(alien.return_beingimage(), (el.x, el.y))
            el.x -= 6
            if el.x < - 10:
                alien_list_in_game.pop(i)
            if player_rect.colliderect(el.return_rect()):
                player.HP -= el.Attack
                alien_list_in_game.pop(i)
                Money += el.Pmoney
                if player.HP <= 0:
                    gameplay = False


screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("MyFirstGameOnPython")


pg.display.update()
clock = pg.time.Clock()

FPS = 120
Money = 0
bg_x = 0

alien_list_in_game = []
bullets = []

alien_timer = pg.USEREVENT + 1
pg.time.set_timer(alien_timer, 1500)

label = pg.font.Font("shrift/Mfont.ttf", 60)
lose_label = label.render("You Lose!", False, (193, 196, 199))
restart_label = label.render("Restart game, press Enter", False, (100, 255, 100))

pg.display.set_icon(pg.image.load("pinteres/ikon.png").convert_alpha())
zadniy_fon = pg.image.load("pinteres/Zadnik.jpg").convert()
player = BasicAirplan(150, 300)

running = True
gameplay = True
pause = False

while running:
    screen.blit(zadniy_fon, (bg_x, 0))
    screen.blit(zadniy_fon, (bg_x + 1280, 0))
    screen.blit(player.return_beingimage(), (player.x, player.y))

    bg_x -= 2
    if bg_x == -1280:
        bg_x = 0
    if gameplay and pause:
        fpause()
    elif gameplay:

        player_rect = player.return_beingimage().get_rect(topleft=(player.x, player.y))

        money_label = label.render(f"Money:{Money}", True, (200, 200, 200))
        screen.blit(money_label, (950, 50))
        activgame()
    else:
        screen.fill((87, 100, 100))
        screen.blit(lose_label, (500, 180))
        screen.blit(restart_label, (250, 400))
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            restart()

    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == alien_timer:
            alien = BasicEnemy(1300, random.uniform(20, 700))
            alien_list_in_game.append(alien)
        if gameplay and event.type == pg.KEYUP and event.key == pg.K_SPACE:
            bullets.append(player.return_bulletimage().get_rect(topleft=(player.x + 30, player.y + 10)))

    clock.tick(FPS)