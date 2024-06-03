from pgzero.builtins import Actor
from utils import list_actor_attributes, create_actor
from typing import List, Tuple
import pandas as pd

class ActorContainer:
    def __init__(self):
        self.actor_list: List[Actor] = []
  
    def add_actor(self, *args, **kwargs):
        actor = create_actor(*args, **kwargs)
        self.actor_list.append(actor)
        return actor
    
    def remove_actor(self, actor):
        self.actor_list.remove(actor)
    
    def save_file(self, f):
        fieldnames = []
        for actor in self.actor_list:
            fieldnames.append(list_actor_attributes(actor, ['image', 'pos']))
        
        df = pd.DataFrame(fieldnames)
        df.to_pickle(f)
    
    def read_file(self, f):
        df = pd.read_pickle(f).T                        
        fieldnames = df.to_dict()
        
        for actor in fieldnames.values():
            self.add_actor(**actor)
            
    def offset_tiles(self, pos: Tuple[int, int]):
        dx, dy = pos
        for actor in self.actor_list:
            actor.x += dx
            actor.y += dy
            
    def draw(self):
        for actor in self.actor_list:
            actor.draw()