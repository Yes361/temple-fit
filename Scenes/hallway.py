from managers import Scene
from Game import LevelManager, Text

class hallway(Scene):
    SCENE_NAME = 'hallway'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
        self.globals = kwargs
    
    def on_show(self):
        global level, text
        level = LevelManager(662, 662)
        # text = Text('Hello my name is Raiyan', (300, 300), 10, angle=45)
    
    def on_update(self, dt):
        level.update(dt)
    
    def on_draw(self, screen):
        level.draw(screen)