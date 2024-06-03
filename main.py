from pgzero.builtins import *
import pgzrun
from pgzhelper import *
import sys
import os

from level_design import ActorContainer
from camera import Camera

# assert sys.version_info <= (3, 10)

os.environ['SDL_VIDEO_CENTERED'] = '1' #Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ''

c = Camera()
c.initialize_camera(0, (640, 480))

def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    pass    

def update(dt):
    pass

def draw():
    screen.blit(c.return_camera_frame((WIDTH, HEIGHT)), (0, 0))

pgzrun.go()