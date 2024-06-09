from helper import Actor, ActorBase, ActorContainer
from constants import Constants
import pygame

class Button(Actor):
    """
    asds
    """ 
    def __init__(self, *args, on_click: callable = None, on_hover: callable = None, **kwargs):
        self.event_click = on_click
        self.event_hover = on_hover
        self._input_manager = None
        super().__init__(*args, **kwargs)
    
    def on_hover(self, pos):
        if self.hidden:
            return
        
        if self.collidepoint(pos) and callable(self.event_hover):
            self.event_hover()
        
    def on_click(self, pos, buttons):
        if self.hidden:
            return
        
        if self.collidepoint(pos) and any(buttons) and callable(self.event_click):
            self.event_click()
            
    def handle_mouse_input(self):
        self.on_hover(pygame.mouse.get_pos())
        self.on_click(pygame.mouse.get_pressed())
        
    def update(self, dt):
        super().update(dt)
        
    def Bind(self, input_manager, identifier):
        self._input_manager = input_manager
        self.identifier = identifier
        self._input_manager.subscribe(Constants.MOUSE_HOVER, self.on_hover, self.identifier)
        self._input_manager.subscribe(Constants.MOUSE_DOWN, self.on_click, self.identifier)
    
    def Release(self):
        self._input_manager.unsubscribe(self.on_hover, self.identifier)
        self._input_manager.unsubscribe(self.on_click, self.identifier)
        self._input_manager = None
    
            
class Menu(ActorBase):
    def __init__(self, pos, dims):
        self.UI_elements = ActorContainer()
        self.pos = pos
        self.dims = dims
        self.hidden = False
                
    def draw(self, screen):
        if self.hidden:
            return
        
        
        surf = pygame.Surface((100, 100), masks=pygame.SRCALPHA)
        surf.fill((255, 0, 0))
        
        screen.blit(surf, (50, 50))
        self.UI_elements.draw(screen)

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
        
    def draw(self, screen):
        super().draw()
        if not self._is_slot:
            return

        screen.draw.text(f'{self.item_count}', self.pos)

class Inventory(Actor):
    def __init__(self):
        pass
    
    def draw(self, screen):
        pass
    
    def update(self, dt):
        pass