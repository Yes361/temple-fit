from helper import ActorContainer, Singleton
from typing import Dict, Tuple, List, Type
from dataclasses import dataclass
from constants import Constants
from abc import ABC, abstractmethod
import pygame




class placeholder(ABC):
    scenes = []
    def __init__(self, *args, **kwargs):
        self.scenes.append(self)
        
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
    


@dataclass
class Scene: 
    on_update: callable = None
    on_draw: callable = None
    on_show: callable = None
    on_hide: callable = None
    UI_elements: ActorContainer = None

class SceneManager(Singleton):
    """
    Handles Scene Transition/Visibility and Draw/Update Callbacks
    """
    def __init__(self, predefined_scenes={}):
        self.scenes: Dict[any, Type[Scene]] = predefined_scenes
        self._active_scenes: List[str] = []
        
    def subscribe_scene(self, scene_name, scene: Type[Scene | placeholder]):
        assert scene_name not in self.scenes, f'\"{scene_name}\" is already subscribed.'
        self.scenes[scene_name] = scene

    def unsubscribe_scene(self, scene):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self.scenes.pop(scene)
    
    def subscribe(self, 
                  scene, 
                  update_callback: callable=None, 
                  draw_callback: callable=None, 
                  on_show: callable=None, 
                  on_hide: callable=None, 
                  UI_elements: ActorContainer=None
        ):
        assert scene not in self.scenes, f'\"{scene}\" is already subscribed.'
        self.scenes[scene] = Scene(update_callback, draw_callback, on_show, on_hide, UI_elements)
            
    def unsubscribe(self, scene):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self.scenes.pop(scene)

    def show_scene(self, scene):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        assert scene not in self._active_scenes, f'\"{scene}\" is already visible.'
        self._active_scenes.append(scene)
        current_scene = self.scenes[scene]
        
        if current_scene.UI_elements is not None:
            current_scene.UI_elements.hidden = False
        
        if callable(current_scene.on_show):
            current_scene.on_show()
        
    def hide_scene(self, scene):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        assert scene in self._active_scenes, f'\"{scene}\" is already invisible.'
        self._active_scenes.remove(scene)
        current_scene = self.scenes[scene]
        
        if current_scene.UI_elements is not None:
            current_scene.UI_elements.hidden = True
        
        if callable(current_scene.on_hide):
            current_scene.on_hide()
        
    def clear_active_scenes(self):
        for scene in self._active_scenes:
            self.hide_scene(scene)
        self._active_scenes.clear()
        
    @property
    def get_active_scenes(self):
        return self._active_scenes

    def switch_scene(self, scene):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self.clear_active_scenes()
        self.show_scene(scene)
    
    def draw(self, screen):        
        for scene in self._active_scenes:
            
            current_scene = self.scenes[scene]
            on_draw = current_scene.on_draw
            if self._active_scenes is not None and callable(on_draw):
                on_draw(screen)
            
            if current_scene.UI_elements is not None:
                current_scene.UI_elements.draw(screen)
            
    def update(self, dt):
        for scene in self._active_scenes:
            
            current_scene = self.scenes[scene]
            on_update = current_scene.on_update
            if self._active_scenes is not None and callable(on_update):
                on_update(dt)
            
            if current_scene.UI_elements is not None:
                current_scene.UI_elements.update(dt)

@dataclass
class InputEvent:
    type: any
    callback: callable
    
class InputManager(Singleton):
    """
    jksadoasdksadjasdjksadjaskdad
    """
    EVENTS = [Constants.KEY_UP, Constants.KEY_DOWN, Constants.KEY_HOLD, Constants.MOUSE_HOVER]
    def __init__(self):
        self._group = None
        self._callbacks: Dict[any, List[InputEvent]] = {}
    
    def subscribe(self, type, callback: callable, group_identifier: any):
        if group_identifier not in self._callbacks:
            self._callbacks[group_identifier] = []
        self._callbacks[group_identifier].append(InputEvent(type, callback))
        
    def unsubscribe(self, group_identifier=None, callback=None, ):
        self._callbacks.remove(group_identifier)
    
    def clear_group(self):
        self._group = None
    
    def set_group(self, group):
        assert group in self._callbacks, f'{group} is not subscribed.'
        self._group = group
    
    def filter_events(self, type, *args, **kwargs):
        if self._group:
            for event in self._callbacks[self._group]:
                if event.type == type and event.callback:
                    event.callback(*args, **kwargs)
        else:
            for _, group in self._callbacks.items():
                for event in group:
                    if event.type == type and event.callback:
                        event.callback(*args, **kwargs)
    
    def on_key_down(self, key, unicode):
        self.filter_events(Constants.KEY_DOWN, key, unicode)
        
    def on_key_up(self, key, unicode):
        self.filter_events(Constants.KEY_UP, key, unicode)
    
    def on_key_hold(self, dt):
        self.filter_events(Constants.KEY_HOLD)
        
    def on_mouse_hover(self, pos):
        self.filter_events(Constants.MOUSE_HOVER, pos)
        
    def on_mouse_down(self, pos, button):
        self.filter_events(Constants.MOUSE_DOWN, pos, button)
        
    def on_mouse_up(self, pos, button):
        self.filter_events(Constants.MOUSE_UP, pos, button)
                
input_manager = InputManager()
scene_manager = SceneManager()

# class GameManager:
#     def __init__(self):
#         self._scene_manager = scene_manager
#         self._input_manager = input_manager
    
#     def load_game_actors(self, scene_name):
#         pass