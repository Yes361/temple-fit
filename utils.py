from pgzero.builtins import Actor
from typing import List, Any, Tuple
import pygame

def list_actor_attributes(actor: Actor, field_name: List[str]) -> dict[str, Any]:
    """
    @param actor
    @param field_name The desired fields
    @return: A dictionary containing the values of the desired fields
    """
    field = {}
    for name in field_name:
        field[name] = getattr(actor, name)
    return field

def require_kwargs(fields, kwargs, error_msg = '%s is required'):
    """
    @raises An error if a required field was not passed
    """
    for field in fields:
        if field not in kwargs:
            raise Exception(error_msg % field)

class Actor(Actor):
    """
    Revised Version of Actor Class
    
    Now supports resizing, passing custom properties at initialization, update(dt), and reset()
    """
    EXPECTED_INIT_KWARGS = set(['pos', 'topleft', 'bottomleft', 'topright', 'bottomright',
    'midtop', 'midleft', 'midbottom', 'midright', 'center'])
    
    def __init__(self, *args, **kwargs):
        self.hidden = False
        
        keys = list(kwargs.keys())
        for key in keys:
            if key not in Actor.EXPECTED_INIT_KWARGS:
                setattr(self, key, kwargs[key])
                kwargs.pop(key)

        super().__init__(*args, **kwargs)
        
    def resize(self, dimensions):
        self._surf = pygame.transform.scale(self._surf, dimensions)
    
    def draw(self, *args, **kwargs):
        if not self.hidden:
            super().draw()
            
    def update(self, dt):
        pass
    
    def reset(self):
        pass

class ActorContainer:
    """
    Actor Container is a list of Actors - Similar to Group() in CMU Academy
    """
    def __init__(self, *args, **kwargs):
        self.actor_list = list(*args, **kwargs) or []
        self.hidden = False
  
    def add_actor(self, actor):
        self.actor_list.append(actor)
        return actor
    
    def remove_actor(self, actor):
        self.actor_list.remove(actor)
        
    # TODO: z-index shenanigans
    # def set_actor_zindex(self, actor):
    #     pass
        
    def colliderect(self, other_actor):
        for actor in self.actor_list:
            if actor.colliderect(other_actor):
                return True
        return False

    def draw(self, *args, **kwargs):
        if self.hidden:
            return
        
        for actor in self.actor_list:
            actor.draw(*args, **kwargs)
    
    def update(self, dt):
        for actor in self.actor_list:
            actor.update(dt)
            
    def __iter__(self):
        return iter(self.actor_list)