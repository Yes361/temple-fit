from helper import ActorContainer, Actor, Rect, schedule
from managers import Scene, game_manager
from pgzero.builtins import animate
from Game import camera, Pose, HealthBar, Entity
from dataclasses import dataclass
from typing import List
import pygame, random

# Definitions

@dataclass
class Objective:
    action: str
    count: str
    completed: bool = False


def player_health(hp):
    if hp < 0:
        game_manager.switch_scene("")


# Global Actor Definitions

backdrop = Actor("battle-backdrop", topleft=(0, 0), dims=(662, 662))

camera.resize((250, 250 * 3 / 4))
camera.topleft = (355, 386)

player_sprite = Entity(
    "character-battle-sprite",
    topleft=(50, 282),
    scale=1.2,
)

player = ActorContainer(
    player_sprite=player_sprite,
    healthbar=HealthBar(
        "healthbar",
        Rect((78, 35), (220, 35)),
        100,
        on_hp_change=player_health,
        topleft=(10, 510),
        scale=0.8,
        fill = (153,1,1)
    ),
)
player.name = "Player TMP"

enemy_sprite = Entity(
    "character-battle-sprite",
    topleft=(371, 109),
    scale=0.5,
)

enemy = ActorContainer(
    enemy_sprite=enemy_sprite,
    healthbar=HealthBar(
        "healthbar", Rect((58.5, 26.25), (220, 35)), 100, topleft=(300, 250), scale=0.6, fill = (153,1,1)
    ),
)
enemy.name = "Enemy TMP"

next_room = "hallway"
next_player_pos = (0, 0)


all_actors = ActorContainer(
    player=player, enemy=enemy, cam=camera, back=backdrop
)

objectives: List[Objective] = []

# Helper Functions

def anim():
    def move_player():
        hp_damage_taken = enemy.healthbar.total_hp / len(objectives)
        enemy.healthbar.animate_damage(hp_damage_taken)
        
    def move_enemy():
        player.healthbar.animate_damage(random.randint(0, 20))
        schedule(move_player, 0.1)

    schedule(move_enemy, 2)


def create_new_objective(rec):
    min_count, max_count = rec["exercise"]
    count = random.randint(min_count, max_count)
    for i in range(count):
        exercise_of_choice = random.choice(Pose.IMPLEMENTED_ACTIONS)
        if i == 0:
            Pose.set_active_recognizer([exercise_of_choice])

        min_set, max_set = rec["sets"]
        objectives.append(
            Objective(exercise_of_choice, random.randint(min_set, max_set))
        )


def check_uncompleted_objectives():
    for idx, obj in enumerate(objectives):
        if obj.completed:
            continue
        
        if Pose.report_stats(obj.action) >= obj.count:
            obj.completed = True
            anim()

            try:
                Pose.reset_all_recognizers()
                Pose.set_active_recognizer([objectives[idx + 1].action])
            except IndexError:
                schedule(lambda: game_manager.switch_scene('hallway', next_room, next_player_pos), 1)

        break

# TODO: make it pretteh
def draw_checklist(screen):
    screen.draw.text(
        "Checklist", (40, 30), fontname="pixel", fontsize=30, owidth=0.5, ocolor="white"
    )
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

def reset():
    objectives.clear()
    player.healthbar.hp = 100
    enemy.healthbar.hp = 100

class battle(Scene):
    SCENE_NAME = "Battle"

    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)

    # TODO: vary difficulty
    def on_show(self, next="hallway", pos=(0, 0), room=0, enemy_image='character-battle-sprite'):
        global next_room, next_player_pos
        next_room = next
        next_player_pos = pos
        enemy_sprite.image = enemy_image

        reset()
        # create_new_objective(exercise[room])
        objectives.append(Objective("bicep curls", 10))
        objectives.append(Objective("bicep curls", 10))
        objectives.append(Objective("bicep curls", 10))

    def on_hide(self):
        pass

    def on_draw(self, screen):
        # all_actors.draw(screen)
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

    def on_update(self, dt):
        all_actors.update(dt)
        check_uncompleted_objectives()

    def on_key_down(self, key, unicode):
        pass