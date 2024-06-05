from utils import Actor
from pgzero.builtins import keyboard, keys

class Entity(Actor):
    def __init__(self, *args, **kwargs):
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
    def resolve(ActorA, ActorB):
        if not ActorA.colliderect(ActorB):
            return
        
        # min(ActorB.left - ActorA.right, )