from helper import ActorContainer, Actor, AbstractActor, Rect
from .collisions import Collisions
from .entity import Player
                
class LevelManager(AbstractActor):
    def __init__(self, dims, player: Player, levels, *args, **kwargs):
        self.entities = ActorContainer()
        self.player = player
        self.width, self.height = dims
        self.levels = levels
        self.current_level = list(levels.keys())[0]
        
        self.world: Actor = None
        self.camera = [0, 0]
        self.colliders = Collisions()
        self.total_offset = [0, 0]
    
    def _load_level(self, level, player_pos):
        self.current_level = level
        level = self.levels[level]
        
        self.world = level['world']
        self.world.pos = (0, 0)
        self.camera = [0, 0]
        self.colliders.rect_list = level['colliders']
        self.player.pos = player_pos
        self.entities = level['entities']
        
        self.offset_room((self.width / 2, self.height / 2))
    
    def load_level(self, level, player_pos):
        if self.world is not None:
            self.offset_room(self.total_offset)
        self.total_offset = [0, 0]
        
        self._load_level(level, player_pos)
    
    def update(self, dt):
        self.entities.update(dt)
        self.player.update(dt)
        self.colliders.resolve_entity_collisions(self.player)
        
    def offset_room(self, pos):
        dx, dy = pos
        self.total_offset = [self.total_offset[0] - dx, self.total_offset[1] - dy]
        self.entities.x -= dx
        self.entities.y -= dy
        self.player.x -= dx
        self.player.y -= dy
        self.world.x -= dx
        self.world.y -= dy
        for collider in self.colliders.rect_list:
            collider.x -= dx
            collider.y -= dy
            
    def set_camera(self, pos):
        self.camera = [pos[0] - self.width / 2, pos[1] - self.height / 2]
        x, y = self.camera
        x = max(self.world.left, min(x, self.world.left + self.world.width - self.width))
        y = max(self.world.top, min(y, self.world.top + self.world.height - self.height))
        self.camera = [x, y]
        
    def debug(self, screen):
        for collider in self.colliders.rect_list:
            screen.draw.rect(Rect((collider.x, collider.y), (collider.width, collider.height)), (255, 255, 255))
    
    def draw(self, screen):            
        
        self.offset_room(self.camera)
        
        self.world.draw()
        self.player.draw(screen)
        self.entities.draw(screen)
        self.debug(screen)
            
        self.offset_room((-self.camera[0], -self.camera[1]))
                    
        self.set_camera(self.player.pos)