from helper import ActorContainer, Actor, AbstractActor
from .collisions import Collisions
from .entity import Entity, Player
from pgzero.builtins import Rect
from typing import List
        
class LevelManager(AbstractActor):
    def __init__(self, **kwargs):
        self.player: Entity = kwargs.get('player', Player('character.png'))
        self.world: Actor = kwargs.get('world', Actor('hallway.png', pos=(331, 331)))
        self.world.scale = 0.1
        
        rect = Entity('character')
        rect.resize((self.world.topright[0], 100))
        rect.pos = self.world.topleft
        rect.is_static = True
        
        self.colliders = Collisions(
            (rect, lambda: print("HI"))
        )
            
    def load_level(self, f):
        pass
    
    def save_level(self, f):
        pass
    
    def update(self, dt):
        self.player.update(dt)
        self.colliders.resolve_entity_collisions(self.player)
    
    def draw(self, screen):
        self.world.draw()
        self.player.draw()
        for collider, callback in self.colliders.rect_list:
            collider.draw()