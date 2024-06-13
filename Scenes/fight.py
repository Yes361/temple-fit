from helper import ActorContainer, Actor
from managers import Scene
from Game import camera, HealthBar, Text, CheckList
from pgzero.builtins import Rect

def create_battle_icon():
    return ActorContainer(
        character = Actor('character', pos=(331, 300)),
        a = HealthBar(pos=(331, 361), images=['healthbar_1', 'healthbar_2', 'healthbar_3', 'healthbar_4', 'healthbar_5', 'healthbar_6'], scale=0.6)
    )

class battle(Scene):
    SCENE_NAME = 'Battle'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
            
    def on_show(self):
        global backdrop, a, b, c
        
        camera.resize((300, 300 * 3 / 4))
        camera.pos=(50, 50)
        
        backdrop = Actor('battle-backdrop')
        backdrop.resize((662, 662))

        a = create_battle_icon()
        a.pos = (200, 200)
        b = create_battle_icon()
        
        c = CheckList((50, 331), spacing=50)
        c.create_new_objective('5', 'rah')
        
    def on_hide(self):
        pass
    
    def on_draw(self, screen):
        backdrop.draw()
        camera.draw(screen)
        a.draw()
        b.draw()
        c.draw(screen)
        
    def on_update(self, dt):
        pass
        
    def on_key_down(self, key, unicode):
        # a.change_counter(1)
        pass