from .start_screen import StartScreen
from .camera_screen import CameraScreen
from camera import Camera

WIDTH = 662
HEIGHT = 662
cam = Camera(pos=(0, 200))
cam.initialize_camera(0, (600, 450))

StartScreen(WIDTH, HEIGHT)
CameraScreen(cam)