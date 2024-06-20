"""
This file implements the scene for the beginning dialogue with the mayor
"""

from managers import Scene, game_manager
from helper import Actor, ActorContainer, Rect, Music, CACHED_DIALOGUE, CACHED_VOICELINES
from Game import Button, Dialogue
from pgzero.builtins import keyboard

backdrop = Actor("narrative_backdrop", topleft=(0, 0), dims=(662, 662))

sprite = Actor("narrative_icon", pos=(100, 580))
sprite.scale = 1.5

# Set up the text box for displaying dialogue
text_box = Actor("narrative_text_box", pos=(370, 600), scale=0.3)
text_box.resize((450, 95))

# Container for holding UI elements
ui_elements = ActorContainer()

# Set up the next button for advancing the scene
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
        self._reset = False

    def on_hide(self):
        pass

    def on_show(self):
        global text_anim
        
        if not Music.is_playing('in_game'):
            Music.stop()
            Music.play('in_game')

        text_anim = Dialogue(
            sprite,
            {
                "MC": "character-battle-sprite",
                "Mayor": "narrative_icon",
            },
            CACHED_DIALOGUE["start"],
            voice_lines=CACHED_VOICELINES["mayorscene"],
            time_per_char=0.02,
            bounding_box=Rect((220, 565), (425, 75)),
            color="black",
        )
        
        self._reset = True

    def on_draw(self, screen):
        backdrop.draw()
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
            # Advance the text if the space bar is pressed
            if not text_anim.is_complete():
                text_anim.next()
            else:
                # Hide the text animation and text box, show the next button
                text_anim.hidden = True
                text_box.hidden = True
                next_button.hidden = False

    def reset(self):
        if self._reset:
            text_anim.hidden = False
            text_box.hidden = False
            next_button.hidden = True