import pygame as pg
import pygame.draw
import random

from Being import *
import sys

pg.font.init()


def activgame():
    move()
    outalien()
    shot()


def move():
    global player_y, player_x
    keys = pg.key.get_pressed()
    if keys[pg.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pg.K_DOWN] and player_y < 650:
        player_y += player_speed
    if keys[pg.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pg.K_RIGHT] and player_x < 1100:
        player_x += player_speed


def shot():
    global bullets, player, alien_list_in_game
    if bullets:
        for (i, el) in enumerate(bullets):
            screen.blit(player.return_bulletimage(), (el.x, el.y))
            el.x += 4

            if el.x > 1250:
                bullets.pop(i)

            if alien_list_in_game:
                for (index, alien_el) in enumerate(alien_list_in_game):
                    if el.colliderect(alien_el):
                        alien_list_in_game.pop(index)
                        bullets.pop(i)


def outalien():
    global alien_list_in_game, gameplay, alien
    if alien_list_in_game:
        for (i, el) in enumerate(alien_list_in_game):
            screen.blit(alien.return_beingimage(), el)
            el.x -= 6

            if el.x < - 10:
                alien_list_in_game.pop(i)

            if player_rect.colliderect(el):
                gameplay = False


screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("MyFirstGameOnPython")


pg.display.update()
clock = pg.time.Clock()

FPS = 120
player_speed = 15
player_y = 150
player_x = 150
bg_x = 0

alien_list_in_game = []
bullets = []

alien_timer = pg.USEREVENT + 1
pg.time.set_timer(alien_timer, 500)

label = pg.font.Font("shrift/Mfont.ttf", 60)
lose_label = label.render("You Lose!", False, (193, 196, 199))
restart_label = label.render("Restart game, press Enter", False, (100, 255, 100))

pg.display.set_icon(pg.image.load("pinteres/ikon.png").convert_alpha())
zadniy_fon = pg.image.load("pinteres/Zadnik.jpg").convert()
player = BasicAirplan(pg.image.load("pinteres/HeroesRight.png").convert_alpha(), 150, 150)
alien = Enemy(pg.image.load("pinteres/ufo.png").convert_alpha())

running = True
gameplay = True

while running:
    screen.blit(zadniy_fon, (bg_x, 0))
    screen.blit(zadniy_fon, (bg_x + 1280, 0))
    screen.blit(player.return_beingimage(), (player_x, player_y))

    bg_x -= 2
    if bg_x == -1280:
        bg_x = 0

    if gameplay:

        player_rect = player.return_beingimage().get_rect(topleft=(player_x, player_y))

        activgame()
    else:
        screen.fill((87, 100, 100))
        screen.blit(lose_label, (500, 180))
        screen.blit(restart_label, (250, 400))

        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            alien_list_in_game.clear()
            bullets.clear()
            player_x, player_y = 150, 150
            bullets_left = 5
            gameplay = True

    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == alien_timer:
            alien_list_in_game.append(alien.return_beingimage().get_rect(topleft=(1300, random.uniform(0, 715))))
        if gameplay and event.type == pg.KEYUP and event.key == pg.K_SPACE:
            bullets.append(player.return_bulletimage().get_rect(topleft=(player_x + 30, player_y + 10)))

    clock.tick(FPS)