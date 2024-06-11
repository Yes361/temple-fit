from managers import Scene
from Game import LevelManager

class hallway(Scene):
    SCENE_NAME = 'hallway'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
        self.globals = kwargs
    
    def on_show(self):
        global level
        level = LevelManager()
    
    def on_update(self, dt):
        level.update(dt)
    
    def on_draw(self, screen):
        level.draw(screen)