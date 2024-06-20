from abc import ABC, abstractmethod
from helper import ActorContainer
from typing import *
import pygame

class Scene:
    """
    Base Scene class.

    This class represents a generic scene in the game. Each specific scene in the game should
    inherit from this class and implement the required abstract methods to define the scene's behavior.
    """
    def __init__(self, scene, *args, **kwargs):
        game_manager.subscribe(scene, self)
        self.globals = kwargs
    
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
        pass
    
    @abstractmethod
    def on_mouse_move(self, pos, rel, buttons):
        pass
    
    @abstractmethod
    def on_mouse_hold(self, pos, buttons):
        pass
    
    @abstractmethod
    def on_mouse_up(self, pos, buttons):
        pass
    
    @abstractmethod
    def on_mouse_hover(self, pos):
        pass
    
    @abstractmethod
    def on_music_end(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass
    
class GameManager:
    """
    Handles Scene Transition/Visibility and Draw/Update Callbacks.

    The GameManager is responsible for managing the lifecycle of scenes, including transitions, visibility,
    and handling updates and drawing. It maintains a registry of scenes and manages which scenes are active
    and visible at any given time.
    """
    def __init__(self, predefined_scenes={}):
        self.scenes: Dict[any, Type[Scene]] = predefined_scenes
        self._active_scenes: List[str] = []
        self._event_stack = []
        
    def subscribe(self, scene_name, scene: Type[Scene]):
        """
        Register a new scene with the given name.

        @params
        scene_name : str
            The name to register the scene under.
        scene : Type[Scene]
            The scene instance to register.
        """
        assert scene_name not in self.scenes, f'\"{scene_name}\" is already subscribed.'
        self.scenes[scene_name] = scene

    def unsubscribe(self, scene):
        """
        Unregister an existing scene.

        @params
        scene : str
            The name of the scene to unregister.
        """
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self.scenes.pop(scene)
        
    def list_all_scenes(self):
        """
        Return a list of all registered scene names.

        @returns
        List[str]
            A list of registered scene names.
        """
        return self.scenes.keys()

    def show_scene(self, scene, *args, switch_event_scene: bool = True, **kwargs):
        """
        Make a registered scene active and visible.

        @params
        scene : str
            The name of the scene to show.
        switch_event_scene : bool
            Whether to switch the event handling to this scene (default is True).
        *args : tuple
            Additional positional arguments to pass to the scene's on_show method.
        **kwargs : dict
            Additional keyword arguments to pass to the scene's on_show method.
        """
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        assert scene not in self._active_scenes, f'\"{scene}\" is already visible.'
        
        if switch_event_scene:
            self._event_stack.append(scene)
        
        self._active_scenes.append(scene)
        self.scenes[scene].on_show(*args, **kwargs)
        
    def hide_scene(self, scene, *args, **kwargs):
        """
        Make an active scene invisible.

        @params
        scene : str
            The name of the scene to hide.
        *args : tuple
            Additional positional arguments to pass to the scene's on_hide method.
        **kwargs : dict
            Additional keyword arguments to pass to the scene's on_hide method.
        """
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        assert scene in self._active_scenes, f'\"{scene}\" is already invisible.'
        
        self._active_scenes.remove(scene)
        
        self.scenes[scene].on_hide(*args, **kwargs)
        if len(self._event_stack) > 0:
            self._event_stack.pop()
        
    def clear_active_scenes(self):
        """
        Hide all currently active scenes.
        """
        for scene in self._active_scenes:
            self.hide_scene(scene)
        self._active_scenes.clear()
        
    def get_active_scenes(self):
        """
        Return a list of currently active scene names.

        @returns:
        List[str]
            A list of active scene names.
        """
        return self._active_scenes

    def switch_scene(self, scene, *args, **kwargs):
        """
        Switch to a new scene, making it the only active scene.

        @params
        scene : str
            The name of the scene to switch to.
        *args : tuple
            Additional positional arguments to pass to the scene's on_show method.
        **kwargs : dict
            Additional keyword arguments to pass to the scene's on_show method.
        """
        assert scene not in self._active_scenes, f'\"{scene}\" is already active.'
        assert scene in self.scenes, f'\"{scene}\" doesn\'t exist.'
        self.clear_active_scenes()
        
        if len(self._event_stack) > 0:
            self._event_stack.pop()
        self.show_scene(scene, *args, switch_event_scene=True, **kwargs)
        
    def reset(self):
        for scene in self.scenes.values():
            scene.reset()
    
    def draw(self, screen):      
        """
        Draw all active scenes onto the given screen.

        @params
        screen : pgzero.screen.Screen
            The screen or surface to draw the scenes on.
        """  
        for scene in self._active_scenes:
            
            current_scene = self.scenes[scene]
            current_scene.on_draw(screen)
            
    def update(self, dt):
        """
        Update all active scenes.

        @params
        dt : float
            The time delta since the last update.
        """
        for scene in self._active_scenes:
            
            current_scene = self.scenes[scene]
            current_scene.on_update(dt)
            
        current_event = self.current_event()
        self.scenes[current_event].on_mouse_hold(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        self.scenes[current_event].on_mouse_hover(pygame.mouse.get_pos())
        self.scenes[current_event].on_key_hold(dt)
                
    def current_event(self):
        """
        Return the name of the scene that should currently handle input events.

        @returns:
        str
            The name of the current event scene.
        """
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