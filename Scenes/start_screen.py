from managers import Scene, input_manager, scene_manager
from Game import Button
from helper import Actor, ActorContainer
from constants import Constants

Actors = ActorContainer()

class StartScreen(Scene):
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        super().__init__('Start Screen', self)
        
    def on_draw(self, screen):
        pass
    
    def on_hide(self):
        pass
    
    def on_show(self):
        pass
    
    def on_update(self, dt):
        pass
    
    def load_actors(self):
        pass
        
    def hm(self, x, y):
        pass

    def start_screen(self):
        pass