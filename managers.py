from abc import ABC, abstractmethod
from helper import ActorContainer
from typing import *
import pygame

class Scene:
    def __init__(self, scene, *args, **kwargs):
        game_manager.subscribe(scene, self)
        self.globals = kwargs
        # self.all_actors = ActorContainer(
        #     UI_element = ActorContainer(),
        #     Actors = ActorContainer()   
        # )
        # self.Actors = self.all_actors.Actor
        # self.UI_element = self.all_actors.UI_element
    
    @abstractmethod
    def load_actors():
        pass
    
    @abstractmethod
    def delete_actors():
        pass
    
    @abstractmethod
    def on_show(self):
        pass
    
    @abstractmethod
    def on_hide(self):
        pass
    
    @abstractmethod
    def on_draw(self, screen):
        pass
    
    @abstractmethod
    def on_update(self, dt):
        pass
    
    @abstractmethod
    def on_key_down(self, key, unicode):
        pass
    
    @abstractmethod
    def on_key_up(self, key):
        pass
    
    @abstractmethod
    def on_key_hold(self, dt):
        pass
    
    @abstractmethod
    def on_mouse_down(self, pos, button):
        # if self.UI_element.hidden:
        #     return
        
        # for actor in self.UI_element:
        #     actor.on_click(pos, button)
        pass
    
    @abstractmethod
    def on_mouse_move(self, pos, rel, buttons):
        pass
    
    @abstractmethod
    def on_mouse_hold(self, pos, buttons):
        # if self.UI_element.hidden:
        #     return
        
        # for actor in self.UI_element:
        #     actor.on_hold(pos, buttons)
        pass
    
    @abstractmethod
    def on_mouse_up(self, pos, buttons):
        pass
    
    @abstractmethod
    def on_mouse_hover(self, pos):
        # if self.UI_element.hidden:
        #     return
        
        # for actor in self.UI_element:
        #     actor.on_hover(pos)
        pass
    
    @abstractmethod
    def on_music_end(self):
        pass
    
class GameManager:
    """
    Handles Scene Transition/Visibility and Draw/Update Callbacks
    """
    def __init__(self, predefined_scenes={}):
        self.scenes: Dict[any, Type[Scene]] = predefined_scenes
        self._active_scenes: List[str] = []
        self._event_stack = []
        
    def subscribe(self, scene_name, scene: Type[Scene]):
        assert scene_name not in self.scenes, f'\"{scene_name}\" is already subscribed.'
        self.scenes[scene_name] = scene

    def unsubscribe(self, scene):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self.scenes.pop(scene)
        
    def list_all_scenes(self):
        return self.scenes.keys()

    def show_scene(self, scene, *args, switch_event_scene: bool = True, **kwargs):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        assert scene not in self._active_scenes, f'\"{scene}\" is already visible.'
        
        if switch_event_scene:
            self._event_stack.append(scene)
        
        self._active_scenes.append(scene)
        self.scenes[scene].on_show(*args, **kwargs)
        
    def hide_scene(self, scene, *args, **kwargs):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        assert scene in self._active_scenes, f'\"{scene}\" is already invisible.'
        
        self._active_scenes.remove(scene)
        
        self.scenes[scene].on_hide(*args, **kwargs)
        if len(self._event_stack) > 0:
            self._event_stack.pop()
        
    def clear_active_scenes(self):
        for scene in self._active_scenes:
            self.hide_scene(scene)
        self._active_scenes.clear()
        
    def get_active_scenes(self):
        return self._active_scenes

    def switch_scene(self, scene, *args, **kwargs):
        assert scene not in self._active_scenes, f'\"{scene}\" is already active.'
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self.clear_active_scenes()
        
        if len(self._event_stack) > 0:
            self._event_stack.pop()
        self.show_scene(scene, *args, switch_event_scene=True, **kwargs)
    
    def draw(self, screen):        
        for scene in self._active_scenes:
            
            current_scene = self.scenes[scene]
            current_scene.on_draw(screen)
            
    def update(self, dt):
        for scene in self._active_scenes:
            
            current_scene = self.scenes[scene]
            current_scene.on_update(dt)
            
        current_event = self.current_event()
        self.scenes[current_event].on_mouse_hold(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        self.scenes[current_event].on_mouse_hover(pygame.mouse.get_pos())
        self.scenes[current_event].on_key_hold(dt)
                
    def current_event(self):
        return self._event_stack[-1]
                
    def on_key_down(self, key, unicode):
        self.scenes[self.current_event()].on_key_down(key, unicode)
    
    def on_mouse_move(self, pos, button, rel):
        self.scenes[self.current_event()].on_mouse_move(pos, button, rel)
        
    def on_mouse_down(self, pos, button):
        self.scenes[self.current_event()].on_mouse_down(pos, button)
    
    def on_mouse_up(self, pos, button):
        self.scenes[self.current_event()].on_mouse_up(pos, button)
        
    def on_key_up(self, key):
        self.scenes[self.current_event()].on_key_up(key)
        
    def on_music_end(self):
        self.scenes[self.current_event()].on_music_end()
          
game_manager = GameManager()