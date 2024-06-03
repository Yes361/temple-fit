from pgzero.builtins import Actor
from typing import List

class ActorContainer:
    def __init__(self):
        self.actor_list: List[Actor] = []
    
    def offset_tiles(self, pos):
        dx, dy = pos
        for actor in self.actor_list:
            actor.x += dx
            actor.y += dy 
            
    def draw(self):
        for actor in self.actor_list:
            actor.draw()