from managers import Scene, game_manager
from Game import LevelManager, ColliderRect, Entity, Player
from helper import Actor, ActorContainer, schedule
from pgzero.builtins import animate

freeze_frame = False

player = Player(
    "characterb_59",
    pos=(300, 300),
    animation_frames={
        "up": ["characterb_93", "characterb_94", "characterb_95"],
        "down": ["characterb_57", "characterb_58", "characterb_59"],
        "right": ["characterb_81", "characterb_82", "characterb_83"],
        "left": ["characterb_69", "characterb_70", "characterb_71"],
        "idle": ["characterb_58"],
    },
    scale=2,
    speed=3
)

ui = ActorContainer(tab = Actor('battle_scene_tab', scale=0.15))
ui.tab.topleft = (0, 662 - ui.tab.height)

def fade():
    global freeze_frame
    
    freeze_frame = True
    animate(player, opacity=0)
    animate(level_manager.world, opacity=0)
    animate(level_manager.entities, opacity=0)
    animate(ui, opacity=0)
    
    schedule(lambda: game_manager.switch_scene('Battle', prev=level_manager.current_level, room=0), 1)
    
def reset_opacity():
    global freeze_frame
    
    freeze_frame = False
    player.opacity = 255
    level_manager.world.opacity = 255
    level_manager.entities.opacity = 255
    ui.opacity = 255
    
class Enemy(Entity):
    def update(self, dt):
        global player
        self.direction = self.direction_to(player)
        self.move_in_direction(self.speed)
        
        if self.colliderect(player):
            fade()
            
        super().update(dt)


levels = {
    "floor": {
        "world": Actor("floor1-open.png", scale=0.3),
        "colliders": [
            ColliderRect((-2160 * 0.3 / 2 + 81, -4320 * 0.3 / 2), (81, 4320 * 0.3)),
            ColliderRect((2160 * 0.3 / 2 - 81 * 2, -4320 * 0.3 / 2), (81, 4320 * 0.3)),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room1", player_pos=(200, 0)),
            ),
        ],
        "entities": ActorContainer(),
    },
    "room1": {
        "world": Actor("stone_left.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-1080 * 662 / 1080 / 2, -1080 * 662 / 1080 / 2 - 81),
                (1080 * 662 / 1080, 81),
            ),
            ColliderRect(
                (-1080 * 662 / 1080 / 2, 1080 * 662 / 1080 / 2), (1080 * 662 / 1080, 81)
            ),
            ColliderRect(
                (-1080 * 662 / 1080 / 2 - 81, -1080 * 662 / 1080 / 2),
                (81, 1080 * 662 / 1080),
            ),
            ColliderRect(
                (1080 * 662 / 1080 / 2, -1080 * 662 / 1080 / 2), (81, 1080 * 662 / 1080)
            ),
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81 * 2),
                fn=lambda: level_manager.load_level("floor", player_pos=(0, 0)),
            ),
        ],
        "entities": ActorContainer(
            green_moth=Enemy("green_moth", pos=(-200, 0), scale=0.15)
        ),
    },
}

level_manager = LevelManager((662, 662), player, levels)
level_manager.load_level('floor', (0, 0))

class hallway(Scene):
    SCENE_NAME = "hallway"

    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
        self.globals = kwargs

    def on_show(self, room='floor', player_pos=(0, 0)):
        global level_manager, text

        if room != 'floor':
            levels[room]['entities'].clear()
        
        reset_opacity()
        level_manager.load_level(room, player_pos)        

    def on_update(self, dt):
        if not freeze_frame:
            level_manager.update(dt)

    def on_draw(self, screen):
        level_manager.draw(screen)
        ui.draw()
