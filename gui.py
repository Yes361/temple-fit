from level_design import ActorContainer
import pygame
from actor import Actor

class button(Actor):
    """
    asds
    """ 
    def on_hover(self, pos):
        if self.collidepoint(pos):
            print('l')
    
    def on_hold(self):
        pass
    
    def on_click(self):
        self.callback()
        
    def update(self, dt=0):
        pos = pygame.mouse.get_pos()
        self.on_hover(pos)

class SceneManager:
    """
    
    """
    def __init__(self):
        self.scenes = {}
        self.callbacks = {}
        self.current_scene = None
    
    def add_scene(self, scene_name, actor_list: ActorContainer, callback: callable = None):
        actor_list.hidden = True
        self.scenes[scene_name] = actor_list
        self.callbacks[scene_name] = callback
        
    def set_scene(self, scene_name):
        if scene_name not in self.scenes:
            return
        
        for scene in self.scenes.keys():
            self.scenes[scene].hidden = not scene == scene_name
        
        if fn := self.callbacks[scene_name]:
            fn()
            
    def draw_scenes(self):
        for scene in self.scenes.values():
            scene.draw()