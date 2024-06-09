import pgzrun
import pgzero.screen
import pygame
import os

from managers import scene_manager, input_manager, SceneManager
import Scenes

screen: pgzero.screen.Screen
os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 662
HEIGHT = 662
TITLE = "I wanna kms"

def on_mouse_down(pos, button):
    input_manager.on_mouse_down(pos, ())
    print(button)

def on_key_down(key, unicode):
    input_manager.on_key_down(key, unicode)

def update(dt):
    scene_manager.update(dt)
    input_manager.on_key_hold(dt)
    input_manager.on_mouse_hover(pygame.mouse.get_pos())

def draw():    
    screen.clear()
    scene_manager.draw(screen)

pgzrun.go()