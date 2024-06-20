from managers import Scene, game_manager
from Game import LevelManager, ColliderRect, Entity, Player, Dialogue
from helper import (
    Actor,
    ActorContainer,
    schedule,
    Rect,
    Music,
    CACHED_DIALOGUE,
    CACHED_VOICELINES,
)
from pgzero.builtins import animate, keyboard
import random

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

# UI setup
text_box = Actor("narrative_text_box", pos=(370, 600), scale=0.3)
text_box.resize((450, 95))
ui = Actor("battle_scene_tab", scale=0.15)
ui.topleft = (0, 662 - ui.height)
scroll_counter = 0
text_anim = None
key_counter_img = Actor("key", pos=(50, 610))
key_counter_img.scale = 0.15
scroll_counter_img = Actor("scroll", pos=(110, 610))
scroll_counter_img.scale = 0.10

# Constants for scrolls and floors
FIRST_SET_OF_SCROLLS = 8
SECOND_SET_OF_SCROLLS = 6
required_scrolls = FIRST_SET_OF_SCROLLS
current_floor = 0
key_counter = 0

# Fade animation between rooms and battle scenes
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
        """
        Enemy AI simply moves towards the player, and on contact, switches to the battle scene
        """
        global player

        def switch():
            game_manager.switch_scene(
                "Battle",
                next=self.next,
                room=current_floor,
                enemy_image=self.image,
                scale=20 / self.width,
            )
            levels[level_manager.current_level]["entities"].enemy.hidden = True

        if self.hidden:
            return

        self.direction = self.direction_to(player)
        self.move_in_direction(self.speed)

        if self.colliderect(player):
            fade()
            schedule(switch, 1)

        super().update(dt)


class Item(Entity):
    def update(self, dt):
        """
        Each item simply increments the appropriate counter on contact
        """
        global player, scroll_counter, key_counter
        if self.hidden:
            return

        if self.colliderect(player):
            if self.image == "scroll":
                levels[level_manager.current_level]["entities"].scroll.hidden = True
                scroll_counter += 1
            elif self.image == "key":
                levels[level_manager.current_level]["entities"].key.hidden = True
                key_counter += 1

# Basic Colliders for rooms left and right of the main hallway on each floor

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


def load_final_room():
    global text_anim

    level_manager.load_level("final_room", player_pos=(0, 0))
    sprite = Actor("narrative_icon", pos=(100, 580))

    text_anim = Dialogue(
        sprite,
        {
            "MC": "character-battle-sprite",
            "OM": "old_man_icon",
        },
        CACHED_DIALOGUE["outro"],
        voice_lines=CACHED_VOICELINES["oms"],
        time_per_char=0.02,
        bounding_box=Rect((220, 565), (425, 75)),
        color="black",
        on_finish=lambda: game_manager.switch_scene(
            "Battle", next="outro", enemy_image="old_man_enemy", scale=0.4, room=2
        ),
    )


def next_floor(floor):
    global scroll_counter, key_counter, required_scrolls, current_floor
    if key_counter < 1:
        return

    if floor == "floor" and scroll_counter >= required_scrolls:
        level_manager.load_level("floor2", player_pos=(0, -378))
        required_scrolls += SECOND_SET_OF_SCROLLS
        key_counter = 0
        current_floor += 1
    if floor == "floor2" and scroll_counter >= required_scrolls:
        level_manager.load_level("floor3", player_pos=(0, 453))
        current_floor += 1


