from utils import ActorContainer, Actor

class Tile(Actor):
    pass

class World(ActorContainer):
    def __init__(self, tile_size):
        self.tile_size = tile_size
        super().__init__()
    
    def add_tile(self, image, pos, **kwargs):
        x, y = pos
        tile = Actor(image, (x * self.tile_size, y * self.tile_size), r = x, c = y, **kwargs)
        tile.resize((self.tile_size, self.tile_size))
        self.add_actor(tile)
        
        
class LevelManager:
    def __init__(self):
        pass
    
    def load_level(self, f):
        pass
    
    def save_level(self, f):
        pass