from managers import Scene, game_manager
from helper import Actor, ActorContainer, Rect, CACHED_DIALOGUE, CACHED_VOICELINES
from Game import Button, Dialogue
from pgzero.builtins import keyboard, keys

backdrop = Actor("narrative_backdrop", topleft=(0, 0), dims=(662, 662))

sprite = Actor("narrative_icon", pos=(100, 580))
sprite.scale = 1.5

text_box = Actor("narrative_text_box", pos=(370, 600), scale=0.3)
text_box.resize((450, 95))

ui_elements = ActorContainer()

next_button = Button(
    "arrow",
    pos=(550, 500),
    on_click=lambda x, y: game_manager.switch_scene("hallway", "fields"),
)
next_button.hidden = True


class Narrative(Scene):
    SCENE_NAME = "Narrative"

    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_hide(self):
        pass

    def on_show(self):
        global text_anim

        text_anim = Dialogue(
            sprite,
            {
                "MC": "character-battle-sprite",
                "Mayor": "narrative_icon",
                "Merchant": "narrative_icon",
            },
            CACHED_DIALOGUE["start"],
            voice_lines=CACHED_VOICELINES["mayorscene"],
            time_per_char=0.02,
            bounding_box=Rect((220, 565), (425, 75)),
            color="black",
        )

    def on_draw(self, screen):
        backdrop.draw()
        sprite.draw()
        text_box.draw()
        text_anim.draw(screen)
        ui_elements.draw()
        next_button.draw()

    def on_update(self, dt):
        ui_elements.update(dt)
        next_button.update(dt)

    def on_mouse_down(self, pos, button):
        next_button.on_click(pos, button)

    def on_key_down(self, key, unicode):
        if keyboard.SPACE:
            if not text_anim.is_complete():
                text_anim.next()
            else:
                text_anim.hidden = True
                sprite.hidden = True
                text_box.hidden = True
                next_button.hidden = False
