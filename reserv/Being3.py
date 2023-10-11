import pygame as pg


class Being:
    _playerimage = pg.image.load("pinteres/ikon.png")
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def return_beingimage(self):
        return self._playerimage

    def return_rect(self):
        return self._playerimage.get_rect(topleft=(self.x, self.y))


class Heroes(Being):
    _bulletimage = ""
    bullets = []

    def return_bulletimage(self):
        return self._bulletimage

    def return_beingimage(self):
        return self._playerimage


class BasicAirplan(Heroes):
    HP = 100
    Attack = 10
    Speed = 15
    _playerimage = pg.image.load("pinteres/basicrocket.png")
    _bulletimage = pg.image.load("pinteres/bullet.png")


class ProAirplan(Heroes):
    HP = 250
    Attack = 30
    Speed = 15
    _bulletimage = pg.image.load("pinteres/bullet.png")
    _playerimage = pg.image.load("pinteres/prorocket.png")


class Enemy(Being):
    HP = 0
    Attack = 0
    Pmoney = 0


class BasicEnemy(Being):
    _playerimage = pg.image.load("pinteres/alien.png")
    HP = 20
    Attack = 25
    Pmoney = 10

    def move(self):
        self.x -= 5


class ProEnemy(Being):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.Npredel = self.y + 50
        self.Vpredel = self.y - 50
        self.Flag = True

    _playerimage = pg.image.load("pinteres/proalien.png")
    HP = 35
    Attack = 60
    Pmoney = 25

    def move(self):
        self.x -= 5
        if self.y > self.Npredel and self.Flag == True: self.Flag = False
        if self.y < self.Vpredel and self.Flag == False: self.Flag = True
        if self.Flag: self.y += 1
        else: self.y -= 1


class ExtraEnemy(Being):
    _playerimage = pg.image.load("pinteres/extraalien.png")
    _bulletimage = pg.image.load("pinteres/alienbullet.png")
    HP = 65
    Attack = 50
    BulletAttack = 20
    Pmoney = 10

    bullets = []


    def move(self):
        self.x -= 5

    def return_bulletimage(self):
        return self._bulletimage

    def return_bulletrect(self):
        return self._bulletimage.get_rect()


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    _bulletimage = pg.image.load("pinteres/alienbullet.png")
    BulletAttack = 20
    speedbullet = 0
    activbullet = False
    """
    def bulletmove(self, screen):
        if self.activbullet:
            screen.blit(self._bulletimage, (self.x, self.y))
            self.x -= self.speedbullet
            self.speedbullet += 5
            if self.x - self.speedbullet < 50:
                self.speedbullet = 0
                self.activbullet = False"""

    def return_bulletimage(self):
        return self._bulletimage

    def return_rect(self):
        return self._bulletimage.get_rect(topleft=(self.x, self.y))




