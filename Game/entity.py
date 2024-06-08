from helper import Actor
from pgzero.builtins import keyboard, keys, Rect

class Entity(Actor):
    def __init__(self, *args, **kwargs):
        self.is_static = kwargs.get('is_static', True)
        super().__init__(*args, **kwargs)
    
class Enemies(Entity):
    pass

class Player(Entity):
    def __init__(self, *args, **kwargs):
        self.speed = 2
        super().__init__(*args, **kwargs)
        
    def move(self):
        if keyboard[keys.S] or keyboard[keys.DOWN]:
            self.y += self.speed
        if keyboard[keys.W] or keyboard[keys.UP]:
            self.y -= self.speed
        if keyboard[keys.D] or keyboard[keys.RIGHT]:
            self.x += self.speed
        if keyboard[keys.A] or keyboard[keys.LEFT]:
            self.x -= self.speed

class Collisions:
    @staticmethod
    def resolve(EntityA: Rect | Entity, EntityB: Rect | Entity):
        if not EntityA.colliderect(EntityB) or (EntityA.is_static and EntityB.is_static):
            return
        
        overlap_x = min(EntityA.right - EntityB.left, EntityB.right - EntityA.left)
        overlap_y = min(EntityA.bottom - EntityB.top, EntityB.bottom - EntityA.top)

        if overlap_x < overlap_y:
            sign = 1 if EntityA.centerx > EntityB.centerx else -1
            
            if getattr(EntityA, 'is_static', True):
                EntityB.x -= overlap_x * sign
            else:
                EntityA.x += overlap_x * sign
        else:
            sign = 1 if EntityA.centery > EntityB.centery else -1
            
            if getattr(EntityA, 'is_static', True):
                EntityB.y -= overlap_y * sign
            else:
                EntityA.y += overlap_y * sign