from managers import Scene, game_manager
from Game import LevelManager, ColliderRect, Entity, Player, Dialogue
from helper import (
    Actor,
    ActorContainer,
    schedule,
    Rect,
    CACHED_DIALOGUE,
    CACHED_VOICELINES,
)
from pgzero.builtins import animate, keyboard

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

ui = Actor("battle_scene_tab", scale=0.15)
ui.topleft = (0, 662 - ui.height)
counter = 0

text_anim = None
sprite = None
scroll_counter_img = Actor("scroll", pos=(ui.width / 2, 662 - ui.height / 4))
scroll_counter_img.scale = 0.15


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
                lambda: game_manager.switch_scene("Battle", next=self.next, room=0, enemy_image=self.image, scale=self.scale),
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


def next_floor(current_floor):
    global counter
    if counter >= 8:
        if current_floor == "floor":
            level_manager.load_level("floor2")
        elif current_floor == "floor2":
            game_manager.switch_scene("Battle")
        counter = 0


def create_room(name, world, floor, next_player_pos, left_side):
    if left_side:
        colliders = [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level(floor, player_pos=next_player_pos),
            )
        ] + left_rooms
        enemy_spawn = (-200, 0)
    else:
        colliders = [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level(floor, player_pos=next_player_pos),
            )
        ] + right_rooms
        enemy_spawn = (200, 0)
    return {
        "world": Actor(world, scale=662 / 1080),
        "colliders": colliders,
        "entities": ActorContainer(
            enemy=Enemy("green_moth", pos=enemy_spawn, scale=0.15, next=name),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    }


def load_tutorial():
    global text_anim, sprite
    sprite = Actor("narrative_icon", pos=(130, 560))
    sprite.scale = 1
    text_anim = Dialogue(
        sprite,
        {
            "MC": "character-battle-sprite",
            "Fairy": "fairy",
        },
        CACHED_DIALOGUE["tutorial"],
        voice_lines=CACHED_VOICELINES["tutorial"],
        time_per_char=0.02,
        bounding_box=Rect((220, 565), (425, 75)),
        color="black",
    )

    level_manager.load_level("tutorial_start", (0, 0))

def load_floor3():
    global text_anim, sprite
    
    level_manager.load_level("floor3", player_pos=(0, 0))
    sprite = Actor("narrative_icon", pos=(100, 580))
    sprite.scale = 1.5
    
    text_anim = Dialogue(
        sprite,
        {
            "MC": "character-battle-sprite",
            "OM": "narrative_icon",
        },
        CACHED_DIALOGUE["outro"],
        voice_lines=CACHED_VOICELINES["oms"],
        time_per_char=0.02,
        bounding_box=Rect((220, 565), (425, 75)),
        color="white",
        on_finish=lambda: game_manager.switch_scene('Battle', next='outro', enemy_image='dragon')
    )


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
                    "tutorial_hallway", player_pos=(-280, 0)
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
                fn=lambda: level_manager.load_level("tutorial_boss", player_pos=(-280, 0)),
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
            enemy=Enemy("green_moth", pos=(200, 0), scale=0.15, next="floor")
        ),
    },
    "fields": {
        "world": Actor("sageme", scale=662 / 208),
        "colliders": [
            ColliderRect(
                (-662 / 2, -960 / 2 * 662 / 208 + 400),
                (662, 10),
                fn=load_tutorial,
            ),
            ColliderRect(
                (662 / 2, -960 / 2 * 662 / 208),
                (10, 960 * 662 / 208),
                fn=load_tutorial,
            ),
            ColliderRect(
                (-662 / 2, 960 / 2 * 662 / 208),
                (662, 10),
                fn=load_tutorial,
            ),
            ColliderRect(
                (-662 / 2 + 10, -960 / 2),
                (10, 960 * 662 / 208),
                fn=load_tutorial,
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
                fn=lambda: level_manager.load_level("floor2", player_pos=(-100, 0)),
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 83, -4320 * 0.3 / 2 + 80 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room1", player_pos=(100, 0)),
                # fn=lambda: print('room1')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room2", player_pos=(-100, 0)),
                # fn=lambda: print('room2')
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room3", player_pos=(100, 0)),
                # fn=lambda: print('room3')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room4", player_pos=(-100, 0)),
                # fn=lambda: print('room4')
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room5", player_pos=(100, 0)),
                # fn=lambda: print('room5')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 3, -4320 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room6", player_pos=(-100, 0)),
                # fn=lambda: print('room6')
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 14 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room7", player_pos=(100, 0)),
                # fn=lambda: print('room7')
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 14 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room8", player_pos=(-100, 0)),
                # fn=lambda: print('room8')
            ),
        ],
        "entities": ActorContainer(),
    },
    "room1": create_room("room1", "stone_left", "floor", (-84, -370), True),
    "room2": create_room("room2", "netherite_right", "floor", (96, -370), False),
    "room3": create_room("room3", "wood_left", "floor", (-84, 48), True),
    "room4": create_room("room4", "stone_right", "floor", (96, 48), False),
    "room5": create_room("room5", "purple_left", "floor", (-84, 219), True),
    "room6": create_room("room6", "purple_right", "floor", (96, 219), False),
    "room7": create_room("room7", "netherite_left", "floor", (-84, 501), True),
    "room8": create_room("room8", "wood_right", "floor", (96, 501), False),
    "floor2": {
        "world": Actor("floor2", scale=0.3),
        "colliders": [
            ColliderRect((-2160 * 0.3 / 2 + 81, -3500 * 0.3 / 2), (81, 3500 * 0.3)),
            ColliderRect((2160 * 0.3 / 2 - 81 * 2, -3500 * 0.3 / 2), (81, 3500 * 0.3)),
            ColliderRect(
                (-2160 * 0.3 / 2 + 81, 3500 * 0.3 / 2 - 80),
                (3500 * 0.3, 10),
                fn=load_floor3,
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
            ),
        ],
        "entities": ActorContainer(),
    },
    "room1-2": create_room("room1-2", "smooth_left", "floor2", (-84, -370), True),
    "room2-2": create_room("room2-2", "brick_right", "floor2", (96, -370), False),
    "room3-2": create_room("room3-2", "block_left", "floor2", (-84, 48), True),
    "room4-2": create_room("room4-2", "smooth_right", "floor2", (96, 48), False),
    "room5-2": create_room("room5-2", "brick_left", "floor2", (-84, 219), True),
    "room6-2": create_room("room6-2", "block_right", "floor2", (96, 219), False),
    'floor3': {
        'world': Actor('final_room', scale=0.3),
        'colliders': [
            ColliderRect((-2300 / 2 * 0.3, -1300 / 2 * 0.3 - 10), (2300 * 0.3, 10)),
            ColliderRect((2300 / 2 * 0.3, -1300 / 2 * 0.3), (10, 1300 * 0.3)),
            ColliderRect((-2300 / 2 * 0.3, 1300 / 2 * 0.3 - 10), (2300 * 0.3, 10)),
            ColliderRect((-2300 / 2 * 0.3 - 10, -1300 / 2 * 0.3), (10, 1300 * 0.3)),
        ],
        'entities': ActorContainer()
    }
        
}

