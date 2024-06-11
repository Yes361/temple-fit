from helper import ActorContainer, Actor
from managers import Scene
from Game import camera
from pgzero.builtins import Rect


class battle(Scene):
    SCENE_NAME = 'Battle'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
            
    def on_show(self):
        global backdrop, character
        
        camera.resize((300, 300 * 3 / 4))
        camera.pos=(50, 50)
        
        backdrop = Actor('battle-backdrop')
        backdrop.resize((662, 662))

        character = Actor('character', pos=(200, 400))    
        
    def on_hide(self):
        pass
    
    def on_draw(self, screen):
        pass
    
    def on_update(self, dt):
        pass
        
    def on_key_down(self, key, unicode):
        print(key, unicode)