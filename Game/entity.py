from pgzero.builtins import keyboard, keys
from .collisions import Collider
from .gui import HealthBar
from helper import Actor, Rect
from typing import Type

DEFAULT_ENTITY_SPEED = 2

class Entity(Collider):
    def __init__(self, *args, healthbar: HealthBar=None, speed=DEFAULT_ENTITY_SPEED, animation={}, **kwargs):
        self.speed = speed
        self.health = healthbar
        self.animations = animation
        super().__init__(*args, **kwargs)
        
        
    def draw(self, screen):
        if self.hidden:
            return
        
        self.health.draw(screen)
        super().draw()
    
class Enemy(Entity):
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
        
        if self.images != self.animation_frames[anim]:
            self.images = self.animation_frames[anim]
            
    def update(self, dt):
        self.move(dt)
        self.animate()
        super().update(dt)
        
    def on_collide(self, collision):
        print('hi')