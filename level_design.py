from utils import list_actor_attributes
from typing import List, Tuple
from actor import Actor
import pandas as pd

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
        if not self.hidden:
            return
        
        for actor in self.actor_list:
            actor.draw()
            
    def __iter__(self):
        return iter(self.actor_list)