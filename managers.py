from typing import Dict, Tuple, List
from dataclasses import dataclass
from helper import ActorContainer
from constants import Constants
import pygame

@dataclass
class Scene: 
    update_callback: callable = None
    draw_callback: callable = None
    on_show: callable = None
    on_hide: callable = None
    UI_elements: ActorContainer = None

class SceneManager:
    """
    Handles Scene Transition/Visibility and Draw/Update Callbacks
    """
    def __init__(self, predefined_scenes={}):
        self.scenes: Dict[str, Scene] = predefined_scenes
        self._active_scenes: List[str] = []
    
    def subscribe(self, 
                  scene: str, 
                  update_callback: callable=None, 
                  draw_callback: callable=None, 
                  on_show: callable=None, 
                  on_hide: callable=None, 
                  UI_elements: ActorContainer=None
        ):
        assert scene not in self.scenes, f'\"{scene}\" is already subscribed.'
        self.scenes[scene] = Scene(update_callback, draw_callback, on_show, on_hide, UI_elements)
            
    def unsubscribe(self, scene: str):
        if scene in self.scenes:
            self.scenes.pop(scene)

    def show_scene(self, scene: str):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        assert scene not in self._active_scenes, f'\"{scene}\" is already visible.'
        self._active_scenes.append(scene)
        current_scene = self.scenes[scene]
        
        if current_scene.UI_elements:
            current_scene.UI_elements.hidden = False
        
        if on_show := current_scene.on_show:
            on_show()
        
    def hide_scene(self, scene: str):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        assert scene in self._active_scenes, f'\"{scene}\" is already invisible.'
        self._active_scenes.remove(scene)
        current_scene = self.scenes[scene]
        
        if current_scene.UI_elements:
            current_scene.UI_elements.hidden = True
        
        if on_hide := current_scene.on_hide:
            on_hide()
        
    def clear_active_scenes(self):
        for scene in self._active_scenes:
            self.hide_scene(scene)
        self._active_scenes.clear()
        
    @property
    def get_active_scenes(self):
        return self._active_scenes

    def switch_scene(self, scene: str):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self.clear_active_scenes()
        self.show_scene(scene)
    
    def draw(self, *args, **kwargs):        
        for scene in self._active_scenes:
            
            current_scene = self.scenes[scene]
            on_draw = current_scene.draw_callback
            if self._active_scenes and on_draw:
                on_draw()
            
            if UI_elements := current_scene.UI_elements:
                UI_elements.draw(*args, **kwargs)
            
    def update(self, dt):
        for scene in self._active_scenes:
            
            current_scene = self.scenes[scene]
            on_update = current_scene.update_callback
            if self._active_scenes and on_update:
                on_update()
            
            if UI_elements := current_scene.UI_elements:
                UI_elements.update(dt)

@dataclass
class InputEvent:
    type: any
    callback: callable
    
class InputManager:
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
                
class LevelManager:
    def __init__(self):
        self.entities = ActorContainer()
        self.world = []
    
    def load_level(self, f):
        pass
    
    def save_level(self, f):
        pass
                
input_manager = InputManager()
scene_manager = SceneManager()

class GameManager:
    def __init__(self):
        self._input_manager = InputManager()
        self._scene_manager = SceneManager()
        self._level_manager = LevelManager()