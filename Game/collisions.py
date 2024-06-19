from typing import List, Tuple, Type
from dataclasses import dataclass
from abc import abstractmethod
from helper import Actor, Rect

    
class Collider(Actor):
    def __init__(self, *args, is_static=False, is_passable=False, fn=None, **kwargs):
        self.is_static = is_static
        self.is_passable = is_passable
        self.fn = fn
        super().__init__(*args, **kwargs)
    
    @abstractmethod
    def on_collide(self, collision):
        pass
        
class ColliderRect(Rect):
    def __init__(self, *args, is_static=True, is_passable=False, fn=None, **kwargs):
        self.is_static = is_static
        self.is_passable = is_passable
        self.fn = fn
        
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
            
        super().__init__(*args)
        
@dataclass
class CollisionData:
    colliderA: ColliderRect | Collider
    colliderB: ColliderRect | Collider

class Collisions:
    def __init__(self, *args):
        self.rect_list: List[Tuple[any, Type[Collider | ColliderRect]]] = [] if len(args) == 0 else args

    def add(self, collider: Type[Collider | ColliderRect]):
        self.rect_list.append(collider)
        
    def remove(self, collider: Type[Collider | ColliderRect]):
        self.rect_list = [rect for rect in self.rect_list if rect != collider]

    def resolve_entity_collisions(self, entity: Type[Collider]):
        for collider in self.rect_list:
            if Collisions.resolve_collision(entity, collider):
                entity.on_collide(CollisionData(entity, collider))
                if callable(collider.fn):
                    collider.fn()

    @staticmethod
    def resolve_collision(ColliderA: Type[Collider], ColliderB: Type[Collider | ColliderRect]):
        if not ColliderA.colliderect(ColliderB):
            return False
        
        if not (ColliderA.is_static or ColliderB.is_static):
            return True
            
        if ColliderA.is_passable or ColliderB.is_passable:
            return True
        
        overlap_x = min(ColliderA.right - ColliderB.left, ColliderB.right - ColliderA.left)
        overlap_y = min(ColliderA.bottom - ColliderB.top, ColliderB.bottom - ColliderA.top)

        if overlap_x < overlap_y:
            sign = 1 if ColliderA.centerx > ColliderB.centerx else -1
            
            if ColliderA.is_static:
                ColliderB.x -= overlap_x * sign
            else:
                ColliderA.x += overlap_x * sign
        else:
            sign = 1 if ColliderA.centery > ColliderB.centery else -1
            
            if ColliderA.is_static:
                ColliderB.y -= overlap_y * sign
            else:
                ColliderA.y += overlap_y * sign
        
        return True
