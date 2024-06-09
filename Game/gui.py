from helper import GUIElement
import pygame

class Button(GUIElement):
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
        
    def on_click(self, pos, button):
        if self.hidden:
            return
        
        if self.collidepoint(pos) and callable(self.event_click):
            self.event_click(pos, button)
    
    def update(self, dt):
        self.on_hover(pygame.mouse.get_pos())
        super().update(dt)