from managers import Scene
from camera import Camera
from helper import ActorContainer

class CameraScreen(Scene):
    def __init__(self):
        self.UI_elements = None
        super().__init__('Camera', self)
        
    def on_draw(self, screen):
        self.cam.draw(screen)
        return super().on_draw(screen)
    
    def on_hide(self):
        return super().on_hide()
    
    def on_show(self):
        self.cam = Camera(pos=(0, 200))
        self.cam.initialize_camera(0, (600, 450))
        self.UI_elements = ActorContainer(self.cam)
        return super().on_show()
    
    def on_update(self, dt):
        return super().on_update(dt)