# Creates a room branching from the main hallway on each floor
def create_room(name: str, world: str, floor: str, next_player_pos: tuple, left_side: bool, enemy_type: str, scale=0.15):
    if left_side:
        colliders = [
            ColliderRect(
                (1080 * 662 / 1080 / 2 - 81 - 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level(floor, player_pos=next_player_pos),
            )
        ] + left_rooms
        enemy_spawn = (-100, 0)
    else:
        colliders = [
            ColliderRect(
                (-1080 * 662 / 1080 / 2 + 1, -1080 * 662 / 1080 / 2 + 81 * 4),
                (81, 81),
                fn=lambda: level_manager.load_level(floor, player_pos=next_player_pos),
            )
        ] + right_rooms
        enemy_spawn = (100, 0)

    return {
        "world": Actor(world, scale=662 / 1080),
        "colliders": colliders,
        "entities": ActorContainer(
            enemy=Enemy(enemy_type, pos=enemy_spawn, scale=scale, next=name),
            scroll=Item("scroll", scale=0.15, pos=(0, 0)),
        ),
    }

# Load the Dialogue and Tutorial
def load_tutorial():
    global text_anim
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
                fn=lambda: level_manager.load_level(
                    "tutorial_boss", player_pos=(-280, 0)
                ),
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
            ),
            ColliderRect(
                (-662 / 2, 960 / 2 * 662 / 208),
                (662, 10),
            ),
            ColliderRect(
                (-662 / 2 + 10, -960 / 2),
                (10, 960 * 662 / 208),
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
                fn=lambda: next_floor("floor"),
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 83, -4320 * 0.3 / 2 + 80 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room1", player_pos=(100, 0)),
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room2", player_pos=(-100, 0)),
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room3", player_pos=(100, 0)),
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room4", player_pos=(-100, 0)),
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room5", player_pos=(100, 0)),
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 3, -4320 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room6", player_pos=(-100, 0)),
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -4320 * 0.3 / 2 + 81 * 14 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room7", player_pos=(100, 0)),
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -4320 * 0.3 / 2 + 81 * 14 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room8", player_pos=(-100, 0)),
            ),
        ],
        "entities": ActorContainer(),
    },
    "room1": create_room("room1", "stone_left", "floor", (-84, -370), True, "green_moth", scale=0.1),
    "room2": create_room("room2", "netherite_right", "floor", (96, -370), False, "scorpion", scale=0.15),
    "room3": create_room("room3", "wood_left", "floor", (-84, 48), True, "dragon", scale=0.2),
    "room4": create_room("room4", "stone_right", "floor", (96, 48), False, "dragon", scale=0.2),
    "room5": create_room("room5", "purple_left", "floor", (-84, 219), True, "red_hood", scale=0.3),
    "room6": create_room("room6", "purple_right", "floor", (96, 219), False, "green_moth", scale=0.1),
    "room7": create_room("room7", "netherite_left", "floor", (-84, 501), True, "red_hood", scale=0.3),
    "room8": create_room("room8", "wood_right", "floor", (96, 501), False, "scorpion", scale=0.15),
    "floor2": {
        "world": Actor("floor2", scale=0.3),
        "colliders": [
            ColliderRect((-2160 * 0.3 / 2 + 81, -3500 * 0.3 / 2), (81, 3500 * 0.3)),
            ColliderRect((2160 * 0.3 / 2 - 81 * 2, -3500 * 0.3 / 2), (81, 3500 * 0.3)),
            ColliderRect(
                (-2160 * 0.3 / 2 + 81, 3500 * 0.3 / 2 - 80),
                (3500 * 0.3, 10),
                fn=lambda: next_floor("floor2"),
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 83, -3500 * 0.3 / 2 + 80 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room1-2", player_pos=(100, 0)),
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -3500 * 0.3 / 2 + 81 * 3 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room2-2", player_pos=(-100, 0)),
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -3500 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room3-2", player_pos=(100, 0)),
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 1, -3500 * 0.3 / 2 + 81 * 7 + 10),
                (81, 81),
                fn=lambda: level_manager.load_level("room4-2", player_pos=(-100, 0)),
            ),
            ColliderRect(
                (-2160 * 0.3 / 2 + 82, -3500 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room5-2", player_pos=(100, 0)),
            ),
            ColliderRect(
                (2160 * 0.3 / 2 - 81 * 2 - 3, -3500 * 0.3 / 2 + 81 * 11 - 25),
                (81, 81),
                fn=lambda: level_manager.load_level("room6-2", player_pos=(-100, 0)),
            ),
        ],
        "entities": ActorContainer(),
    },
    "room1-2": create_room("room1-2", "smooth_left", "floor2", (-84, -370), True, "dragon", scale=0.2),
    "room2-2": create_room("room2-2", "brick_right", "floor2", (96, -370), False, "red_hood", scale=0.3),
    "room3-2": create_room("room3-2", "block_left", "floor2", (-84, 48), True, "scorpion", scale=0.15),
    "room4-2": create_room("room4-2", "smooth_right", "floor2", (96, 48), False, "green_moth", scale=0.1),
    "room5-2": create_room("room5-2", "brick_left", "floor2", (-84, 219), True, "dragon", scale=0.2),
    "room6-2": create_room("room6-2", "block_right", "floor2", (96, 219), False, "red_hood", scale=0.3),
    "floor3": {
        "world": Actor("floor3", scale=0.3),
        "colliders": [
            ColliderRect((-2160 * 0.3 / 2 + 81, -3500 * 0.3 / 2), (81, 3500 * 0.3)),
            ColliderRect((2160 * 0.3 / 2 - 81 * 2, -3500 * 0.3 / 2), (81, 3500 * 0.3)),
            ColliderRect((-2160 * 0.3 / 2 + 81, 3500 * 0.3 / 2), (3500 * 0.3, 10)),
            ColliderRect(
                (-2160 * 0.3 / 2 + 81, -3500 * 0.3 / 2 + 80),
                (3500 * 0.3, 10),
                fn=load_final_room,
            ),
        ],
        "entities": ActorContainer(),
    },
    "final_room": {
        "world": Actor("final_room"),
        "colliders": [
            ColliderRect((-662 / 2, -662 / 2 - 10), (662, 10)),
            ColliderRect((662 / 2, -662 / 2), (10, 662)),
            ColliderRect((-662 / 2, 662 / 2 - 10), (662, 10)),
            ColliderRect((-662 / 2 - 10, -662 / 2), (10, 662)),
        ],
        "entities": ActorContainer(),
    },
}

