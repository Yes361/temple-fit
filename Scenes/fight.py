from helper import ActorContainer, Actor
from managers import Scene
from Game import camera, HealthBar
from pgzero.builtins import Rect

def create_battle_icon():
    character = Actor('character', pos=(200, 400))
    a = HealthBar(pos=(331, 331), images=['healthbar_1', 'healthbar_2', 'healthbar_3', 'healthbar_4', 'healthbar_5', 'healthbar_6'], scale=0.6)
    return character, a

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

        character, a = create_battle_icon()
        # b = HealthBar()
        
    def on_hide(self):
        pass
    
    def on_draw(self, screen):
        backdrop.draw()
        camera.draw(screen)
        # screen.draw.rect(Rect(()), (255, 255, 255))
        # b.draw()
    
    def on_update(self, dt):
        pass
        
    def on_key_down(self, key, unicode):
        a.change_counter(1)