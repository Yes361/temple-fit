from managers import Scene, game_manager
from helper import Actor, ActorContainer, Rect, CACHED_DIALOGUE
from Game import Button, Dialogue

class Narrative(Scene):
    SCENE_NAME = "Narrative"

    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_hide(self):
        pass

    def on_show(self):
        global backdrop, sprite, ui_elements, text_box, text_anim

        backdrop = Actor('narrative_backdrop')
        backdrop.resize((662, 662))
        backdrop.topleft = (0, 0)
        
        sprite = Actor('narrative_icon', pos=(70, 550))
        sprite.scale = 0.15
        text_box = Actor('narrative_text_box', pos=(370, 600))
        text_box.scale = 0.3
        text_box.resize((450, 95))
        
        text_anim = Dialogue(time_per_char=0.02, bounding_box=Rect((220, 565), (425, 75)), dialogue=CACHED_DIALOGUE['start'], color='black')
        ui_elements = ActorContainer()

    def on_draw(self, screen):
        backdrop.draw()
        sprite.draw()
        text_box.draw()
        text_anim.draw(screen)
        ui_elements.draw()

    def on_update(self, dt):
        ui_elements.update(dt)

    def on_mouse_down(self, pos, button):
        pass

    def on_key_down(self, key, unicode):
        if text_anim.is_complete():
            text_anim.next()