import pgzrun
from pgzero.builtins import *
from pgzhelper import *
import pgzero
import os

from managers import scene_manager, input_manager, SceneManager
import Game

screen: pgzero.screen.Screen

os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 662
HEIGHT = 662
TITLE = "I wanna kms"
    
scene_manager.show_scene('Start Screen')
input_manager.set_group('Global')

def on_mouse_down(pos, button):
    input_manager.on_mouse_down(pos, button)

def on_key_down(key, unicode):
    input_manager.on_key_down(key, unicode)

def update(dt):
    scene_manager.update(dt)
    input_manager.on_key_hold(dt)
    input_manager.on_mouse_hover(pygame.mouse.get_pos())

def draw():    
    screen.clear()
    screen.fill((255, 255, 255))
    scene_manager.draw(screen)

pgzrun.go()