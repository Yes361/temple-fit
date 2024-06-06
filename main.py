import pgzrun
from pgzero.builtins import *
from pgzhelper import *
import os

from helper import Actor, ActorContainer
from managers import scene_manager, input_manager, SceneManager
from gui import Button, Menu, Item
from camera import Camera
from entity import Player, Entity, Collisions
from level_design import World
from constants import Constants

os.environ["SDL_VIDEO_CENTERED"] = "1"  # Forces window to be centered on screen.
WIDTH = 662
HEIGHT = 662
TITLE = "I wanna kms"

cam = None
def initialize_cam(screen):
    global cam
    cam = Camera(Screen=screen)
    cam.initialize_camera(0, (662, 662))

intro = Entity("dragon_3.png", pos=(WIDTH / 2, HEIGHT / 2))
intro.fps = 24

StartScreen = Button('play_button.png', (331, 331), on_hover=lambda: scene_manager.switch_scene('Camera'), hidden=True)
StartScreen.scale = 0.1
StartScreen.Bind(input_manager, 'Start Screen')

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
    
def draw_camera():
    screen.blit(cam.draw((400, 300)), (131, 181))
    
### PARTITION

scene_manager.subscribe(
    "a",
    UI_elements=ActorContainer(
        [
            a := Entity("dragon_1.png", pos=(300, 300), is_static=True),
            b := Entity("dragon_1.png", pos=(300, 300), is_static=False),
        ]
    ),
)
scene_manager.subscribe("Start Screen", on_show=play_start_screen_animation, UI_elements=ActorContainer([intro, StartScreen]))
scene_manager.subscribe("Camera", draw_callback=draw_camera)
scene_manager.show_scene('Start Screen')

def on_mouse_down(pos, button):
    pass


def on_key_down(key, unicode):
    input_manager.on_key_down(key, unicode)

def update(dt):
    scene_manager.update(dt)
    input_manager.on_key_hold(dt)
    input_manager.on_mouse_hover(pygame.mouse.get_pos())


def draw():
    screen.clear()
    scene_manager.draw(Screen=screen)

initialize_cam(screen)
pgzrun.go()