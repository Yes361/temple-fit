from pgzero.builtins import *
import pgzrun
from pgzhelper import *
import sys
import os

from level_design import Level
from camera import Camera

# assert sys.version_info <= (3, 10)

os.environ['SDL_VIDEO_CENTERED'] = '1' #Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ''

l = Level()
# c = Camera()
l.place_block(Actor('enemyblack1', pos=(100, 100)))
l.save_file('level.csv')
# l.read_file('level.csv')
# c.initialize_camera(0)

def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    pass    

def update(dt):
    pass

def draw():
    # screen.blit(c.return_camera_frame(WIDTH, HEIGHT), (0, 0))
    l.draw()
    pass

pgzrun.go()