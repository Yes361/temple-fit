from helper import ActorContainer, Actor, Rect, schedule, Music
from managers import Scene, game_manager
from Game import camera, Pose, HealthBar, Entity
from dataclasses import dataclass
from typing import List
import random
from . import config

# Definitions

@dataclass
class Objective:
    """
    Represents a specific objective in the battle, consisting of an action
    to perform, a count of how many times to perform it, and a completion status.
    """
    action: str
    count: str
    completed: bool = False

# Global Actor Definitions

backdrop = Actor("battle-backdrop", topleft=(0, 0), dims=(662, 662))

# Configure the camera size and position.
camera.resize((250, 250 * 3 / 4))
camera.topleft = (355, 386)

player_sprite = Entity(
    "character-battle-sprite",
    topleft=(50, 282),
    scale=1.2,
)

# Callback function for when the player's health changes
def player_health(hp):
    if hp < 0:
        game_manager.switch_scene("Start Screen", False)

# Define the player actor container with health bar.
player = ActorContainer(
    player_sprite=player_sprite,
    healthbar=HealthBar(
        "healthbar",
        Rect((78, 35), (220, 35)),
        100,
        on_hp_change=player_health,
        topleft=(10, 510),
        scale=0.8,
        fill=(153, 1, 1),
    ),
)
player.name = "The MC"

enemy_sprite = Entity(
    "character-battle-sprite",
    topleft=(371, 109),
    scale=0.5,
)

# Define the enemy actor container with health bar.
enemy = ActorContainer(
    enemy_sprite=enemy_sprite,
    healthbar=HealthBar(
        "healthbar",
        Rect((58.5, 26.25), (220, 35)),
        100,
        topleft=(300, 250),
        scale=0.6,
        fill=(153, 1, 1),
    ),
)
enemy.name = "The Big Bad"

# Initialize variables for the next room, player position, and timer.
next_room = "hallway"
next_player_pos = (0, 0)
timer = 0

objectives: List[Objective] = []

# Defines the animations for player and enemy movements during the battle.
def anim():
    def move_player():
        hp_damage_taken = enemy.healthbar.total_hp / len(objectives)
        enemy.healthbar.animate_damage(hp_damage_taken)

    def move_enemy():
        player.healthbar.animate_damage(random.randint(0, 20))
        schedule(move_player, 0.1)

    schedule(move_enemy, 2)

# Creates objectives based on the exercise recommendations in the configuration.
def create_objectives(rec):
    min_count, max_count = rec["exercise"]
    count = random.randint(min_count, max_count)
    
    for i in range(count):
        exercise_of_choice = random.choice(Pose.IMPLEMENTED_ACTIONS)
        
        # Set the recognizer for the first exercise
        if i == 0:
            Pose.set_active_recognizer([exercise_of_choice])

        min_set, max_set = rec["sets"]
        objectives.append(Objective(exercise_of_choice, random.randint(min_set, max_set)))



# Checks the list of objectives and updates their completion status.
# If an objective is completed, triggers the next animation and objective.
def check_uncompleted_objectives():
    for idx, obj in enumerate(objectives):
        if obj.completed:
            continue
        
        # 
        if Pose.report_stats(obj.action) >= obj.count:
            obj.completed = True
            anim()

            Pose.reset_all_recognizers()
            try:
                Pose.set_active_recognizer([objectives[idx + 1].action])
            except IndexError:
                schedule(next_scene, 1)
        break

# Draws the checklist
def draw_checklist(screen):
    screen.draw.text("Checklist", (40, 30), fontname="pixel", fontsize=30, owidth=0.5, ocolor="white") # Title
    
    for idx, obj in enumerate(objectives):
        completed_text = "x" if obj.completed else ""
        screen.draw.text(
            f"[{completed_text}] complete {obj.count} {obj.action}",
            (75, 60 + 30 + idx * 30),
            fontname="pixel",
            fontsize=30,
            owidth=0.5,
            ocolor="white",
        )

# Switches to the next scene based on the current room.
def next_scene():
    if next_room == "outro":
        game_manager.switch_scene("outro")
    else:
        game_manager.switch_scene("hallway", next_room, next_player_pos)

# Resets the battle scene, clearing objectives and resetting health bars and timers.
def reset():
    global timer
    objectives.clear()
    player.healthbar.stop_animating_damage()
    enemy.healthbar.stop_animating_damage()
    
    player.healthbar.hp = 100
    enemy.healthbar.hp = 100
    
    timer = config.time_limit

class battle(Scene):
    SCENE_NAME = "Battle"

    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)

    def on_show(
        self,
        next="hallway",
        pos=(0, 0),
        room=0,
        enemy_image="character-battle-sprite",
        scale=1,
    ):
        global next_room, next_player_pos
        
        Music.stop()
        Music.play('battle')        
        
        next_room = next
        next_player_pos = pos
        enemy_sprite.image = enemy_image
        enemy_sprite.scale = scale

        reset()
        create_objectives(config.exercise[room])
    
    def on_hide(self):
        Pose.reset_all_recognizers()

    def on_draw(self, screen):
        backdrop.draw()
        camera.draw(screen)
        draw_checklist(screen)

        player.draw(screen)
        enemy.draw(screen)

        draw_checklist(screen)

        screen.draw.text(
            player.name,
            (player_sprite.left + 90, player_sprite.top - 10),
            fontname="pixel",
        )
        screen.draw.text(
            enemy.name,
            (enemy_sprite.left + 10, enemy_sprite.top - 20),
            fontname="pixel",
        )
        
        screen.draw.text(f'time remaining: {timer:.3f}', (400, 50), fontname="pixel")

    def on_update(self, dt):
        global timer
        check_uncompleted_objectives()
        
        timer -= dt
        
        if timer < 0:
            game_manager.reset_scenes()
            game_manager.switch_scene('hallway', 'floor')
        
        if player.healthbar.hp < 1:
            game_manager.switch_scene("Start Screen", False)

    def reset(self):
        reset()