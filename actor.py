from pgzero.builtins import Actor
import pygame
import pgzrun

class Actor(Actor):
    ACCEPTED_KWARGS = ['topleft', 'bottomleft', 'topright', 'bottomright',
    'midtop', 'midleft', 'midbottom', 'midright',
    'center']
    def __init__(self, *args, **kwargs):
        self.hidden = False
        super().__init__(*args, **kwargs)
    
    def draw(self):
        if not self.hidden:
            super().draw()
            
    def update(self, dt=0):
        pass
    
    def reset(self, dt=0):
        pass
    
# class FrameActor:
#     def __init__(self, frame=None):
#         self.hidden = False
#         self.pos = (0, 0)
#         self.dims = (640, 480)
#         self.frame = frame if frame else pygame.Surface(self.dims)
        
#     def draw(self, screen):
#         if not self.hidden:
#             screen.blit(self.frame, self.pos)
