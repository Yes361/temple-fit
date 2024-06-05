from dataclasses import dataclass
from utils import ActorContainer
from typing import Dict

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
    
    """
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self._current_scene: str = None
    
    def add_scene(self, scene_name, update_callback: callable, draw_callback: callable, UI_elements: ActorContainer=None):
        self.scenes[scene_name] = Scene(update_callback, draw_callback, UI_elements)
            
    def remove_scene(self, scene_name: str):
        self.scenes.pop(scene_name)

    def set_scene(self, scene_name: str):
        self._current_scene = scene_name
        
    @property
    def get_scene(self):
        return self._current_scene

    def switch_scene(self, scene_name: str):
        self._current_scene = scene_name
        for name, scene in self.scenes.items():
            if scene.UI_elements:
                
                if name == scene_name:
                    self.show_scene(name)
                else:
                    self.hide_scene(name)
            
    def show_scene(self, scene_name: str):
        self.scene_UI[scene_name].hidden = False
        
    def hide_scene(self, scene_name: str):
        self.scene_UI[scene_name].hidden = True
    
    def draw(self, *args, **kwargs):
        current_scene = self.scenes[self._current_scene]
        on_draw = current_scene.draw_callback
        if self._current_scene and on_draw:
            on_draw()
        
        if UI_elements := current_scene.UI_elements:
            UI_elements.draw(*args, **kwargs)
        
    def update(self, dt):
        current_scene = self.scenes[self._current_scene]
        on_update = current_scene.update_callback
        if self._current_scene and on_update:
            on_update()
        
        if UI_elements := current_scene.UI_elements:
            UI_elements.update(dt)
            
class InputManager(EventManager):
    """
    jksadoasdksadjasdjksadjaskdad
    """
    KEY_DOWN = 0
    KEY_HOLD = 1
    MAX_EVENTS = 2
    def __init__(self):
        self._group = None
        self._callbacks = [[] for i in range(InputManager.MAX_EVENTS)]
    
    def subscribe(self, group, callback, type):
        self._callbacks[type].append((group, callback))
        
    def unsubscribe(self, group, callback):
        for callbacks in self._callbacks:
            if (group, callback) in callbacks:
                callbacks.remove((group, callback))
                break
    
    def clear_group(self):
        self._group = None
    
    def set_group(self, group):
        self._group = group
    
    def filter_callback(self, type):
        for group, callback in self._callbacks[type]:
            if self._group == None or self._group == group:
                yield callback
    
    def on_key_down(self, key, unicode):
        for callback in self.filter_callback(InputManager.KEY_DOWN):
            if callback:
                callback(key, unicode)
        
    def on_key_hold(self, dt):
        for callback in self.filter_callback(InputManager.KEY_HOLD):
            if callback:
                callback()
                
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