from managers import Scene, game_manager
from helper import Actor, ActorContainer
from Game import Button, Text

class Narrative(Scene):
    SCENE_NAME = "Narrative"

    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_hide(self):
        pass

    def on_show(self):
        global intro, ui_elements

        intro = Text('Hello My name is Raiyan', (331, 331), 2, tween='accelerate')
        ui_elements = ActorContainer()

    def on_draw(self, screen):
        intro.draw(screen)
        ui_elements.draw()

    def on_update(self, dt):
        intro.update(dt)
        ui_elements.update(dt)

    def on_mouse_down(self, pos, button):
        pass

    def on_key_down(self, key, unicode):
        pass