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
        del backdrop
        del character
    
    def on_draw(self, screen):
        backdrop.draw()
        camera.draw()
        character.draw()
        screen.draw.filled_rect(Rect((100, 500), (200, 100)), (255, 255, 255))
        screen.draw.filled_rect(Rect((400, 450), (200, 100)), (255, 255, 255))
    
    def on_update(self, dt):
        pass
        
    def on_key_down(self, key, unicode):
        print(key, unicode)