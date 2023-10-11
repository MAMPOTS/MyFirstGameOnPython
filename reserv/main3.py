import pygame as pg
import pygame.draw
import random

from Being import *
from Screen import *

pg.font.init()
pg.init()


def activgame():
    global Money
    move()
    outalien()
    shot()
    activ_screen()
    flevel()


def move():
    global player, pause, lvl
    keys = pg.key.get_pressed()
    if keys[pg.K_UP] and player.y > 0:
        player.y -= player.Speed
    if keys[pg.K_DOWN] and player.y < 650:
        player.y += player.Speed
    if keys[pg.K_LEFT] and player .x > 0:
        player.x -= player.Speed
    if keys[pg.K_RIGHT] and player.x < 1100:
        player.x += player.Speed
    if keys[pg.K_p]:
        pause = True


def outalien():
    global alien_list_in_game, gameplay, player, Money
    if alien_list_in_game:
        for (i, el) in enumerate(alien_list_in_game):
            screen.blit(el.return_beingimage(), (el.x, el.y))
            el.move()
            if isinstance(el, ExtraEnemy):
                if el.y + 20 > player.y > el.y - 20 and len(el.bullets) == 0 and el.x - 350 > player.x:
                    el.bullets.append(el.return_bulletimage().get_rect(topleft=(el.x + 30, el.y + 22)))
                if el.bullets:
                    for (i, bul) in enumerate(el.bullets):
                        screen.blit(el.return_bulletimage(), (bul.x, bul.y))
                        bul.x -= 10
                        if bul.x < -50:
                            el.bullets.pop(i)
                        if player.return_rect().colliderect(bul):
                            player.HP -= el.BulletAttack
                            el.bullets.pop(i)
                            if player.HP <= 0:
                                gameplay = False
            if el.x < - 10:
                alien_list_in_game.pop(i)
            if player.return_rect().colliderect(el.return_rect()):
                player.HP -= el.Attack
                boom_effect(el.return_rect())
                alien_list_in_game.pop(i)
                Money += el.Pmoney
                if player.HP <= 0:
                    gameplay = False


def shot():
    global bullets, player, alien_list_in_game, Money
    if player.bullets:
        for (i, el) in enumerate(player.bullets):
            screen.blit(player.return_bulletimage(), (el.x, el.y))
            el.x += 4
            if el.x > 1250:
                player.bullets.pop(i)

            if alien_list_in_game:
                for (index, alien_el) in enumerate(alien_list_in_game):
                    if el.colliderect(alien_el.return_rect()):
                        player.bullets.pop(i)
                        alien_el.HP -= player.Attack
                        if alien_el.HP <= 0:
                            boom_effect(alien_el.return_rect())
                            alien_list_in_game.pop(index)
                            Money += alien_el.Pmoney


def activ_screen():
    global bg_x
    bg_x -= 2
    if bg_x == -1280:
        bg_x = 0

    HP_label = label.render(f"HP:{player.HP}", True, (200, 200, 200))
    money_label = label.render(f"Money:{Money}", True, (200, 200, 200))
    lvl_label = label.render(f"lvl: {lvl}", True, (200, 200, 200))

    screen.blit(HP_label, (30, 600))
    screen.blit(money_label, (950, 50))
    screen.blit(lvl_label, (500, 50))


def flevel():
    global time_counter, lvl
    if time_counter == 0:
        if lvl == 1:
            lvl = 2
            time_counter = 90
        elif lvl == 2:
            lvl = 3
            time_counter = 120


def boom_effect(coord):
    explosion = Explosion(coord.center[0], coord.center[1])
    explosion_group.add(explosion)


def fpause():
    global gameplay, pause, player
    keys = pg.key.get_pressed()
    screen.fill((255,255,255))
    if keys[pg.K_RETURN]:
        pause = False
    elif keys[pg.K_SPACE] and not(isinstance(player, ProAirplan)):
        player = ProAirplan(player.x, player.y)


