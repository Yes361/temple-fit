from pgzero.builtins import *
import pgzrun
from pgzhelper import *
import sys
import os

from utils import Actor, ActorContainer
from gui import SceneManager, Button, Menu
from camera import Camera
from input import inputManager
from entity import Player

from level_design import World

os.environ["SDL_VIDEO_CENTERED"] = "1"  # Forces window to be centered on screen.
WIDTH = 800
HEIGHT = 600
TITLE = ""

cam1 = Camera()
cam1.initialize_camera(0, (640, 480))

scene = SceneManager()
input_manager = inputManager()

def cam():
    screen.blit(cam1.draw((WIDTH - 100, HEIGHT - 100)), (50, 50))

scene.add_scene(
    "cam",
    None,
    cam,
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
    ActorContainer([t := World(64), c, Menu(1, 1)])
)

scene.set_scene("cam1")

for i in range(5):
    for j in range(5):  
        t.add_tile(f'a2_flora_{i * j}.png', (i, j))

input_manager.subscribe('Global', c.move, inputManager.KEY_HOLD)

# def on_mouse_down(pos, button):
    # pass

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