# Position the keys randomly on each floor
def position_keys():
    random_room_floor1 = f"room{random.randint(1, 8)}"
    random_pos_floor1 = (random.randint(-200, 200), random.randint(-200, 200))
    levels[random_room_floor1]["entities"].add("key", Item("key", pos=random_pos_floor1, scale=0.5))

    random_room_floor2 = f"room{random.randint(1, 6)}-2"
    random_pos_floor2 = (random.randint(-200, 200), random.randint(-200, 200))
    levels[random_room_floor2]["entities"].add("key", Item("key", pos=random_pos_floor2, scale=0.5))


level_manager = LevelManager((662, 662), player, levels)
level_manager.load_level("floor", (0, 0))


class hallway(Scene):
    SCENE_NAME = "hallway"

    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
        self.globals = kwargs

    def on_show(self, room="fields", player_pos=(0, 0)):

        global level_manager, text_anim

        if not Music.is_playing("in_game"):
            Music.stop()
            Music.play("in_game")

        reset_opacity()

        if room == "fields":
            player_pos = (0, 1000)
        elif room == "floor":
            player_pos = (0, 588)

        level_manager.load_level(room, player_pos)

    def on_update(self, dt):
        if not freeze_frame:
            level_manager.update(dt)

        # Change the closed floor1 image to an open floor1 image if conditions are met
        if scroll_counter >= FIRST_SET_OF_SCROLLS and key_counter >= 1:
            levels["floor"]["world"].image = "floor1-open"

        if level_manager.current_level.startswith("tutorial") and text_anim:
            text_anim.update(dt)

        if text_anim is None or text_anim.is_complete():
            player.move()

    def on_draw(self, screen):
        level_manager.draw(screen)
        ui.draw()

        scroll_counter_img.draw()
        key_counter_img.draw()
        screen.draw.text(f"{key_counter}/1", (30, 630), fontname="pixel", fontsize=30)
        screen.draw.text(
            f"{scroll_counter}/{required_scrolls}",
            (80, 630),
            fontname="pixel",
            fontsize=30,
        )

        if text_anim is not None and not text_anim.is_complete():
            text_box.draw()
            text_anim.draw(screen)

    def on_key_down(self, key, unicode):
        if text_anim and keyboard.SPACE:
            if not text_anim.is_complete():
                text_anim.next()

    def reset(self):
        global scroll_counter, key_counter, required_scrolls
        scroll_counter = 0
        key_counter = 0

        required_scrolls = FIRST_SET_OF_SCROLLS
        
        levels["floor"]["world"].image = "floor1-open"

        # Reset the Entities in each level to a base state
        for level in levels.values():
            entities = level["entities"]
            if entities.has("enemy"):
                entities.enemy.hidden = False

            if entities.has("scroll"):
                entities.scroll.hidden = False

            if entities.has("key"):
                entities.remove("key")
        position_keys()