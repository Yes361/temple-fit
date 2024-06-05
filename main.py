from pgzero.builtins import *
import pgzrun
from pgzhelper import *
import sys
import os

from utils import Actor, ActorContainer
from gui import SceneManager, Button
from camera import Camera
from input import inputManager
from entity import Player

os.environ["SDL_VIDEO_CENTERED"] = "1"  # Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ""

# c = Camera()
# c.initialize_camera(0, (640, 480))

scene = SceneManager()
input_manager = inputManager()

scene.add_scene(
    "cam",
    None,
    None,
    ActorContainer([
        a := Actor("dragon_1.png", pos=(500, 500), collision=True), 
        b := Button("dragon_2.png", pos=(300, 300), callback=lambda: None),
        c := Player("dragon_3.png", pos=(200, 200))
    ]),
)

scene.add_scene(
    "cam1",
    None,
    None,
)

scene.set_scene("cam")

input_manager.subscribe('Global', c.move, inputManager.KEY_HOLD)
input_manager.subscribe('Global', lambda x, y: print(y), inputManager.KEY_DOWN)

def on_mouse_down(pos, button):
    a.pos = pos

def on_key_down(key, unicode):
    input_manager.on_key_down(key, unicode)
    # input_manager.unsubscribe('Global', c.move)

def update(dt):
    scene.update(dt)
    input_manager.on_key_hold(dt)

def draw():
    screen.clear()
    scene.draw()


pgzrun.go()
