from helper import ActorContainer, Actor
from managers import Scene
from Game import camera
from pgzero.builtins import Rect

all_actors = ActorContainer(
    UI_element = ActorContainer(),
    Actors = ActorContainer()   
)
Actors = all_actors.Actor 
UI_element = all_actors.UI_element

backdrop = Actor('battle-backdrop')
backdrop.resize((662, 662))

battle_tab = Actor('battle_scene_tab')
battle_tab.scale = 0.2
battle_tab.left = 0
battle_tab.top = 662 - battle_tab.height

character = Actor('character')

class battle(Scene):
    SCENE_NAME = 'Battle'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
        self.globals = kwargs
        
    def on_draw(self, screen):
        backdrop.draw(screen)
        camera.draw(screen)
        character.draw(screen)
        screen.draw.filled_rect(Rect((200, 500), (100, 100)), (255, 255, 255))
        battle_tab.draw(screen)
    
    def on_update(self, dt):
        pass
    
    def on_hide(self):
        pass
    
    def on_show(self):
        camera.resize((300, 300 * 3 / 4))
        camera.pos=(200, 50)