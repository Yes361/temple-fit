from helper import ActorContainer, Actor, AbstractActor, Rect
from managers import game_manager
from .collisions import Collisions, ColliderRect
from .entity import Entity, Player
from typing import List
        
class LevelManager(AbstractActor):
    def __init__(self, width, height, *args, **kwargs):
        self.entities = ActorContainer(player=Player('characterb_59', pos=(300, 300), animation_frames={
            'up': ['characterb_93', 'characterb_94', 'characterb_95'],
            'down': ['characterb_57', 'characterb_58', 'characterb_59'],
            'right': ['characterb_81', 'characterb_82', 'characterb_83'],
            'left': ['characterb_69', 'characterb_70', 'characterb_71'],
            'idle': ['characterb_58']
        }, scale=2))
        
        self.width, self.height = width, height
        
        self.world: Actor = Actor('hallway.png', pos=(width / 2, height / 2), scale=0.2)
        
        self.camera = [self.entities.x, self.entities.y]
        self.colliders = Collisions(
            ColliderRect((self.world.left, self.world.top - 100), (self.world.width, 100)),
            ColliderRect((self.world.left - 100, self.world.top), (100, self.world.height)),
            ColliderRect((self.world.left + self.world.width, self.world.top), (100, self.world.height)),
            ColliderRect((self.world.left, self.world.top + self.world.height), (self.world.width, 100)),
            ColliderRect((self.world.left + 50, self.world.top), (self.world.width - 50, 100), fn=lambda: game_manager.switch_scene('Battle'))
        ) 
    
    def update(self, dt):
        self.entities.update(dt)
        self.colliders.resolve_entity_collisions(self.entities.player)
        
    def offset_room(self, pos):
        dx, dy = pos
        self.entities.x -= dx
        self.entities.y -= dy
        self.world.x -= dx
        self.world.y -= dy
        for collider in self.colliders.rect_list:
            collider.x -= dx
            collider.y -= dy
            
    def set_camera(self, pos): # i sure do love writing good code !!!! (i wanna kms)
        self.camera = [pos[0] - self.width / 2, pos[1] - self.height / 2]
        x, y = self.camera
        if y < self.world.top:
            self.camera = [x, self.world.top]
        if y > self.world.top + self.world.height - self.height:
            self.camera = [x, self.world.top + self.world.height - self.height]
        
    def debug(self, screen):
        for collider in self.colliders.rect_list:
            screen.draw.rect(Rect((collider.x, collider.y), (collider.width, collider.height)), (255, 255, 255))
        
    
    def draw(self, screen):            
        
        self.offset_room(self.camera)
        
        self.world.draw()
        self.entities.draw()
        self.debug(screen)
            
        self.offset_room((-self.camera[0], -self.camera[1]))
                    
        self.set_camera(self.entities.player.pos)