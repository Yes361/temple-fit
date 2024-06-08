from managers import Scene, input_manager, scene_manager
from gui import Button
from helper import Actor, ActorContainer
from constants import Constants

class StartScreen(Scene):
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        super().__init__('Start Screen', self)
        
    def on_draw(self, screen):
        return super().on_draw(screen)
    
    def on_hide(self):
        return super().on_hide()
    
    def on_show(self):
        self.load_actors()
        
        self.Actors['intro'].play_gif(
            "intro_card", 1,
            on_finish=lambda: self.Actors['intro'].play_gif(
                "intro", 1,
                on_finish=self.start_screen
            ),
        )
        super().on_show()
    
    def on_update(self, dt):
        super().on_update(dt)
    
    def load_actors(self):
        self.Actors.add_actor('intro', Actor("dragon_3.png", pos=(self.WIDTH / 2, self.HEIGHT / 2)))
        self.Actors['intro'].fps = 24
        self.Actors.add_actor('StartScreen', Button('play_button.png', (331, 331), on_click=lambda: scene_manager.switch_scene('Camera'), hidden=True))
        self.Actors['StartScreen'].scale = 0.1
        self.Actors['StartScreen'].Bind(input_manager, self.scene_name)
        input_manager.subscribe(Constants.KEY_DOWN, self.hm, 'Global')
        
    def hm(self, x, y):
        print(x, y)
        self.Actors['intro'].skip_gif()

    def start_screen(self):
        self.Actors['intro'].image = "intro_frame_84.png"
        self.Actors['StartScreen'].hidden = False
        input_manager.set_group('Start Screen')