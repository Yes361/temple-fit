from helper import GUIElement, Actor, Rect
from typing import Dict
from pgzero.builtins import animate
import pygame

class Button(Actor, GUIElement):
    """
    A GUI button that can respond to click and hover events.
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
        
class HealthBar(Actor, GUIElement):
    """
    A GUI health bar that can display and animate changes in health.
    """
    def __init__(self, image, extents, total_hp, *args, counter_default=0, on_hp_change=None, fill=(255, 0, 0), **kwargs):
        self._counter_value = counter_default
        self.on_hp_change = on_hp_change
        self.percent_filled = 1
        self.total_hp = total_hp
        self._hp = total_hp
        self._anim = None
        self.extents: Rect = extents
        self.fill = fill
        super().__init__(image, *args, **kwargs)
    
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        self._hp = value
        self.percent_filled = self._hp / self.total_hp
        if self._anim is not None:
            self._anim.stop(complete=False)
        
    def animate_damage(self, loss_hp):
        """
        Animate the health bar to show damage taken.
        
        @params:
            loss_hp (int): The amount of health points lost.
        """
        fn = self.on_hp_change
        if callable(fn):
            fn = lambda: self.on_hp_change(self.hp - loss_hp)
        self._anim = animate(self, duration=5, on_finished=fn, hp=self.hp - loss_hp)
        
    def draw(self, screen):
        """
        Draw the health bar on the screen.
        
        @params:
            screen (pygame.Surface): The surface to draw the health bar on.
        """
        super().draw()
        pos = (self.extents.x + self.left, self.extents.y + self.top)
        dims = (self.extents.width * self.percent_filled * self.scale, self.extents.height * self.scale)
        screen.draw.filled_rect(Rect(pos, dims), self.fill)
        
    