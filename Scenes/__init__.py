from .start import StartScreen
from .globals import Global
from Game import Camera
from managers import game_manager

Global.cam = Camera(pos=(0, 200))
Global.cam.initialize_camera(0, (600, 450))

StartScreen()
game_manager.show_scene('Start Screen')