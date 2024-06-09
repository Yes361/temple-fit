from managers import Scene, game_manager
from helper import Actor, ActorContainer
from Game import Button

All_actors = ActorContainer(
    Actors = ActorContainer(),
    UI_elements = ActorContainer(hidden=True)
)

Actors = All_actors.Actors
UI_elements = All_actors.UI_elements

def load_ui_elements():
    button = Button("play_button", (331, 340), on_click=None)
    button.scale = 0.1
        
    UI_elements.add("Start", button)

def load_actors():
    Actors.add("Intro", Actor("dragon_1"))
    load_ui_elements()

def handle_starting_screen_animation():
    intro = Actors.Intro
    intro.pos = (331, 331)
    intro.play_gif(
        "intro_card", iterations=1,
        on_finish=lambda: intro.play_gif(
            "intro", iterations=1,
            on_finish=show_starting_screen_menu
        )
    )

def show_starting_screen_menu():
    UI_elements.hidden = False

class StartScreen(Scene):
    SCENE_NAME = 'Start Screen'
    
    def __init__(self, *args, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_draw(self, screen):
        All_actors.draw(screen)

    def on_hide(self):
        All_actors.clear()

    def on_show(self):
        load_actors()
        handle_starting_screen_animation()

    def on_update(self, dt):
        Actors.update(dt)
        
    def on_mouse_down(self, pos, button):
        for actor in UI_elements:
            actor.on_click(pos, button)
            
    def on_key_down(self, key, unicode):
        pass