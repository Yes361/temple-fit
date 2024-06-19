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
    speed=3,
)

ui = ActorContainer(tab=Actor("battle_scene_tab", scale=0.15))
ui.tab.topleft = (0, 662 - ui.tab.height)
counter = 0


def fade():
    global freeze_frame

    freeze_frame = True
    animate(player, opacity=0)
    animate(level_manager.world, opacity=0)
    animate(level_manager.entities, opacity=0)
    animate(ui, opacity=0)


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
        if self.hidden:
            return

        self.direction = self.direction_to(player)
        self.move_in_direction(self.speed)

        if self.colliderect(player):
            fade()
            schedule(
                lambda: game_manager.switch_scene("Battle", next=self.next, room=0),
                1,
            )

        super().update(dt)


class Item(Entity):
    def update(self, dt):
        global player, counter
        if self.hidden:
            return

        if self.colliderect(player):
            levels[level_manager.current_level]["entities"].scroll.hidden = True
            counter += 1


left_rooms = [
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
    ColliderRect((1080 * 662 / 1080 / 2 - 81, -1080 * 662 / 1080 / 2), (81, 82 * 4)),
    ColliderRect(
        (1080 * 662 / 1080 / 2 - 81, -1080 * 662 / 1080 / 2 + 82 * 5), (81, 82 * 4)
    ),
]

right_rooms = [
    ColliderRect(
        (-1080 * 662 / 1080 / 2, -1080 * 662 / 1080 / 2 - 81),
        (1080 * 662 / 1080, 81),
    ),
    ColliderRect(
        (-1080 * 662 / 1080 / 2, 1080 * 662 / 1080 / 2),
        (1080 * 662 / 1080, 81),
    ),
    ColliderRect(
        (-1080 * 662 / 1080 / 2 - 81, -1080 * 662 / 1080 / 2),
        (81, 1080 * 662 / 1080),
    ),
    ColliderRect(
        (1080 * 662 / 1080 / 2, -1080 * 662 / 1080 / 2),
        (81, 1080 * 662 / 1080),
    ),
    ColliderRect((-1080 * 662 / 1080 / 2, -1080 * 662 / 1080 / 2), (81, 82 * 4)),
    ColliderRect(
        (-1080 * 662 / 1080 / 2, -1080 * 662 / 1080 / 2 + 82 * 5), (81, 82 * 4)
    ),
]


def next_floor():
    global counter
    if counter >= 8:
        level_manager.load_level("floor2")
        counter = 0


