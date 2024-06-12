from pgzero.builtins import keyboard, keys, Rect
from .collisions import Collider
from helper import Actor

DEFAULT_ENTITY_SPEED = 2

class Entity(Collider):
    def __init__(self, *args, **kwargs):
        self.speed = kwargs.pop('speed', DEFAULT_ENTITY_SPEED)
        self.animations = kwargs.pop('animation', {})
        super().__init__(*args, **kwargs)
    
class Enemies(Entity):
    pass

class Player(Entity):
    def __init__(self, *args, animation_frames=None, **kwargs):
        self.animation_frames = animation_frames
        self._is_moving = False
        self._current_anim = 'idle'
        if animation_frames is None:
            self.animation_frames = {
                'up': [],
                'down': [],
                'left': [],
                'right': [],
                'idle': []
            }
        super().__init__(*args, **kwargs)
        
    def move(self, dt):
        anim = 'idle'
        if keyboard[keys.S] or keyboard[keys.DOWN]:
            self.y += self.speed
            anim = 'down'
            
        if keyboard[keys.W] or keyboard[keys.UP]:
            self.y -= self.speed
            anim = 'up'
            
        if keyboard[keys.D] or keyboard[keys.RIGHT]:
            self.x += self.speed
            anim = 'right'
            
        if keyboard[keys.A] or keyboard[keys.LEFT]:
            self.x -= self.speed
            anim = 'left'
            
        self.anim = self.animation_frames[anim]
            
    def update(self, dt):
        self.move(dt)
        self.animate()
        super().update(dt)
        
    def on_collide(self, collision):
        print('hi')