level_manager = LevelManager((662, 662), player, levels)
level_manager.load_level("floor", (0, 0))


class hallway(Scene):
    SCENE_NAME = "hallway"

    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
        self.globals = kwargs

    def on_show(self, room="fields", player_pos=(0, 0)):
        global level_manager, text_anim, sprite

        reset_opacity()

        if room == "fields":
            player_pos= (0, 1000)
        elif room == 'floor':
            player_pos = (0, 588)

        if level_manager.current_level.startswith("room"):
            levels[room]["entities"].enemy.hidden = True
        
        level_manager.load_level(room, player_pos)

    def on_update(self, dt):
        if not freeze_frame:
            level_manager.update(dt)

        if counter >= 1: # CHANGE
            levels["floor"]["world"].image = "floor1-open"

        if level_manager.current_level.startswith("tutorial") and text_anim and sprite:
            text_anim.update(dt)
            sprite.update(dt)

        if text_anim is None or text_anim.is_complete():
            player.move()
            
        print(player.pos)

    def on_draw(self, screen):
        global counter

        level_manager.draw(screen)
        ui.draw()
        scroll_counter_img.draw()
        
        
        screen.draw.text(f"{counter}", (40, 615))

        if text_anim and sprite:
            text_anim.draw(screen)
            if not text_anim.is_complete():
                sprite.draw(screen)

    def on_key_down(self, key, unicode):
        if text_anim and keyboard.SPACE:
            if not text_anim.is_complete():
                text_anim.next()
            else:
                text_anim.hidden = True
                sprite.hidden = True
