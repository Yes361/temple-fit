from managers import Scene, game_manager
from helper import Actor
from pgzero.builtins import music

# In all fairness, this could've been moved to start.py

outro = Actor("character-battle-sprite", pos=(331, 331))

class Outro(Scene):
    SCENE_NAME = "outro"

    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_show(self):
        
        music.stop()
        music.play('in_game')
            
        outro.play_gif('ending', iterations=1, on_finish=lambda: game_manager.switch_scene('Start Screen', False))

    def on_draw(self, screen):
        outro.draw()

    def on_update(self, dt):
        outro.update(dt)