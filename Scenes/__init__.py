from .start_screen import StartScreen
from Game import Camera
from managers import scene_manager

cam = Camera(pos=(0, 200))
cam.initialize_camera(0, (600, 450))

StartScreen()
scene_manager.show_scene('Start Screen')