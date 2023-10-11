import pygame as pg
import random

pg.font.init()
pg.init()


class Being:
    _playerimage = [pg.image.load("pinteres/ikon.png")]
    imageactiv = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def return_beingimage(self):
        if self.imageactiv != len(self._playerimage) - 1:
            self.imageactiv += 1
        else:
            self.imageactiv = 0
        return self._playerimage[self.imageactiv]

    def return_rect(self):
        return self._playerimage[0].get_rect(topleft=(self.x, self.y))


class Heroes(Being):
    _bulletimage = ""
    bullets = []
    Speed = 15

    def return_bulletimage(self):
        return self._bulletimage


class BasicAirplan(Heroes):
    HP = 100
    Attack = 10
    Speed = 10
    player_anim = 1
    ActivHP = HP

    bullets = []
    _bulletimage = pg.image.load("pinteres/Airplane/bullet.png")

    _playerimage = []
    playerimageUP = pg.image.load("pinteres/Airplane/BasicAirplaneDOWN.png")
    playerimageDOWN = pg.image.load("pinteres/Airplane/BasicAirplaneUP.png")

    for i in range(1,  4):
        _playerimage.append(pg.image.load(f"pinteres/Airplane/BasicAirplaneRight{i}.png"))

    def return_bulletimage(self):
        return self._bulletimage

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.y > 0:
            self.y -= self.Speed
            self.player_anim = 2
        elif keys[pg.K_DOWN] and self.y < 650:
            self.y += self.Speed
            self.player_anim = 3
        else:
            self.player_anim = 1
        if keys[pg.K_LEFT] and self.x > 0:
            self.x -= self.Speed
        if keys[pg.K_RIGHT] and self.x < 1100:
            self.x += self.Speed


class BasicEnemy(Being):
    _playerimage = []
    HP = 20
    Attack = 25
    Pmoney = 5

    for i in range(1,  11):
        _playerimage.append(pg.image.load(f"pinteres/Alien/BasicAlien/BasicAlien{i}.png"))

    def move(self):
        self.x -= 5


class ProEnemy(Being):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.Npredel = self.y + 50
        self.Vpredel = self.y - 50
        self.Flag = True

    _playerimage = []
    HP = 35
    Attack = 60
    Pmoney = 15

    for i in range(1,  9):
        _playerimage.append(pg.image.load(f"pinteres/Alien/ProAlien/ProAlien{i}.png"))

    def move(self):
        self.x -= 5
        if self.y > self.Npredel and self.Flag == True: self.Flag = False
        if self.y < self.Vpredel and self.Flag == False: self.Flag = True
        if self.Flag: self.y += 1
        else: self.y -= 1


class ExtraEnemy(Being):
    _playerimage = []
    _bulletimage = []
    _bulletactiv = 0
    HP = 65
    Attack = 50
    BulletAttack = 20
    Pmoney = 30

    bullets = []
    for i in range(1,  10):
        _playerimage.append(pg.image.load(f"pinteres/Alien/ExtraAlien/ExtraAlien{i}.png"))

    for i in range(1, 4):
        _bulletimage.append(pg.image.load(f"pinteres/Alien/ExtraAlien/bullet/AlienBullet{i}.png"))


    def move(self):
        self.x -= 5

    def return_bulletimage(self):
        if self._bulletactiv != len(self._bulletimage) - 1:
            self._bulletactiv += 1
        else:
            self._bulletactiv = 0
        return self._bulletimage[self._bulletactiv]

    def return_bulletrect(self):
        return self._bulletimage[0].get_rect()

    def shot_el(self, player, screen):
        if self.y + 30 > player.y > self.y - 30 and len(self.bullets) == 0 and self.x - 350 > player.x:
            self.bullets.append(self.return_bulletimage().get_rect(topleft=(self.x - 5, self.y + 47)))
        if self.bullets:
            for (i, bul) in enumerate(self.bullets):
                screen.blit(self.return_bulletimage(), (bul.x, bul.y))
                bul.x -= 7
                if bul.x < -50:
                    self.bullets.pop(i)
                if player.return_rect().colliderect(bul):
                    player.ActivHP -= self.BulletAttack
                    self.bullets.pop(i)

class BasicBoss(Being):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.Flag = True

    _playerimage = []
    _bulletimage = []

    HP = 50
    Attack = 50
    BulletAttack = 50
    Pmoney = 250
    y = 100

    BossActiv = False
    AttackActiv = 0
    _bulletactiv = 0
    pg.time.set_timer(pg.USEREVENT + 10, 6000)

    for i in range(1, 10):
        _playerimage.append(pg.image.load(f"pinteres/Alien/Boss/BasicBoss{i}.png"))

    bullets = []
    for i in range(1, 4):
        _bulletimage.append(pg.image.load(f"pinteres/Alien/ExtraAlien/bullet/AlienBullet{i}.png"))

    def shot_el(self, player, screen):
        if self.y + 30 > player.y > self.y - 30 and len(self.bullets) == 0 and self.x - 350 > player.x:
            self.bullets.append(self.return_bulletimage().get_rect(topleft=(self.x - 5, self.y + 47)))
        if self.bullets:
            for (i, bul) in enumerate(self.bullets):
                screen.blit(self.return_bulletimage(), (bul.x, bul.y))
                bul.x -= 7
                if bul.x < -50:
                    self.bullets.pop(i)
                if player.return_rect().colliderect(bul):
                    player.ActivHP -= self.BulletAttack
                    self.bullets.pop(i)

    def return_bulletimage(self):
        if self._bulletactiv != len(self._bulletimage) - 1:
            self._bulletactiv += 1
        else:
            self._bulletactiv = 0
        return self._bulletimage[self._bulletactiv]

    def move(self, alien_list_in_game):
        if self.AttackActiv == 1:
            self.x -= 20
            if self.x <= 0:
                self.AttackActiv = 0
        elif self.AttackActiv == 2:
            for i in range(3):
                alien_list_in_game.append(ExtraEnemy(1300, random.uniform(20, 690)))
            self.AttackActiv = 0
        else:
            if self.x < 1100:
                self.x += 10
        if self.y > 690 and self.Flag == True: self.Flag = False
        if self.y < 10 and self.Flag == False: self.Flag = True
        if self.Flag:
            self.y += 5
        else:
            self.y -= 5