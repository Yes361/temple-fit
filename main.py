import pgzrun
import pgzero.screen
import os

from managers import game_manager, GameManager
import Scenes

screen: pgzero.screen.Screen
os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 662
HEIGHT = 662
TITLE = "I wanna kms"

def on_mouse_down(pos, button):
    game_manager.on_mouse_down(pos, button)

def on_key_down(key, unicode):
    game_manager.on_key_down(key, unicode)

def update(dt):
    game_manager.update(dt)

def draw():    
    screen.clear()
    game_manager.draw(screen)

pgzrun.go()