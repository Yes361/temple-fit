from managers import Scene, game_manager
from helper import Actor, ActorContainer


class StartScreen(Scene):
    SCENE_NAME = "outro"

    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_hide(self):
        pass

    def on_show(self):
        global intro, ui_elements

        intro = Actor("character-battle-sprite", pos=(331, 331))
        intro.play_gif

    def on_draw(self, screen):
        intro.draw()
        ui_elements.draw()

    def on_update(self, dt):
        intro.update(dt)
