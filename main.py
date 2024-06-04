from pgzero.builtins import *
import pgzrun
from pgzhelper import *
from actor import Actor
import sys
import os

from gui import SceneManager, button
from level_design import ActorContainer
from camera import Camera

# assert sys.version_info <= (3, 10)

os.environ['SDL_VIDEO_CENTERED'] = '1' #Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ''

c = Camera()
c.initialize_camera(0, (640, 480))

scene = SceneManager()

def cam():
    screen.blit(c.return_camera_frame((WIDTH - 100, HEIGHT - 100)), (50, 50))
    
def witch():
    scene.switch_scene('cam1')

scene.add_scene('cam', None, cam, ActorContainer([button('dragon_1.png', pos=(100, 100), callback=witch)]))
scene.add_scene('cam1', None, None, ActorContainer([Actor('dragon_2.png', pos=(300, 300))]))

scene.set_scene('cam')

def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    scene.switch_scene('cam1')

def update(dt):
    scene.update(dt)

def draw():
    screen.clear()
    scene.draw()

pgzrun.go()