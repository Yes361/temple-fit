from .start import StartScreen
from .fight import battle
from Game import camera
from managers import game_manager

camera.initialize_camera(0, (600, 450))

StartScreen()
battle()

game_manager.show_scene('Battle')