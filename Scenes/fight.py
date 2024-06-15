from helper import ActorContainer, Actor, Rect
from managers import Scene
from Game import camera, HealthBar, Text, CheckList
import pygame

class battle(Scene):
    SCENE_NAME = 'Battle'
    
    def __init__(self, **kwargs):
        super().__init__(self.SCENE_NAME)
            
    def on_show(self):
        global backdrop, player_sprite, player_sprite_name, enemy_sprite, enemy_sprite_name
        
        backdrop = Actor('tmp0', topleft=(0, 0), dims=(662, 662))
        
        player_sprite = Actor('character-battle-sprite', topleft=(131, 282), scale=1)
        player_sprite_name = 'Player TMP'
        
        enemy_sprite = Actor('character-battle-sprite', topleft=(371, 109), scale=1)
        enemy_sprite_name = 'Enemy TMP'
        
        camera.resize((216, 216 * 3 / 4))
        camera.topleft = (355, 386)
        
    def on_hide(self):
        pass
    
    def on_draw(self, screen):
        backdrop.draw()
        camera.draw(screen)
        
        player_sprite.draw(screen)
        enemy_sprite.draw(screen)
        
        screen.draw.text(player_sprite_name, (player_sprite.x, player_sprite.y - 20))
        screen.draw.text(enemy_sprite_name, (enemy_sprite.x, enemy_sprite.y - 20))
        print(pygame.mouse.get_pos())
        
        
    def on_update(self, dt):
        pass
        
    def on_key_down(self, key, unicode):
        # a.change_counter(1)
        pass