import pgzrun
from pgzero.builtins import *
from pgzhelper import *
import pgzero
import os

from helper import Actor, ActorContainer
from managers import scene_manager, input_manager, SceneManager
from gui import Button, Menu, Item
from camera import Camera
from entity import Player, Entity, Collisions
from level_design import World
from constants import Constants

screen: pgzero.screen.Screen

os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 662
HEIGHT = 662
TITLE = "I wanna kms"

cam = Camera(pos=(0, 200))
cam.initialize_camera(0, (600, 450))

intro = Entity("dragon_3.png", pos=(WIDTH / 2, HEIGHT / 2))
intro.fps = 24

StartScreen = Button('play_button.png', (331, 331), on_click=lambda: scene_manager.switch_scene('Camera'), hidden=True)
StartScreen.scale = 0.1
StartScreen.Bind(input_manager, 'Start Screen')

def hm(x, y):
    print(x, y)
    intro.pause_gif()

input_manager.subscribe(Constants.KEY_DOWN, hm, 'Global')

def play_start_screen_animation():
    intro.play_gif(
        "intro_card", 1,
        on_finish=lambda: intro.play_gif(
            "intro", 1,
            on_finish=start_screen
        ),
    )

def start_screen():
    intro.image = "intro_frame_84.png"
    StartScreen.hidden = False
    input_manager.set_group('Start Screen')
    
### PARTITION

scene_manager.subscribe(
    "a",
    UI_elements=ActorContainer(
        a := Entity("dragon_1.png", pos=(300, 300), is_static=True),
        b := Entity("dragon_1.png", pos=(300, 300), is_static=False),
    ),
)

scene_manager.subscribe("Start Screen", on_show=play_start_screen_animation, UI_elements=ActorContainer(intro, StartScreen))
scene_manager.subscribe("Camera", UI_elements=ActorContainer(cam))
scene_manager.show_scene('Start Screen')

input_manager.set_group('Global')

# scene_manager = SceneManager()

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