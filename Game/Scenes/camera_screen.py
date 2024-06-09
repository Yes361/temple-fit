from managers import Scene
from Game.camera import Camera
from helper import ActorContainer

class CameraScreen(Scene):
    def __init__(self, cam):
        self.cam = cam
        super().__init__('Camera', self)
        
    def on_draw(self, screen):
        self.cam.draw(screen)
        pass
    
    def on_hide(self):
        pass
    
    def on_show(self):
        pass
    
    def on_update(self, dt):
        pass