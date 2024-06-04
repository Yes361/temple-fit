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

b = button('enemyblack4', topleft=(500, 500))

asd = SceneManager()
asd.add_scene('b', ActorContainer([Actor('enemyblack1', pos=(100, 100), collision=True), Actor('enemyblack2', pos=(200, 200)), Actor('enemyblack3', pos=(300, 300))]), lambda: print(2))
asd.add_scene('a', ActorContainer([Actor('enemyblack3', pos=(100, 100)), Actor('enemyblack2', pos=(200, 200)), Actor('enemyblack1', pos=(300, 300))]), lambda: print(3))

def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    asd.set_scene(unicode)

def update(dt):
    b.update()

def draw():
    
    screen.blit(c.return_camera_frame((WIDTH, HEIGHT)), (0, 0))
    
    asd.draw_scenes()
    b.draw()
pgzrun.go()