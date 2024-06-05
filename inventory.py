from utils import Actor, ActorContainer, require_kwargs
import pygame

class Item(Actor):
    def __init__(self, *args, **kwargs):
        self.item_count = 0
        self._is_slot = False
        self.slot_image = '10_boss_17.png'
        super().__init__(*args, **kwargs)
    
    def set_inventory_icon(self):
        self.image = '10_boss_17.png'
        self._is_slot = True
        
    def draw(self, *args, **kwargs):
        super().draw()
        if not self._is_slot:
            return
    
        require_kwargs(['Screen'], kwargs, error_msg='%s is required. Pass it to the Scene Manager\'s draw function')
        Screen = kwargs['Screen']
        Screen.draw.text(f'{self.item_count}', self.pos)

class Inventory:
    def __init__(self):
        pass
    
    def draw():
        pass
    
    def update():
        pass