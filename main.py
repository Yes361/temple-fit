from pgzero.builtins import *
import pgzrun
from pgzhelper import *
import os

os.environ['SDL_VIDEO_CENTERED'] = '1' #Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ''

def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    pass    

def update(dt):
    pass

def draw():
    pass

pgzrun.go()