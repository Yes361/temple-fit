from managers import Scene, game_manager
from helper import Actor, ActorContainer, Music
from pgzero.builtins import animate
from Game import Button
from . import config
import sys

player_button_pressed = False


def fade_ui_elements(group: ActorContainer):
    for elm in group:
        if not elm.hidden:
            elm.animate_targets(tween="bounce_end", pos=(elm.x, -50))

    group.hidden = False
    group.opacity = 0
    animate(group, opacity=255)


def outro_sequence():
    ui_elements.hidden = True
    intro.play_gif("outro_card", iterations=1, on_finish=lambda: sys.exit(0))


def set_difficulty(mode):
    config.set_difficulty(mode)
    game_manager.switch_scene("Narrative")


class StartScreen(Scene):
    SCENE_NAME = "Start Screen"

    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_hide(self):
        pass

    def on_show(self, play_intro=True):
        global intro, ui_elements, play_button

        def press_player_button():
            global player_button_pressed
            if not player_button_pressed:
                player_button_pressed = True
                fade_ui_elements(difficulty)

        game_manager.reset_scenes()

        Music.stop
        Music.play("menu")

        intro = Actor("character-battle-sprite", pos=(331, 331))

        difficulty = ActorContainer(
            easy=Button(
                "easy.png",
                pos=(331, 490),
                on_click=lambda key, unicode: set_difficulty("easy"),
                scale=0.1,
            ),
            middle=Button(
                "medium.png",
                pos=(331, 530),
                on_click=lambda key, unicode: set_difficulty("medium"),
                scale=0.1,
            ),
            hard=Button(
                "hard.png",
                pos=(331, 570),
                on_click=lambda key, unicode: set_difficulty("hard"),
                scale=0.1,
            ),
            hidden=True,
        )

        ui_elements = ActorContainer(
            narrative_button=Button(
                "play_button.png",
                pos=(331, 400),
                on_click=lambda key, unicode: press_player_button(),
                scale=0.1,
            ),
            exit_button=Button(
                "exit", pos=(331, 450), on_click=lambda key, unicode: outro_sequence(), scale=0.1
            ),
            difficulty_group=difficulty,
            hidden=True,
        )

        if play_intro:
            intro.play_gif(
                "intro_card",
                iterations=1,
                on_finish=lambda: intro.play_gif(
                    "intro",
                    iterations=1,
                    on_finish=lambda: fade_ui_elements(ui_elements),
                ),
            )
        else:
            intro.image = "intro_frame_84"
            ui_elements.hidden = False

    def on_draw(self, screen):
        intro.draw()
        ui_elements.draw()

    def on_update(self, dt):
        intro.update(dt)
        ui_elements.update(dt)

    def on_mouse_down(self, pos, button):
        ui_elements.on_click(pos, button)

    def reset(self):
        global player_button_pressed
        player_button_pressed = False
