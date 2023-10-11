import pygame as pg


class Being:
    __playerimage = ""

    def __init__(self, image):
        self.__playerimage = image

    def return_beingimage(self):
        return self.__playerimage


class Heroes(Being):
    __being_x, __being_y = 0, 0
    __bulletimage = pg.image.load("pinteres/bullet.png")

    def __init__(self, image, x, y):
        super().__init__(image)
        self.__being_x = x
        self.__being_y = y

    def return_bulletimage(self):
        return self.__bulletimage


class BasicAirplan(Heroes):
    HP = 100
    Attack = 20
    __bulletimage = ""


class Enemy(Being):

    def __init__(self, image):
        super().__init__(image)


class BasicEnemy(Enemy):
    HP = 20
    Attack = 10

