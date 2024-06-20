import pgzrun
import pgzero.screen
import os

from managers import game_manager, GameManager
from Scenes import *
from Game import camera

screen: pgzero.screen.Screen
os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 662
HEIGHT = 662
TITLE = "I wanna kms"

camera.initialize_camera(0, (600, 450))

StartScreen()
Narrative()
hallway()
battle()
Outro()

game_manager.show_scene('Start Screen')

def on_mouse_down(pos, button):
    game_manager.on_mouse_down(pos, button)

def on_key_down(key, unicode):
    game_manager.on_key_down(key, unicode)

def on_mouse_up(pos, button):
    game_manager.on_mouse_up(pos, button)
    
def on_mouse_move(pos, rel, buttons):
    game_manager.on_mouse_move(pos, rel, buttons)
    
def on_key_up(key):
    game_manager.on_key_up(key)
    
def on_music_end():
    game_manager.on_music_end()

def update(dt):
    game_manager.update(dt)

def draw():    
    screen.clear()
    game_manager.draw(screen)

pgzrun.go()