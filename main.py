from pgzero.builtins import *
import pgzrun
from pgzhelper import *
import sys
import os

from utils import Actor, ActorContainer
from managers import scene_manager, input_manager
from gui import Button, Menu, Item
from camera import Camera
from entity import Player, Collisions
from level_design import World
from constants import Constants

os.environ["SDL_VIDEO_CENTERED"] = "1"  # Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ""

scene_manager.subscribe('b', None, None, ActorContainer([a := Actor('dragon_1.png', pos=(300, 300)), b := Actor('dragon_1.png', pos=(300, 300))]))
scene_manager.subscribe('a', None, None, ActorContainer([Item('dragon_2.png', slot_image='dragon_3.png', pos=(300, 300), dims=None)]))

scene_manager.show_scene('b')

input_manager.subscribe(Constants.KEY_DOWN, lambda x, y: print(x, y), 'Global')

# but.Bind(input_manager, 'global')
# but.Release()

def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    input_manager.on_key_down(key, unicode)

def update(dt):
    scene_manager.update(dt)
    input_manager.on_key_hold(dt)
    input_manager.on_mouse_hover(pygame.mouse.get_pos())
    
    a.pos = pygame.mouse.get_pos()
    Collisions.resolve(a, b)

def draw():
    screen.clear()
    scene_manager.draw(Screen=screen)

pgzrun.go()
