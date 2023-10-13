import pygame as pg
import pygame.draw
import random

from Being import *

pg.font.init()
pg.init()


class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 9):
            img = pg.image.load(f"pinteres/boomeff/boom_{num}.png")
            img = pg.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 5
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


class Screen():
    def __init__(self, player):
        self.player = player

    screen = pg.display.set_mode((1280, 720))

    pg.display.update()
    clock = pg.time.Clock()

    FPS = 75
    lvl = 1
    numbermenu = 1
    player_anim = 1
    bg_x = 0
    Money = 0

    price = {"Attack": 150, "HP": 150, "Health": 50}
    alien_list_in_game = []

    pygame.mixer.Channel(0).play(pygame.mixer.Sound("music/soundtrekforfriends/ASKORBINKA.mp3"))

    running = True
    gamemenu = True
    gameplay = False
    pause = False
    win = False

    pg.display.set_icon(pg.image.load("pinteres/ikon.png").convert_alpha())
    pause_menu = pg.image.load("pinteres/menu/pause_menu.png").convert_alpha()
    restart_menu = pg.image.load("pinteres/menu/restartmenu.png").convert_alpha()
    zadnik = pg.image.load("pinteres/Zadnik.jpg").convert()
    winpic = pg.image.load("pinteres/menu/winmenu.jpg").convert()

    BBoss = BasicBoss(1100, 0)
    explosion_group = pg.sprite.Group()

    STOPPED_PLAYING = pygame.USEREVENT + 20
    pygame.mixer.music.set_endevent(STOPPED_PLAYING)

    time_counter = 60
    pg.time.set_timer(pg.USEREVENT + 2, 1000)

    alien_timer = pg.USEREVENT + 1
    pg.time.set_timer(alien_timer, 1500)

    small_label = pg.font.Font("shrift/Mfont.ttf", 30)
    label = pg.font.Font("shrift/Mfont.ttf", 60)

    def activgame(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_p]:
            self.pause = True
        self.player.move()
        self.outalien()
        self.shot()
        self.activ_screen()

    def alien_add(self, enemy):
        self.alien_list_in_game.append(enemy)

    def outalien(self):
        if self.alien_list_in_game:
            for (i, el) in enumerate(self.alien_list_in_game):
                self.screen.blit(el.return_beingimage(), (el.x, el.y))
                if isinstance(el, BasicBoss):
                    el.move(self.alien_list_in_game)
                else:
                    el.move()
                if isinstance(el, ExtraEnemy) or isinstance(el, BasicBoss):
                    el.shot_el(self.player, self.screen)
                if el.x < - 10:
                    self.alien_list_in_game.pop(i)
                    self.player.ActivHP -= 20
                if self.player.return_rect().colliderect(el.return_rect()):
                    self.player.ActivHP -= el.Attack
                    if not isinstance(el, BasicBoss):
                        self.boom_effect(el.return_rect())
                        self.alien_list_in_game.pop(i)
                    else:
                        el.x = 1100
                    self.Money += el.Pmoney
                if self.player.ActivHP <= 0:
                    self.gameplay = False

    def shot(self):
        if self.player.bullets:
            for (i, el) in enumerate(self.player.bullets):
                self.screen.blit(self.player.return_bulletimage(), (el.x + 70, el.y + 5))
                el.x += 4
                if el.x > 1250:
                    self.player.bullets.pop(i)

                if self.alien_list_in_game:
                    for (index, alien_el) in enumerate(self.alien_list_in_game):
                        if el.colliderect(alien_el.return_rect()):
                            self.player.bullets.pop(i)
                            alien_el.HP -= self.player.Attack
                            if alien_el.HP <= 0:
                                self.boom_effect(alien_el.return_rect())
                                self.alien_list_in_game.pop(index)
                                self.Money += alien_el.Pmoney

    def activ_screen(self):
        self.bg_x -= 2
        if self.bg_x == -1280:
            self.bg_x = 0


        if self.BBoss.HP <= 0:
            self.BBoss.AttackActiv = False
            self.win = True
            self.Mwin()


        if self.time_counter <= 0:
            if self.lvl == 0:
                self.lvl = 1
                self.time_counter = 60
            elif self.lvl == 1:
                self.lvl = 2
                self.time_counter = 90
            elif self.lvl == 2:
                self.lvl = 3
                self.time_counter = 120
            elif self.lvl == 3 and self.BBoss.BossActiv == False and self.BBoss.HP > 0:
                self.time_counter = 100000
                self.BBoss.BossActiv = True


        HP_label = self.label.render(f"HP:{self.player.ActivHP}", True, (200, 200, 200))
        money_label = self.label.render(f"Money:{self.Money}", True, (200, 200, 200))
        lvl_label = self.label.render(f"lvl: {self.lvl}", True, (200, 200, 200))

        if self.win == False:
            self.screen.blit(HP_label, (30, 600))

        if self.BBoss.BossActiv == False and self.win == False:
            self.screen.blit(lvl_label, (500, 50))
            self.screen.blit(money_label, (950, 50))
            self.screen.blit(pygame.font.SysFont('Consolas', 30).render(str(self.time_counter).rjust(3), True, (0, 0, 0)), (32, 48))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (400, 20, self.BBoss.HP, 50))

    def boom_effect(self, coord):
        explosion = Explosion(coord.center[0], coord.center[1])
        self.explosion_group.add(explosion)

    def fpause(self):
        self.screen.blit(self.pause_menu, (0, 0))
        self.screen.blit(self.label.render(f"Money:{self.Money}", True, (200, 200, 200)), (950, 50))
        self.screen.blit(self.small_label.render(f"price: {self.price['Attack']}", True, (255, 150, 150)), (215, 400))
        self.screen.blit(self.small_label.render(f"price: {self.price['HP']}", True, (255, 150, 150)), (580, 400))
        self.screen.blit(self.small_label.render(f"price: {self.price['Health']}", True, (255, 150, 150)), (940, 400))
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    self.pause = False
                if event.key == pg.K_ESCAPE:
                    self.gameplay = False
                    self.gamemenu = True
                if event.type == pg.KEYUP and event.key == pg.K_1:
                    if self.Money - self.price["Attack"] >= 0:
                        self.Money -= self.price["Attack"]
                        self.price["Attack"] += self.price["Attack"]
                        self.player.Attack += 20
                if event.type == pg.KEYUP and event.key == pg.K_2:
                    if self.Money - self. price["HP"] >= 0:
                        self.Money -= self.price["HP"]
                        self.price["HP"] += self.price["HP"]
                        self.player.HP += 20
                        self.player.ActivHP = self.player.HP
                if event.type == pg.KEYUP and event.key == pg.K_3:
                    if self.Money - self.price["Health"] >= 0:
                        self.Money -= self.price["Health"]
                        self.price["Health"] += 30
                        self.player.ActivHP = self.player.HP

            if event.type == pg.QUIT:
                self.running = False

    def restart(self):
        self.screen.blit(self.restart_menu, (0, 0))
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN] or self.gamemenu:
            self.alien_list_in_game.clear()
            self.player.bullets.clear()
            self.player = BasicAirplan(150, 300)
            self.BBoss = BasicBoss(1100, 0)
            self.player.ActivHP = self.player.HP = 100
            self.time_counter = 0
            self.bullets_left = 5
            self.lvl = 0
            self.Money = 0
            self.bg_x = 0
            self.price = {"Attack": 150, "HP": 150, "Health": 50}
            self.gamemenu = False
            self.gameplay = True
            self.soundtrek = ""

    def Mgame(self):
        self.screen.blit(pg.image.load("pinteres/menu/startmenu.png"), (0, 0))

        for event in pg.event.get():
            if event.type == pg.KEYUP and event.key == pg.K_RETURN:
                self.restart()
            if (event.type == pg.KEYUP and event.key == pg.K_ESCAPE) or event.type == pg.QUIT:
                self.running = False

    def Mwin(self):
        self.screen.blit(self.winpic, (0, 0))
        self.screen.blit(self.label.render("Again?", True, (0, 0, 0)), (550, 650))
        self.gameplay = False
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN] or self.gamemenu:
            self.restart()

    def Main(self):
        while self.running:
            self.screen.blit(self.zadnik, (self.bg_x, 0))
            self.screen.blit(self.zadnik, (self.bg_x + 1280, 0))
            if self.player.player_anim == 1:
                self.screen.blit(self.player.return_beingimage(), (self.player.x, self.player.y))
            elif self.player.player_anim == 2:
                self.screen.blit(self.player.playerimageUP, (self.player.x, self.player.y))
            elif self.player.player_anim == 3:
                self.screen.blit(self.player.playerimageDOWN, (self.player.x, self.player.y))


            self.explosion_group.draw(self.screen)
            self.explosion_group.update()

            if self.gamemenu:
                self.Mgame()

            elif self.gameplay and self.pause:
                self.fpause()

            elif self.gameplay:
                self.activgame()
                if self.time_counter <= -1:
                    self.gameplay = False
                    self.gamemenu = False
                    self.win = True
            elif self.win:
                self.Mwin()
            else:
                self.gamemenu = True

            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if pygame.mixer.Channel(0).get_busy() == False:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("music/soundtrekforfriends/IMRUSSIAN.mp3"))

                if event.type == self.alien_timer and (not (self.pause)):
                    if self.BBoss.BossActiv and self.BBoss.HP > 0:
                        if len(self.alien_list_in_game) == 0:
                            self.alien_list_in_game.append(self.BBoss)
                    else:
                        self.BBoss.BossActiv = False
                        if self.lvl == 1:
                            enemy_rand = int(random.uniform(1, 2))
                        if self.lvl == 2:
                            enemy_rand = int(random.uniform(1, 3))
                        if self.lvl == 3:
                            enemy_rand = int(random.uniform(1, 4))
                        if enemy_rand == 1: self.alien_list_in_game.append(BasicEnemy(1300, random.uniform(20, 690)))
                        if enemy_rand == 2: self.alien_list_in_game.append(ProEnemy(1300, random.uniform(20, 690)))
                        if enemy_rand == 3: self.alien_list_in_game.append(ExtraEnemy(1300, random.uniform(20, 690)))

                if self.gameplay and event.type == pg.KEYUP and event.key == pg.K_SPACE and len(self.player.bullets) <= 4:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("music/bulletmusic/16557_1460656892.mp3"))
                    self.player.bullets.append(self.player.return_bulletimage().get_rect(topleft=(self.player.x + 30, self.player.y + 10)))

                if event.type == pg.USEREVENT + 2 and (not (self.pause)):
                    self.time_counter -= 1
                    self.text = str(self.time_counter).rjust(3) if self.time_counter > 0 else 'End'

                if event.type == pg.USEREVENT + 10:
                    self.BBoss.AttackActiv = int(random.uniform(1, 3))

            self.clock.tick(self.FPS)