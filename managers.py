from dataclasses import dataclass
from utils import ActorContainer
from typing import Dict, Tuple, List
from constants import Constants
import pygame

class EventManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EventManager, cls).__new__(cls)
        return cls._instance
    
    def __del__(self):
        EventManager._instance = None
    
@dataclass
class Scene: 
    update_callback: callable = None
    draw_callback: callable = None
    UI_elements: ActorContainer = None

class SceneManager(EventManager): 
    """
    Handles Scene Transition/Visibility and Draw/Update Callbacks
    """
    def __init__(self, predefined_scenes={}):
        self.scenes: Dict[str, Scene] = predefined_scenes
        self._active_scenes: set[str] = set()
    
    def subscribe(self, scene: str, update_callback: callable, draw_callback: callable, UI_elements: ActorContainer=None):
        assert scene not in self.scenes, f'\"{scene}\" is already subscribed.'
        self.scenes[scene] = Scene(update_callback, draw_callback, UI_elements)
            
    def unsubscribe(self, scene: str):
        if scene in self.scenes:
            self.scenes.pop(scene)

    def show_scene(self, scene: str):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self._active_scenes.add(scene)
        self.scenes[scene].UI_elements.hidden = False
        
    def hide_scene(self, scene: str):
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self._active_scenes.remove(scene)
        self.scenes[scene].UI_elements.hidden = True
        
    def clear_active_scenes(self):
        self._active_scenes.clear()
        
        for _, scene in self.scenes.items():
            if scene.UI_elements:
                scene.UI_elements.hidden = True
        
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
    group_identifer: any = None
    
class InputManager(EventManager):
    """
    jksadoasdksadjasdjksadjaskdad
    """
    EVENTS = [Constants.KEY_UP, Constants.KEY_DOWN, Constants.KEY_HOLD, Constants.MOUSE_HOVER]
    def __init__(self):
        self._group = None
        self._callbacks: List[InputEvent] = []
        self._group_id = 0
    
    def subscribe(self, type, callback, group_identifier=None):
        self._callbacks.append(InputEvent(type, callback, group_identifier))
        
    def unsubscribe(self, callback=None, group=None):
        for event in self._callbacks:
            if callback and group:
                if event.callback == callback and event.group_identifer == group:
                    self._callbacks.remove(event)
            elif callback:
                if event.callback == callback:
                    self._callbacks.remove(event)
            elif group:
                if event.group_identifer == group:
                    self._callbacks.remove(event)
            else:
                raise Exception('pluh')
    
    def clear_group(self):
        self._group = None
    
    def set_group(self, group):
        self._group = group
    
    def filter_events(self, type, *args, **kwargs):
        for event in self._callbacks:
            if event.type == type and (self._group == None or self._group == event.group_identifer) and event.callback:
                event.callback(*args, **kwargs)
    
    def on_key_down(self, key, unicode):
        self.filter_events(Constants.KEY_DOWN, key, unicode)
        
    def on_key_up(self, key, unicode):
        self.filter_events(Constants.KEY_UP, key, unicode)
    
    def on_key_hold(self, dt):
        self.filter_events(Constants.KEY_HOLD)
        
    def on_mouse_hover(self, pos):
        self.filter_events(Constants.MOUSE_HOVER, pos)
        
                
class LevelManager(EventManager):
    def __init__(self):
        self.entities = ActorContainer()
        self.world = []
    
    def load_level(self, f):
        pass
    
    def save_level(self, f):
        pass
                
input_manager = InputManager()
scene_manager = SceneManager()

class GameManager(EventManager):
    def __init__(self):
        self._input_manager = InputManager()
        self._scene_manager = SceneManager()
        self._level_manager = LevelManager()