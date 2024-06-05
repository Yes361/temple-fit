from pgzero.builtins import *
import pgzrun
from pgzhelper import *
import sys
import os

from utils import Actor, ActorContainer
from managers import scene_manager, input_manager
from gui import Button, Menu
from camera import Camera
from entity import Player
from inventory import Item
from level_design import World

os.environ["SDL_VIDEO_CENTERED"] = "1"  # Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ""


def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    input_manager.on_key_down(key, unicode)

def update(dt):
    scene_manager.update(dt)
    input_manager.on_key_hold(dt)

def draw():
    scene_manager.clear()
    scene_manager.draw(Screen=screen)

pgzrun.go()
