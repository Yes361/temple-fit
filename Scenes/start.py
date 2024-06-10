from managers import Scene, game_manager
from helper import Actor, ActorContainer
from Game import Button

class StartScreen(Scene):
    SCENE_NAME = 'Start Screen'
    
    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_hide(self):
        pass

    def on_show(self):
        pass

    def on_draw(self, screen):
        pass
    
    def on_update(self, dt):
        pass
        
    def on_mouse_down(self, pos, button):
        pass
            
    def on_key_down(self, key, unicode):
        pass