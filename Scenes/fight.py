from helper import ActorContainer, Actor
from managers import Scene
from Game import camera, HealthBar
from pgzero.builtins import Rect


class battle(Scene):
    SCENE_NAME = 'Battle'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
            
    def on_show(self):
        global backdrop, character, a, b
        
        camera.resize((300, 300 * 3 / 4))
        camera.pos=(50, 50)
        
        backdrop = Actor('battle-backdrop')
        backdrop.resize((662, 662))

        character = Actor('character', pos=(200, 400))
        a = HealthBar(pos=(331, 331), images=['intro_card_frame_001', 'intro_card_frame_055', 'intro_card_frame_148'], scale=0.1)
        # b = HealthBar()
        
    def on_hide(self):
        pass
    
    def on_draw(self, screen):
        backdrop.draw()
        camera.draw(screen)
        # screen.draw.rect(Rect(()), (255, 255, 255))
        a.draw()
        # b.draw()
    
    def on_update(self, dt):
        pass
        
    def on_key_down(self, key, unicode):
        print(key, unicode)
        a.change_counter(1)
        print(a._counter_value, a.scale, a.width, a.height)