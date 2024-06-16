from helper import ActorContainer, Actor, Rect
from managers import Scene
from Game import camera, pose, HealthBar, Text
from dataclasses import dataclass
from typing import List
import pygame

@dataclass
class Objective:
    action: str
    count: str
    hp: int = 20
    completed: bool = False
    
objectives: List[Objective] = []
        
def check_uncompleted_objectives():
    for obj in objectives:
        if obj.completed:
            continue
        
        so_far = pose.report_stats(obj.action)
        
        if so_far > obj.count:
            obj.completed = True
            enemy_health_bar.take_damage(obj.hp)
            
def create_new_objective(exercise, required_count):
    objectives.append(Objective(exercise, required_count))

def draw_checklist(screen):
    screen.draw.text('Checklist', (40, 30), fontname='pixel', fontsize=30, owidth=0.5, ocolor='white')
    for idx, obj in enumerate(objectives):
        completed_text = 'x' if obj.completed else ''
        screen.draw.text(f'[{completed_text}] complete {obj.count} {obj.action}', (75, 60 + 30 + idx * 30), fontname='pixel', fontsize=30, owidth=0.5, ocolor='white')
            

class battle(Scene):
    SCENE_NAME = 'Battle'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
            
    def on_show(self):
        global backdrop, player_sprite, player_sprite_name, player_heath_bar, enemy_sprite, enemy_health_bar, enemy_sprite_name, checklist, completed
        
        backdrop = Actor('battle-backdrop', topleft=(0, 0), dims=(662, 662))
        
        player_sprite = Actor('character-battle-sprite', topleft=(50, 282), scale=1.2)
        player_sprite_name = 'Player TMP'
        player_heath_bar = HealthBar('healthbar', Rect((78, 35), (176, 28)), 100, topleft=(10, 510), scale=0.8)
        
        enemy_sprite = Actor('character-battle-sprite', topleft=(371, 109), scale=0.5)
        enemy_sprite_name = 'Enemy TMP'
        enemy_health_bar = HealthBar('healthbar', Rect((78 * 0.6/0.8, 35 * 0.6/0.8), (176 * 0.6/0.8, 28 * 0.6/0.8)), 100, topleft=(300, 250), scale=0.6)
        
        camera.resize((250, 250 * 3 / 4))
        camera.topleft = (355, 386)
        
        create_new_objective('jumping jacks', 2)
                
    def on_hide(self):
        pass
    
    def on_draw(self, screen):
        backdrop.draw()
        camera.draw(screen)
        draw_checklist(screen)
        
        player_sprite.draw(screen)
        enemy_sprite.draw(screen)
        
        enemy_health_bar.draw(screen)
        player_heath_bar.draw(screen)
        
        screen.draw.text(player_sprite_name, (player_sprite.left + 90, player_sprite.top - 10), fontname='pixel')
        screen.draw.text(enemy_sprite_name, (enemy_sprite.left + 10, enemy_sprite.top - 20), fontname='pixel')
        
        # print(pygame.mouse.get_pos())
        
        
    def on_update(self, dt):
        check_uncompleted_objectives()
        
    def on_key_down(self, key, unicode):
        # a.change_counter(1)
        pass