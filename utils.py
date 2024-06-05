from pgzero.builtins import Actor
from typing import List, Any, Tuple
import pandas as pd

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

def require_kwargs(fields, kwargs):
    """
    END ME
    """
    for field in fields:
        if field not in kwargs:
            raise Exception(f'{field} is required.')

class Actor(Actor):
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
    
    def draw(self):
        if not self.hidden:
            super().draw()
            
    def update(self, dt=0):
        pass
    
    def reset(self):
        pass

class ActorContainer:
    """
    
    """
    def __init__(self, actor_list=[]):
        self.actor_list = actor_list
        self.hidden = False
  
    def add_actor(self, *args, **kwargs):
        actor = Actor(*args, **kwargs)
        self.actor_list.append(actor)
        return actor
    
    def remove_actor(self, actor):
        self.actor_list.remove(actor)
    
    def save_file(self, f: str):
        """
        saves the file
        """
        fieldnames = []
        for actor in self.actor_list:
            fieldnames.append(list_actor_attributes(actor, ['image', 'pos']))
        
        df = pd.DataFrame(fieldnames)
        df.to_pickle(f)
    
    def read_file(self, f: str):
        """
        reads the file
        """
        df = pd.read_pickle(f).T                        
        fieldnames = df.to_dict()
        
        for actor in fieldnames.values():
            self.add_actor(**actor)
            
    def colliderect(self, other_actor):
        for actor in self.actor_list:
            if actor.colliderect(other_actor):
                return True
        return False
            
    def offset_tiles(self, pos: Tuple[int, int]):
        dx, dy = pos
        for actor in self.actor_list:
            actor.x += dx
            actor.y += dy
            
    def draw(self):
        if self.hidden:
            return
        
        for actor in self.actor_list:
            actor.draw()
    
    def update(self, dt):
        for actor in self.actor_list:
            actor.update(dt)
            
    def __iter__(self):
        return iter(self.actor_list)