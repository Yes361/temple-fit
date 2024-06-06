from utils import Actor
from pgzero.builtins import keyboard, keys, Rect

class Entity(Actor):
    def __init__(self, *args, **kwargs):
        self.is_static = True
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
    def resolve(ActorA: Rect | Actor, ActorB: Rect | Actor):
        if not ActorA.colliderect(ActorB):
            return
        
        overlap_x = min(ActorA.right - ActorB.left, ActorB.right - ActorA.left)
        overlap_y = min(ActorA.bottom - ActorB.top, ActorB.bottom - ActorA.top)

        if overlap_x < overlap_y:
            sign = 1 if ActorA.centerx > ActorB.centerx else -1
            ActorB.x -= overlap_x * sign
        else:
            sign = 1 if ActorA.centery > ActorB.centery else -1
            ActorB.y -= overlap_y * sign