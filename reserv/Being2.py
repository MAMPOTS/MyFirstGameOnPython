import pygame as pg
pg.init()


class Being:
    __playerimage = pg.image.load("pinteres/ikon.png")
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def return_beingimage(self):
        return self.__playerimage


class Heroes(Being):
    __bulletimage = ""

    def __init__(self, x, y):
        super().__init__(x, y)

    def return_bulletimage(self):
        return self.__bulletimage


class BasicAirplan(Heroes):
    HP = 100
    Attack = 10
    Speed = 15
    __playerimage = pg.image.load("pinteres/HeroesRight.png")
    __bulletimage = pg.image.load("pinteres/bullet.png")

    def return_bulletimage(self):
        return self.__bulletimage

    def return_rect(self):
        return self.__playerimage.get_rect(topleft=(self.x, self.y))

    def return_beingimage(self):
        return self.__playerimage


class ProAirplan(Heroes):
    HP = 250
    Attack = 30
    speed = 15
    __bulletimage = pg.image.load("pinteres/bullet.png")

    def return_bulletimage(self):
        return self.__bulletimage

    def return_beingimage(self):
        return self.__playerimage


class Enemy(Being):
    def __init__(self, x, y):
        super().__init__(x, y)


class BasicEnemy(Enemy):
    __playerimage = pg.image.load("pinteres/ufo.png")
    HP = 20
    Attack = 25
    Pmoney = 10

    def return_rect(self):
        return self.__playerimage.get_rect(topleft=(self.x, self.y))

    def return_beingimage(self):
        return self.__playerimage

