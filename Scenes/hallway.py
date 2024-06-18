from managers import Scene
from Game import LevelManager, ColliderRect, Enemy, Player
from helper import Actor, ActorContainer

player = Player('characterb_59', pos=(300, 300), animation_frames={
            'up': ['characterb_93', 'characterb_94', 'characterb_95'],
            'down': ['characterb_57', 'characterb_58', 'characterb_59'],
            'right': ['characterb_81', 'characterb_82', 'characterb_83'],
            'left': ['characterb_69', 'characterb_70', 'characterb_71'],
            'idle': ['characterb_58']
        }, scale=2)


level_manager = LevelManager((662, 662), player)

levels = [
    {
        'world': Actor('floor1-open.png', scale=0.3),
        'colliders': [
            ColliderRect((-2160 * 0.3 / 2 + 81, -4320 * 0.3 / 2), (81, 4320 * 0.3)),
            ColliderRect((2160 * 0.3 / 2 - 81 * 2, -4320 * 0.3 / 2), (81, 4320 * 0.3)),
            ColliderRect((-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 3 + 10), (81, 81), fn=lambda: level_manager.load_level(levels[1])),
        ],
        'player_pos': (0, 0),
        'entities': ActorContainer()
    },
    {
        'world': Actor('stone_left.png', scale=662 / 1080),
        'colliders': [
            ColliderRect((-1080 * 662 / 1080 / 2, -1080 * 662 / 1080 / 2 - 81), (1080 * 662 / 1080, 81)),
            ColliderRect((-1080 * 662 / 1080 / 2, 1080 * 662 / 1080 / 2), (1080 * 662 / 1080, 81)),
            ColliderRect((-1080 * 662 / 1080 / 2 - 81, -1080 * 662 / 1080 / 2), (81, 1080 * 662 / 1080)),
            ColliderRect((1080 * 662 / 1080 / 2, -1080 * 662 / 1080 / 2), (81, 1080 * 662 / 1080)),
            ColliderRect((1080 * 662 / 1080 / 2 - 81, -1080 * 662 / 1080 / 2 + 81 * 4), (81, 81 * 2), fn=lambda: level_manager.load_level(levels[0])),
        ],
        'player_pos': (0, 0),
        'entities': ActorContainer(green_moth=Enemy('green_moth', pos=(331, 331), scale=0.15))
    }
]

class hallway(Scene):
    SCENE_NAME = 'hallway'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
        self.globals = kwargs
    
    def on_show(self):
        global level_manager, text
        
        level_manager.load_level(levels[0])
    
    def on_update(self, dt):
        level_manager.update(dt)
    
    def on_draw(self, screen):
        level_manager.draw(screen)