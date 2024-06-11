from helper import ActorContainer, Actor, AbstractActor
from .collisions import Collisions, ColliderRect
from .entity import Entity, Player
from pgzero.builtins import Rect
from typing import List
        
class LevelManager(AbstractActor):
    def __init__(self, **kwargs):
        self.player: Entity = kwargs.get('player', Player('character.png'))
        self.world: Actor = kwargs.get('world', Actor('hallway.png', pos=(331, 331), scale=0.2))
        self.camera = [self.player.x, self.player.y]
        
        rect = ColliderRect((self.world.topleft[0], self.world.topleft[1] - 100), (500, 100))
        rect.is_static = True
                
        self.colliders = Collisions(
            rect
        )
            
    def load_level(self, f):
        pass
    
    def save_level(self, f):
        pass
    
    def update(self, dt):
        self.player.update(dt)
        self.colliders.resolve_entity_collisions(self.player)
                
    def offset(self, pos):
        x, y = pos
        self.world.x -= x - 662 / 2
        self.world.y -= y - 662 / 2
        self.player.x -= x - 662 / 2
        self.player.y -= y - 662 / 2
        for collider in self.colliders.rect_list:
            collider.x -= x - 662 / 2
            collider.y -= y - 662 / 2
    
    def draw(self, screen):            
        self.offset(self.camera)
        
        self.world.draw()
        self.player.draw()
        for collider in self.colliders.rect_list:
            screen.draw.rect(Rect((collider.x, collider.y), (collider.width, collider.height)), (255, 255, 255))
            
        self.offset((-self.camera[0], -self.camera[1]))
        
        self.camera = self.player.pos