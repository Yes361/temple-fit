from utils import Actor, EventManager, ActorContainer, require_kwargs
from dataclasses import dataclass
from typing import List, Dict
import pygame

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
        self.hidden = False
                
    def draw(self, *args, **kwargs):
        if self.hidden:
            return
        
        require_kwargs(['Screen'], kwargs, error_msg='%s is required. Pass it to the Scene Manager\'s draw function')
        Screen = kwargs['Screen'] # Import Screen
        
        surf = pygame.Surface((100, 100), masks=pygame.SRCALPHA)
        surf.fill((255, 0, 0))
        
        Screen.blit(surf, (50, 50))
        self.UI_elements.draw(*args, **kwargs)

    def update(self, dt):
        pass
