from managers import Scene, game_manager
from helper import Actor, ActorContainer
from pgzero.builtins import animate
from Game import Button, camera


def fade_ui_elements():
    ui_elements.hidden = False
    ui_elements.opacity = 0
    animate(ui_elements, opacity=255)
    for elm in ui_elements:
        elm.animate_starting_targets(tween='bounce_end', pos=(elm.x, -50))


class StartScreen(Scene):
    SCENE_NAME = "Start Screen"

    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_hide(self):
        pass

    def on_show(self, play_intro=True):
        global intro, ui_elements

        intro = Actor("character-battle-sprite", pos=(331, 331))

        ui_elements = ActorContainer(
            narrative_button=Button(
                "play_button.png",
                pos=(331, 400),
                on_click=lambda x, y: game_manager.switch_scene('Narrative'),
                scale=0.1,
            ),
            hidden=True,
        )

        if play_intro:
            intro.play_gif(
                "intro_card",
                iterations=1,
                on_finish=lambda: intro.play_gif(
                    "intro", iterations=1, on_finish=fade_ui_elements
                ),
            )
        
    def on_draw(self, screen):
        intro.draw()
        ui_elements.draw()

    def on_update(self, dt):
        intro.update(dt)
        ui_elements.update(dt)

    def on_mouse_down(self, pos, button):
        if ui_elements.hidden:
            return

        for actor in ui_elements:
            actor.on_click(pos, button)

    def on_key_down(self, key, unicode):
        intro.skip_gif()