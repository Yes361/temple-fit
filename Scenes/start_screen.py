from managers import Scene, input_manager, scene_manager
from helper import Actor, ActorContainer
from Game import Button

Actors = ActorContainer()

def load_actors():
    Actors.add("Intro-Animation", Actor("dragon_1"))
    
    button = Button("play_button", (331, 340), on_hover=None)
    button.scale = 0.1
    button.hidden = True
    button.Bind(input_manager, StartScreen.SCENE_NAME)
    
    Actors.add("Start-Screen-Button", button)


def handle_starting_screen_animation():
    Actors['Intro-Animation'].pos = (331, 331)
    Actors["Intro-Animation"].play_gif(
        "intro_card", iterations=1,
        on_finish=lambda: Actors["Intro-Animation"].play_gif(
            "intro", iterations=1,
            on_finish=show_starting_screen_menu
        )
    )

def show_starting_screen_menu():
    Actors['Start-Screen-Button'].hidden = False

class StartScreen(Scene):
    SCENE_NAME = 'Start Screen'
    
    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME, self)

    def on_draw(self, screen):
        Actors.draw(screen)

    def on_hide(self):
        Actors.clear()

    def on_show(self):
        load_actors()
        handle_starting_screen_animation()
        input_manager.set_group(self.SCENE_NAME)

    def on_update(self, dt):
        Actors.update(dt)
