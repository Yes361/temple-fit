import pgzrun
from pgzero.builtins import *
from pgzhelper import *
import os

from helper import Actor, ActorContainer
from managers import scene_manager, input_manager, SceneManager
from gui import Button, Menu, Item
# from camera import Camera
from entity import Player, Entity, Collisions
from level_design import World
from constants import Constants

os.environ["SDL_VIDEO_CENTERED"] = "1"  # Forces window to be centered on screen.
WIDTH = 662
HEIGHT = 662
TITLE = "I wanna kms"

intro = Entity('dragon_3.png', pos=(WIDTH / 2, HEIGHT / 2))
intro.fps = 24

scene_manager.subscribe('a', None, None, ActorContainer([a := Entity('dragon_1.png', pos=(300, 300), is_static=True), b := Entity('dragon_1.png', pos=(300, 300), is_static=False)]))
scene_manager.subscribe('b', UI_elements=ActorContainer([intro]))
scene_manager.show_scene('b')

input_manager.subscribe(Constants.KEY_DOWN, lambda x, y: print(x, y), 'Global')

def on_mouse_down(pos, button):
    pass

def on_key_down(key, unicode):
    input_manager.on_key_down(key, unicode)
    
    intro.play_gif('intro_card', 1, on_finish=lambda: intro.play_gif('intro', 1, on_finish=lambda: intro.play_gif('outro_card', 1)))


def update(dt):    
    scene_manager.update(dt)
    input_manager.on_key_hold(dt)
    input_manager.on_mouse_hover(pygame.mouse.get_pos())
    
    # Collisions.resolve(a, b)
    # a.pos = pygame.mouse.get_pos()

def draw():
    screen.clear()
    scene_manager.draw(Screen=screen)

pgzrun.go()
