from pgzero.builtins import *
import pgzrun
from pgzhelper import *
from actor import Actor
import sys
import os

from gui import SceneManager, button
from level_design import ActorContainer
from camera import Camera
from keyboard import keyManager

# assert sys.version_info <= (3, 10)

os.environ['SDL_VIDEO_CENTERED'] = '1' #Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ''

c = Camera()
c.initialize_camera(0, (640, 480))

scene = SceneManager()
scene.add_scene('cam', None, lambda: screen.blit(c.draw((WIDTH - 100, HEIGHT - 100)), (50, 50)))
scene.set_scene('cam')

def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    pass

def update(dt):
    scene.update(dt)

def draw():
    screen.clear()
    scene.draw()

pgzrun.go()