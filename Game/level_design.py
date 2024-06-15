from helper import ActorContainer, Actor, AbstractActor, Rect
from .collisions import Collisions, ColliderRect
from .entity import Entity, Player
from typing import List
        
class LevelManager(AbstractActor):
    def __init__(self, *args, **kwargs):
        self.entities = ActorContainer(player=Player('character.png', pos=(300, 300), animation_frames={
            'up': ['characterb_94', 'characterb_95', 'characterb_96'],
            'down': ['characterb_58', 'characterb_59', 'characterb_60'],
            'right': ['characterb_82', 'characterb_83', 'characterb_84'],
            'left': ['characterb_70', 'characterb_71', 'characterb_72'],
            'idle': ['characterb_59']
        }, scale=2))
        
        self.world: Actor = kwargs.get('world', Actor('hallway.png', pos=(331, 331), scale=0.2))
        
        self.camera = [self.entities.x, self.entities.y]
        self.colliders = Collisions(ColliderRect((self.world.topleft[0], self.world.topleft[1] - 100), (500, 100), is_static=True)) 
            
    def load_level(self, f):
        pass
    
    def save_level(self, f):
        pass
    
    def update(self, dt):
        self.entities.update(dt)
        self.colliders.resolve_entity_collisions(self.entities.player)
        
    def offset_room(self, pos):
        dx, dy = pos
        self.entities.x -= dx - 331
        self.entities.y -= dy - 331
        self.world.x -= dx - 331
        self.world.y -= dy - 331
        for collider in self.colliders.rect_list:
            collider.x -= dx - 331
            collider.y -= dy - 331
            
    def set_camera(self, pos):
        self.camera = pos
    
    def draw(self, screen):            
        
        self.offset_room(self.camera)
        
        self.world.draw()
        self.entities.draw()
        for collider in self.colliders.rect_list:
            screen.draw.rect(Rect((collider.x, collider.y), (collider.width, collider.height)), (255, 255, 255))
            
        self.offset_room((-self.camera[0], -self.camera[1]))
                    
        self.set_camera(self.entities.player.pos)