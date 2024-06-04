from pgzero.builtins import Actor
import pygame

class Actor(Actor):
    EXPECTED_INIT_KWARGS = set(['pos', 'topleft', 'bottomleft', 'topright', 'bottomright',
    'midtop', 'midleft', 'midbottom', 'midright', 'center'])
    
    def __init__(self, *args, **kwargs):
        self.hidden = False
        
        keys = list(kwargs.keys())
        for key in keys:
            if key not in Actor.EXPECTED_INIT_KWARGS:
                setattr(self, key, kwargs[key])
                kwargs.pop(key)

        super().__init__(*args, **kwargs)
    
    def draw(self):
        if not self.hidden:
            super().draw()
            
    def update(self, dt=0):
        pass
    
    def reset(self):
        pass
