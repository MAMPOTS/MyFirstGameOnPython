from Screen import *

pg.font.init()
pg.init()
player = BasicAirplan(150, 300)

screengame = Screen(player)
pg.display.set_caption("MyFirstGameOnPython")

screengame.activgame()

screengame.Main()