from helper import Actor, ActorBase, ActorContainer, require_kwargs
from constants import Constants
import pygame

class Button(Actor):
    """
    asds
    """ 
    def __init__(self, *args, on_click: callable = None, on_hover: callable = None, **kwargs):
        self.on_click_callback = on_click
        self.on_hover_callback = on_hover
        self._input_manager = None
        super().__init__(*args, **kwargs)
    
    def on_hover(self, pos):
        if self.hidden:
            return
        
        if self.collidepoint(pos) and self.on_hover_callback:
            self.on_hover_callback()
    
    def on_hold(self):
        pass
    
    def on_click(self, pos):
        if self.hidden:
            return
        
        if self.on_click_callback:
            self.on_click_callback()
        
    # def 
    def Bind(self, input_manager, group_identifer):
        self._input_manager = input_manager
        self.group_identifier = group_identifer
        self._input_manager.subscribe(Constants.MOUSE_HOVER, self.on_hover, self.group_identifier)
    
    def Release(self):
        self._input_manager.unsubscribe(self.on_hover, self.group_identifier)
        self._input_manager = None
    
            
class Menu(ActorBase):
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

class Item(Actor):
    def __init__(self, *args, slot_image='', **kwargs):
        self.item_count = 0
        self._is_slot = False
        self.slot_image = slot_image
        super().__init__(*args, **kwargs)
    
    def set_inventory_icon(self):
        self.image = self.slot_image
        self._is_slot = True
        
    def draw(self, *args, Screen, **kwargs):
        super().draw()
        if not self._is_slot:
            return
    
        # require_kwargs(['Screen'], kwargs, error_msg='%s is required. Pass it to the Scene Manager\'s draw function')
        # Screen = kwargs['Screen']
        Screen.draw.text(f'{self.item_count}', self.pos)

class Inventory:
    def __init__(self):
        pass
    
    def draw():
        pass
    
    def update():
        pass