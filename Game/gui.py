from helper import GUIElement
import pygame

class Button(GUIElement):
    """
    asds
    """ 
    def __init__(self, image, *args, on_click: callable = None, on_hover: callable = None, held_frame=None, hover_frame=None, **kwargs):
        self.event_click = on_click
        self.event_hover = on_hover
        self.frames = {'held_frame': held_frame, 'hover_frame': hover_frame, 'og_frame': image}
        super().__init__(image, *args, **kwargs)
    
    def on_hover(self, pos):
        if self.hidden:
            return False
        
        if self.collidepoint(pos):
            if callable(self.event_hover):
                self.event_hover()
            
            return True
        return False            
            
        
    def on_click(self, pos, button):
        if self.hidden:
            return
        
        if self.collidepoint(pos): 
            if callable(self.event_click):
                self.event_click(pos, button)
    
    def update(self, dt):
        self.on_hover(pygame.mouse.get_pos())
        super().update(dt)
        
class HealthBar(GUIElement):
    def __init__(self, *args, counter_default=0, images=[], **kwargs):
        if len(images) == 0:
            raise Exception('Health Bar should have an image')
        self._counter_value = counter_default
        super().__init__(images[0], *args, **kwargs)
        self.images = images
        
    @property
    def counter_value(self):
        return self._counter_value
    
    @counter_value.setter
    def counter_value(self, idx):
        if idx > len(self.images) - 1:
            idx = len(self.images) - 1
        elif idx < 0:
            idx = 0
        elif idx != self._counter_value:
            self._counter_value = idx
            self.image = self.images[idx]
        
    def change_counter(self, amount):
        self.counter_value += amount
            
    def set_counter(self, amount):
        if amount > len(self.images) or amount < 0:
            raise Exception(f'{amount} is out of bounds')
        self.counter_value = amount