def restart():
    global alien_list_in_game, player, bullets_left, Money, bg_x, gameplay, time_counter, lose_label, restart_label, lvl, game_menu
    screen.fill((87, 100, 100))
    screen.blit(lose_label, (500, 180))
    screen.blit(restart_label, (250, 400))
    keys = pg.key.get_pressed()
    if keys[pg.K_RETURN]:
        alien_list_in_game.clear()
        player.bullets.clear()
        player = BasicAirplan(150, 300)
        player.HP = 100
        time_counter = 60
        bullets_left = 5
        Money = 0
        bg_x = 0
        lvl = 3
        game_menu = False
        gameplay = True


def Mgame():
    global gameplay, game_menu, menu, numbermenu
    keys = pg.key.get_pressed()
    if keys[pg.K_DOWN]:
        if numbermenu != 2:
            numbermenu += 1
    elif keys[pg.K_UP] and pg.KEYUP:
        if numbermenu != 1:
            numbermenu -= 1
    elif keys[pg.K_RETURN]:
        restart()
    if numbermenu == 1:
        screen.blit(pg.image.load("pinteres/menu/menu_NG.png"), (0, 0))
    else:
        screen.blit(pg.image.load("pinteres/menu/menu_S.png"), (0, 0))


screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("MyFirstGameOnPython")

pg.display.update()
clock = pg.time.Clock()

FPS = 120
lvl = 1
numbermenu = 1
Money = 0
bg_x = 0

alien_list_in_game = []

alien_timer = pg.USEREVENT + 1
pg.time.set_timer(alien_timer, 1500)

time_counter = 60
pg.time.set_timer(pg.USEREVENT + 2, 1000)


label = pg.font.Font("shrift/Mfont.ttf", 60)
lose_label = label.render("You Lose!", False, (193, 196, 199))
restart_label = label.render("Restart game, press Enter", False, (100, 255, 100))

pg.display.set_icon(pg.image.load("pinteres/ikon.png").convert_alpha())
zadnik = pg.image.load("pinteres/Zadnik.jpg").convert()

player = BasicAirplan(150, 300)
explosion_group = pg.sprite.Group()

running = True
game_menu = True
gameplay = False
pause = False

while running:
    screen.blit(zadnik, (bg_x, 0))
    screen.blit(zadnik, (bg_x + 1280, 0))
    screen.blit(player.return_beingimage(), (player.x, player.y))

    screen.blit(pygame.font.SysFont('Consolas', 30).render(str(time_counter).rjust(3), True, (0, 0, 0)), (32, 48))
    explosion_group.draw(screen)
    explosion_group.update()

    if game_menu:
        Mgame()

    elif gameplay and pause:
        fpause()

    elif gameplay:
        activgame()

    else:
        restart()

    pg.display.update()
    for event in pg.event.get():
        print(pg.USEREVENT)
        if event.type == pg.QUIT:
            running = False

        if event.type == alien_timer and (not(pause)):
            enemy_rand = 1
            if lvl == 2:
                enemy_rand = int(random.uniform(1, 3))
            if lvl == 3:
                enemy_rand = int(random.uniform(1, 4))
            if enemy_rand == 1: alien_list_in_game.append(BasicEnemy(1300, random.uniform(20, 690)))
            if enemy_rand == 2: alien_list_in_game.append(ProEnemy(1300, random.uniform(20, 690)))
            if enemy_rand == 3: alien_list_in_game.append(ExtraEnemy(1300, random.uniform(20, 690)))

        if gameplay and event.type == pg.KEYUP and event.key == pg.K_SPACE:
            player.bullets.append(player.return_bulletimage().get_rect(topleft=(player.x + 30, player.y + 10)))

        if event.type == pg.USEREVENT + 2 and (not(pause)):
            time_counter -= 1
            text = str(time_counter).rjust(3) if time_counter > 0 else 'End'

        if event.type == pygame.QUIT:
            run = False

    clock.tick(FPS)