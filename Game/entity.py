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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def move(self, dt):
        if keyboard[keys.S] or keyboard[keys.DOWN]:
            self.y += self.speed
        if keyboard[keys.W] or keyboard[keys.UP]:
            self.y -= self.speed
        if keyboard[keys.D] or keyboard[keys.RIGHT]:
            self.x += self.speed
        if keyboard[keys.A] or keyboard[keys.LEFT]:
            self.x -= self.speed
            
    def update(self, dt):
        self.move(dt)
        
    def on_collide(self, collision):
        print('hi')