levels = {
    "tutorial_start": {
        "world": Actor("start_tutorial", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-662 / 2, -662 / 2 - 81),
                (662, 81),
            ),
            ColliderRect(
                (-662 / 2, 662 / 2),
                (662, 81),
            ),
            ColliderRect(
                (-662 / 2 - 81, -662 / 2),
                (81, 662),
            ),
            ColliderRect(
                (662 / 2, -662 / 2),
                (81, 662),
                fn=lambda: level_manager.load_level(
                    "tutorial_hallway", player_pos=(0, 0)
                ),
            ),
        ],
        "entities": ActorContainer(),
    },
    "tutorial_hallway": {
        "world": Actor("hallway_tutorial", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-662 / 2, -662 / 2 - 81),
                (662, 81),
            ),
            ColliderRect(
                (-662 / 2, 662 / 2),
                (662, 81),
            ),
            ColliderRect(
                (-662 / 2 - 81, -662 / 2),
                (81, 662),
            ),
            ColliderRect(
                (662 / 2, -662 / 2),
                (81, 662),
                fn=lambda: level_manager.load_level("tutorial_boss", player_pos=(0, 0)),
            ),
        ],
        "entities": ActorContainer(),
    },
    "tutorial_boss": {
        "world": Actor("boss_tutorial", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-662 / 2, -662 / 2 - 81),
                (662, 81),
            ),
            ColliderRect(
                (-662 / 2, 662 / 2),
                (662, 81),
            ),
            ColliderRect(
                (-662 / 2 - 81, -662 / 2),
                (81, 662),
            ),
            ColliderRect(
                (662 / 2, -662 / 2),
                (81, 662),
            ),
        ],
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=(-200, 0), scale=0.15, next="fields")
        ),
    },
    "fields": {
        "world": Actor("sageme", scale=662 / 208),
        "colliders": [
            ColliderRect(
                (-662 / 2, -960 / 2 * 662 / 208 + 400),
                (662, 10),
                fn=lambda: level_manager.load_level("floor", player_pos=(0, 0)),
            ),
            ColliderRect(
                (662 / 2, -960 / 2 * 662 / 208),
                (10, 960 * 662 / 208),
                fn=lambda: level_manager.load_level("floor", player_pos=(0, 0)),
            ),
            ColliderRect(
                (-662 / 2, 960 / 2 * 662 / 208),
                (662, 10),
                fn=lambda: level_manager.load_level("floor", player_pos=(0, 0)),
            ),
            ColliderRect(
                (-662 / 2 + 10, -960 / 2),
                (10, 960 * 662 / 208),
                fn=lambda: level_manager.load_level("floor", player_pos=(0, 0)),
            ),
        ],
        "entities": ActorContainer(),
    },
    "floor": {
        "world": Actor("floor1-closed.png", scale=0.3),
        "colliders": [
            ColliderRect((-2160 * 0.3 / 2 + 81, -4320 * 0.3 / 2), (81, 4320 * 0.3)),
            ColliderRect((2160 * 0.3 / 2 - 81 * 2, -4320 * 0.3 / 2), (81, 4320 * 0.3)),
            ColliderRect(
                (-2160 * 0.3 / 2 + 81, -4320 * 0.3 / 2 + 80),
                (4320 * 0.3, 10),
                fn=next_floor,
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 83, -4320 * 0.3 / 2 + 80 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room1", player_pos=(0, 0)),
                # fn=lambda: print('room1')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room2", player_pos=(0, 0)),
                # fn=lambda: print('room2')
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room3", player_pos=(0, 0)),
                # fn=lambda: print('room3')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room4", player_pos=(0, 0)),
                # fn=lambda: print('room4')
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room5", player_pos=(0, 0)),
                # fn=lambda: print('room5')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 3, -4320 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room6", player_pos=(0, 0)),
                # fn=lambda: print('room6')
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 14 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room7", player_pos=(0, 0)),
                # fn=lambda: print('room7')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 14 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room8", player_pos=(0, 0)),
                # fn=lambda: print('room8')
            ),
        ],
        "entities": ActorContainer(),
    },
    "room1": {
        "world": Actor("stone_left.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor", player_pos=(-84, -370)),
            ),
        ]
        + left_rooms,
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=(-200, 0), scale=0.15, next="floor"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room2": {
        "world": Actor("netherite_right.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor", player_pos=(96, -370)),
            ),
        ]
        + right_rooms,
        "entities": ActorContainer(
            enemy=Enemy("red_hood", pos=(+200, 0), scale=0.15, next="floor"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room3": {
        "world": Actor("wood_left.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor", player_pos=(-84, 48)),
            ),
        ]
        + left_rooms,
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=(-200, 0), scale=0.15, next="floor"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room4": {
        "world": Actor("stone_right.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor", player_pos=(96, 48)),
            ),
        ]
        + right_rooms,
        "entities": ActorContainer(
            enemy=Enemy("red_hood", pos=(+200, 0), scale=0.15, next="floor"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room5": {
        "world": Actor("purple_left.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor", player_pos=(-84, 219)),
            ),
        ]
        + left_rooms,
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=(-200, 0), scale=0.15, next="floor"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room6": {
        "world": Actor("purple_right.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor", player_pos=(96, 219)),
            ),
        ]
        + right_rooms,
        "entities": ActorContainer(
            enemy=Enemy("red_hood", pos=(+200, 0), scale=0.15, next="floor"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room7": {
        "world": Actor("netherite_left.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor", player_pos=(-84, 501)),
            ),
        ]
        + left_rooms,
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=(-200, 0), scale=0.15, next="floor"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room8": {
        "world": Actor("wood_right.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor", player_pos=(96, 501)),
            ),
        ]
        + right_rooms,
        "entities": ActorContainer(
            enemy=Enemy("red_hood", pos=(+200, 0), scale=0.15, next="floor"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "floor2": {
        "world": Actor("floor2", scale=0.3),
        "colliders": [
            ColliderRect((-2160 * 0.3 / 2 + 81, -3500 * 0.3 / 2), (81, 3500 * 0.3)),
            ColliderRect((2160 * 0.3 / 2 - 81 * 2, -3500 * 0.3 / 2), (81, 3500 * 0.3)),
            ColliderRect(
                (-2160 * 0.3 / 2 + 81, -3500 * 0.3 / 2 + 80),
                (3500 * 0.3, 10),
                fn=next_floor,
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 83, -3500 * 0.3 / 2 + 80 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room1-2", player_pos=(0, 0)),
                # fn=lambda: print('room1')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -3500 * 0.3 / 2 + 81 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room2-2", player_pos=(0, 0)),
                # fn=lambda: print('room2')
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -3500 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room3-2", player_pos=(0, 0)),
                # fn=lambda: print('room3')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -3500 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room4-2", player_pos=(0, 0)),
                # fn=lambda: print('room4')
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -3500 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room5-2", player_pos=(0, 0)),
                # fn=lambda: print('room5')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 3, -3500 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room6-2", player_pos=(0, 0)),
                # fn=lambda: print('room6')
            )
        ],
        "entities": ActorContainer(),
    },
    "room1-2": {
        "world": Actor("smooth_left.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor2", player_pos=(-84, -370)),
            ),
        ]
        + left_rooms,
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=(-200, 0), scale=0.15, next="floor2"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room2-2": {
        "world": Actor("brick_right.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor2", player_pos=(96, -370)),
            ),
        ]
        + right_rooms,
        "entities": ActorContainer(
            enemy=Enemy("red_hood", pos=(+200, 0), scale=0.15, next="floor2"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room3-2": {
        "world": Actor("block_left.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor2", player_pos=(-84, 48)),
            ),
        ]
        + left_rooms,
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=(-200, 0), scale=0.15, next="floor2"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room4-2": {
        "world": Actor("smooth_right.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor2", player_pos=(96, 48)),
            ),
        ]
        + right_rooms,
        "entities": ActorContainer(
            enemy=Enemy("red_hood", pos=(+200, 0), scale=0.15, next="floor2"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room5-2": {
        "world": Actor("brick_left.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor2", player_pos=(-84, 219)),
            ),
        ]
        + left_rooms,
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=(-200, 0), scale=0.15, next="floor2"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    "room6-2": {
        "world": Actor("block_right.png", scale=662 / 1080),
        "colliders": [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level("floor2", player_pos=(96, 219)),
            ),
        ]
        + right_rooms,
        "entities": ActorContainer(
            enemy=Enemy("red_hood", pos=(+200, 0), scale=0.15, next="floor22"),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    },
    
}

level_manager = LevelManager((662, 662), player, levels)
level_manager.load_level("floor", (0, 0))


class hallway(Scene):
    SCENE_NAME = "hallway"

    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
        self.globals = kwargs

    def on_show(self, room="fields", player_pos=(0, 0)):
        global level_manager, text

        reset_opacity()

        if room == "fields":
            level_manager.load_level("fields", player_pos=(0, 1000))
        elif room == "tutorial":
            level_manager.load_level("tutorial_start", player_pos)
        elif level_manager.prev_level.startswith("room"):
            levels[room]["entities"].enemy.hidden = True
            level_manager.load_level(room, player_pos)
        else:
            level_manager.load_level(room)

    def on_update(self, dt):
        if not freeze_frame:
            level_manager.update(dt)

        if counter >= 8:
            levels["floor"]["world"].image = "floor1-open"

    def on_draw(self, screen):
        global counter

        level_manager.draw(screen)
        ui.draw()

        screen.draw.text(f"{counter}", (20, 630))
