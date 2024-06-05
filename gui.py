from utils import Actor, ActorContainer, require_kwargs
from dataclasses import dataclass
from typing import List
import pygame
import pgzero.game as game

class Button(Actor):
    """
    asds
    """ 
    REQUIRED_KWARGS = ['callback']
    def __init__(self, *args, **kwargs):
        require_kwargs(Button.REQUIRED_KWARGS, kwargs)
        self.callback = None
        super().__init__(*args, **kwargs)
    
    def on_hover(self, pos):
        if self.collidepoint(pos):
            print('l')
    
    def on_hold(self):
        pass
    
    def on_click(self, pos):
        self.callback()
        
    def update(self, dt=0):
        pos = pygame.mouse.get_pos()
        
        self.on_hover(pos)
        if self.collidepoint(pos):
            self.on_click(pos) 
            
class Menu:
    def __init__(self, pos, dims):
        self.UI_elements = ActorContainer()
        self.pos = pos
        self.dims = dims
                
    def draw(self, *args, **kwargs):        
        surf = pygame.Surface((100, 100), masks=pygame.SRCALPHA)
        surf.fill((255, 0, 0))
        
        game.screen.blit(surf, (50, 50)) # Import Screen
        self.UI_elements.draw(*args, **kwargs)
        
    def update(self, dt):
        pass

@dataclass
class Scene:
    update_callback: callable = None
    draw_callback: callable = None
    scene_UI: ActorContainer = None

class SceneManager: 
    """
    
    """
    def __init__(self):
        self.scenes: List
        self._current_scene = None
    
    def add_scene(self, scene_name, update_callback: callable, draw_callback: callable, UI_elements: ActorContainer=None):
        self.update_callback[scene_name] = update_callback
        self.draw_callback[scene_name] = draw_callback
        self.scene_UI[scene_name] = UI_elements
            
    def remove_scene(self, scene_name):
        self.update_callback.pop(scene_name)
        self.draw_callback.pop(scene_name)
        self.scene_UI.pop(scene_name)

    def set_scene(self, scene_name):
        self._current_scene = scene_name
        
    def get_scene(self):
        return self._current_scene

    def switch_scene(self, scene_name):
        self._current_scene = scene_name
        for name, scene in self.scene_UI.items():
            if scene == None:
                continue
            
            if name == scene_name:
                self.show_scene(name)
            else:
                self.hide_scene(name)
        
    def show_scene(self, scene_name):
        self.scene_UI[scene_name].hidden = False
        
    def hide_scene(self, scene_name):
        self.scene_UI[scene_name].hidden = True
    
    def draw(self, *args, **kwargs):
        callback = self.draw_callback[self._current_scene]
        if self._current_scene and callback:
            callback()
        
        UI_elements = self.scene_UI[self._current_scene]
        if UI_elements:
            UI_elements.draw(*args, **kwargs)
        
    def update(self, dt):
        callback = self.update_callback[self._current_scene]
        if self._current_scene and callback:
            callback()
        
        UI_elements = self.scene_UI[self._current_scene]
        if UI_elements:
            UI_elements.update(dt)