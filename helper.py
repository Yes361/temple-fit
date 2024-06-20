"""
This file contains various helper classes and functions essential for game
development, including Actor, ActorContainer, Rect, Music, and constants for
cached dialogue and voice lines.
"""

from pgzero.builtins import Actor, animate, Rect, music
from pgzhelper import Actor
from typing import *
from abc import abstractmethod
from PIL import Image
import weakref
import pygame
import os
import re

def lower_case_files(directory):
    """
    Converts all filenames in a directory to lowercase.
    
    @params:
        directory (str): The path to the directory.
    """
    for file in os.listdir(directory):
        os.rename(rf'{directory}\{file}', rf'{directory}\{file.lower()}')
        
def extract_gif_frames(read_file, out_dir, prefix):
    """
    Extracts frames from a GIF file and saves them as PNG files.
    
    @params:
        read_file (str): The path to the GIF file.
        out_dir (str): The directory to save the frames.
        prefix (str): The prefix for the output filenames.
    """
    idx = 0
    with Image.open(read_file) as im:
        im.seek(1)
        digit_length = len(str(im.n_frames))
        
        try:
            while True:
                img = im.seek(im.tell() + 1)
                idx += 1
                im.save(rf'{out_dir}/{prefix}_frame_{idx:0{digit_length}d}.png')
        except EOFError:
            pass
        
def extract_voicelines(folder):
    """
    Extracts voice lines from a folder and categorizes them by scene.
    
    @params:
        folder (str): The path to the folder containing the voice lines.
        
    @returns:
        dict: A dictionary where keys are scene names and values are lists of voice line filenames.
    """
    scene = {}
    for file in os.listdir(folder):
        if scene_name := re.match(r'^(.+)_\d+\.mp3$', file):
            scene_name = scene_name.group(1)
            if scene_name not in scene:
                scene[scene_name] = []
            scene[scene_name].append(file)
    return scene

def match_file_prefix(prefix, file):
    """
    Matches a file prefix to a given string.
    
    @params:
        prefix (str): The prefix to match.
        file (str): The filename to check.
        
    @returns:
        bool: True if the prefix matches, otherwise False.
    """
    return re.match(rf'{prefix}(?:_frame)', file) != None

def extract_frames_from_gif(prefix):
    """
    Extracts frames from a GIF file given a prefix.
    
    @params:
        prefix (str): The prefix of the GIF file.
        
    @returns:
        List[str]: A list of frame filenames.
    """
    gif_frames = []
    for file in os.listdir('images'):
        if match_file_prefix(prefix, file):
            gif_frames.append(file)
    return gif_frames

def move_assets_into_images(asset_folder):
    """
    Moves assets from a folder into the 'images' directory.
    
    @params:
        asset_folder (str): The path to the asset folder.
    """
    for file in asset_folder:
        asset_path = f'{asset_folder}/{file}'
        if os.path.isdir(asset_path):
            move_assets_into_images(asset_path)
        else:
            os.rename(asset_path, f'images/{file}')
            
def delete_gif(prefix):
    """
    Deletes GIF frames with a specific prefix from the 'images' directory.
    
    @params:
        prefix (str): The prefix of the GIF frames to delete.
    """
    for file in os.listdir('images'):
        if match_file_prefix(prefix, file):
            os.remove(f'images/{file}')

def load_gifs(path):
    """
    Loads GIF files from a directory and extracts their frames.
    
    @params:
        path (str): The path to the directory containing GIF files.
        
    @returns:
        dict: A dictionary where keys are GIF names and values are lists of frame filenames.
    """
    gifs = os.listdir(path)
    gif_images = {}
    for file in gifs:
        file_name = file.removesuffix('.gif')
        gif_images[file_name] = extract_frames_from_gif(file_name)
    return gif_images


def read_dialogue_lines(asset_folder_path):
    """
    Reads dialogue lines from text files in a folder.
    
    @params:
        asset_folder_path (str): The path to the folder containing dialogue files.
        
    @returns:
        dict: A dictionary where keys are dialogue file names and values are lists of dialogue lines.
    """
    dialogue = {}
    for file in os.listdir(asset_folder_path):
        file_name = re.match(r'^(.+)_\d+\.txt$', file).group(1)
        dialogue_lines = open(os.path.join(asset_folder_path, file), 'r').read().split('\n')
        dialogue[file_name] = list(filter(lambda line: (line != '\n') and (line != ''), dialogue_lines))
    return dialogue

# Store GIFS, Dialogue, and Voice lines
CACHED_GIFS = load_gifs(r'assets/gifs')
CACHED_DIALOGUE = read_dialogue_lines(r'assets/Dialogue')
CACHED_VOICELINES = extract_voicelines(r'sounds')

class AbstractActor:
    """
    AbstractActor is an abstract base class that defines the interface for actors within the game.
    """
    @abstractmethod
    def draw(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def animate(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass

class Actor(Actor, AbstractActor):
    """
    Revised Version of Actor Class
    
    Now supports passing custom properties at initialization, update(dt), and reset()
    """
    _EXPECTED_INIT_KWARGS = set(['pos', 'topleft', 'bottomleft', 'topright', 'bottomright',
    'midtop', 'midleft', 'midbottom', 'midright', 'center'])
    
    def __init__(self, *args, hidden=False, opacity=255, dims=None, **kwargs):
        self.hidden = hidden
        self.iterations = 0
        self._is_playing_gif = False
        self._image_name = ''
        self._anim_instance = None
        self.gif_name = None
        self.time_elapsed = 0
        self.opacity = opacity
        
        # Save the custom properties
        removed_kwargs = {}
        for key in kwargs.copy():
            if key not in Actor._EXPECTED_INIT_KWARGS:
                removed_kwargs[key] = kwargs.pop(key)
        
        super().__init__(*args, **kwargs)
        if dims is not None:
            self.dims = dims
            
        # Set the custom properties
        for key in removed_kwargs:
            setattr(self, key, removed_kwargs[key])
        
    @property
    def dims(self):
        return self._dims
    
    @dims.setter
    def dims(self, value):
        self.resize(value)
        
    @dims.getter
    def dims(self):
        self._dims = self.width, self.height
        return self._dims
        
    def resize(self, dims):
        """
        Resizes the actor to the specified dimensions.
        
        @params:
            dims (tuple): The new dimensions for the actor.
        """
        self._dims = dims
        self.width, self.height = dims
        self._surf = pygame.transform.scale(self._surf, dims)
    
    def draw(self, *args, **kwargs):
        # Opacity
        if self._surf.get_alpha() != self.opacity:
            self._surf.set_alpha(self.opacity)
            
        if not self.hidden:
            super().draw()
    
    def is_animation_available(self):
        """
        Checks if animation is available for the actor.
        
        @returns:
            bool: True if animation is available, otherwise False.
        """
        return type(self.images) == list and len(self.images) > 0
    
    @Actor.image.setter
    def image(self, image):
        if self._image_name != image:
            # Thanks to https://gist.github.com/Susensio/979259559e2bebcd0273f1a95d7c1e79 for this trick
            super(Actor, type(self)).image.fset(self, image)
            self.scale = self.scale # HACK: Whenever a new image is set, scale isn't applied
            # Setting scale to itself seems to resolve the issue
            
    def update(self, dt):
        self.time_elapsed += dt
        # Plays an animation/gif
        if self.is_animation_available():
            if self._is_playing_gif:
                self.animate_gif()
            elif self.gif_name is None:
                self.animate()
                
    def animate_targets(self, duration=1, tween='linear', on_finished=None, **kwargs):
        """
        Animates the actor's properties from a preset value to their current values
        
        @params:
            duration (float): The duration of the animation in seconds.
            tween (str): The type of tweening to use. Default is 'linear'.
            on_finished (callable): The function to call when the animation is finished.
            **kwargs: The properties to animate and their target values. Formatted as (start, finish)
        """
        saved_attributes = {}
        for attr in kwargs:
            saved_attributes[attr] = getattr(self, attr)
            setattr(self, attr, kwargs[attr])
        
        self._anim_instance = animate(self, tween, duration, on_finished=on_finished, **saved_attributes)
                
    def pause_gif(self, play=None):
        """
        Toggle the play/pause state of a GIF animation. If the `play` parameter is provided,
        it explicitly sets the play state of the GIF. If `play` is not provided, it toggles
        the current play state.
        
        @params:
            play : bool, optional
        """
        if play is not None:
            self._is_playing_gif = not play
        else:
            self._is_playing_gif = not self._is_playing_gif
    
    def animate_gif(self):
        if self.iterations == 0:
            self.skip_gif()

        # Decrement iterations if a cycle was completed
        elif super().animate() == len(self.images) - 1 and self.iterations > 0:
            self.iterations -= 1
    
    def stop_gif(self):
        """
        Stops the GIF animation and clears the frames.
        """
        self.iterations = 0
        self.images.clear()
        self._is_playing_gif = False
        self.gif_name = None
        
    def skip_gif(self):
        """
        Skips to the last frame of the GIF animation.
        """
        # Return early if an animation isn't available
        if not self.is_animation_available():
            return
        
        self.image = self.images[-1]
        self.stop_gif()
        if self._gif_on_finish is not None:
            self._gif_on_finish()
    
    def play_animation(self, images, fps, iterations):
        """
        Plays a custom animation with specified frames per second and iterations.
        
        @params:
            images (list): A list of image frames.
            fps (int): Frames per second.
            iterations (int): Number of iterations. -1 for infinite loop.
        """
        self.images = images
        self.fps = fps
        self.iterations = iterations
    
    def play_gif(self, gif, iterations = -1, fps=24, on_finish: callable = None,):
        """
        Plays a GIF animation.
        
        @params:
            gif (str): The name of the GIF to play.
            iterations (int): Number of iterations. Default is -1 (infinite).
            fps (int): Frames per second. Default is 24.
            on_finish (callable, optional): Function to call when the animation finishes.
        """
        self.gif_name = gif
        self._is_playing_gif = True
        self._gif_on_finish = on_finish
        self.play_animation(CACHED_GIFS[gif], fps, iterations)
    
    def copy_basic_attr(self, other: Type[Actor], attrs=['scale']):
        """
        Copies basic attributes from another actor.
        
        @params:
            other (Actor): The other actor to copy attributes from.
            attrs (list): The list of attributes to copy. Default is ['scale'].
        """
        for attr in attrs:
            value = getattr(self, attr)
            setattr(self, attr, value)

class Rect(Rect, AbstractActor):
    """
    The better pgzero Rect, and shares some methods with Actor
    """
    def __init__(self, pos, dims, /, *, scale=1, fill=(255, 255, 255), border=(255, 255, 255)):
        self.fill = fill
        self.border = border
        self._pos = pos
        
        super().__init__(pos, dims)        
        
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self.x, self.y = pos
        
    def draw(self, screen):
        screen.draw.rect(self, self.border)
        screen.draw.filled_rect(self, self.fill)
        
class ActorContainer(AbstractActor):
    """
    Actor Container is a list of Actors - Similar to Group() in CMU Academy
    """
    def __init__(self, pos=(0, 0), /, *, hidden=False, **kwargs):
        """
        Initialize the object and add actors using keyword arguments.
        """
        self._actor_list: Dict[any, Type[Actor | GUIElement | ActorContainer]] = {}
        self.hidden = hidden
        self._opacity = 255
        self._x = 0
        self._y = 0
        self._pos = pos
        
        for name, actor in kwargs.items():
            self.add(name, actor)
    
    @property
    def x(self):
        return self._x
    
    @x.getter
    def x(self):
        self._x = 0
        if len(self._actor_list) == 0:
            return self._x
        
        # Get average x position
        x_avg = 0
        for actor in self._actor_list.values():
            x_avg += actor.x
        self._x = x_avg / len(self._actor_list)
        
        return self._x
    
    @x.setter
    def x(self, value):
        dx = value - self.x
        for actor in self._actor_list.values():
            actor.x += dx
    
    @property
    def y(self):
        return self._y
    
    @y.getter
    def y(self):
        self._y = 0
        if len(self._actor_list) == 0:
            return self._y
        
        # Get average y position
        y_avg = 0
        for actor in self._actor_list.values():
            y_avg += actor.y
        self._y = y_avg / len(self._actor_list)
        return self._y
    
    @y.setter
    def y(self, value):
        dy = value - self.y
        for actor in self._actor_list.values():
            actor.y += dy
    
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, value: Tuple):
        self.x, self.y = value
        self._pos = value
            
    @property
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        for actor in self._actor_list.values():
            actor.opacity = value
  
    def add(self, name: any, actor: Type[AbstractActor]):
        """
        Adds an Actor to the ActorContainer.
        
        @params:
            name (any): The identifier for the actor.
            actor (AbstractActor): The actor to add.
        
        @returns:
            weakref.proxy: A weak reference to the added actor.
        """
        assert name not in self._actor_list, f'\"{name}\" is already added.'
        self._actor_list[name] = actor
        return self.get_weak_actor(name)
    
    def remove(self, name: any):
        assert name in self._actor_list, f'\"{name}\" doesn\'t exist.'
        actor = self._actor_list.pop(name)
        del actor
        
    def has(self, name: any) -> bool:
        """
        Checks if the name exists in the ActorContainer
        
        @params:
            name (any): The identifier for the actor
            
        @returns:
            bool: True if the name exists
        """
        return name in self._actor_list
        
    def colliderect(self, other_actor: Type[AbstractActor]):
        """
        Checks if any actor in the container collides with another actor.
        
        @params:
            other_actor (AbstractActor): The other actor to check collision with.
        
        @returns:
            bool: True if any actor collides with the other actor, False otherwise.
        """
        for actor in self._actor_list.values():
            if actor.colliderect(other_actor):
                return True
        return False

    def draw(self, *args, **kwargs):
        if self.hidden:
            return
        
        for actor in self._actor_list.values():
            actor.draw(*args, **kwargs)
    
    def update(self, dt, *args, **kwargs):
        for actor in self._actor_list.values():
            actor.update(dt, *args, **kwargs)
   
    def clear(self):
        """
        Clears all the Actors in the ActorContainer
        """
        for name in self._actor_list.copy():
            actor = self._actor_list.get(name)
            if isinstance(actor, ActorContainer):
                actor.clear()            
            self.remove(name)
            
    def on_click(self, pos, button):
        if self.hidden:
            return

        for actor in self._actor_list.values():
            actor.on_click(pos, button)
            
            
    def __getattr__(self, property):
        if property in self.__dict__:
            return self.__dict__[property]
        # Allow Actors to be accessed as custom properties
        elif property in self._actor_list:
            # setattr(self, property, ) # Cache result?
            return self.get_weak_actor(property)
        else:
            raise AttributeError(f'{property} is not in {self.__class__.__name__}')
            
    def get_weak_actor(self, item):
        assert item in self._actor_list, f'\"{item}\" is not added.'
        return weakref.proxy(self._actor_list[item])
        
    def __iter__(self):
        return iter(self._actor_list.values())
    
    def __getitem__(self, item):
        return self.get_weak_actor(item)
    
    def __setitem__(self, item, value):
        self._actor_list[item] = value
        
    def __len__(self):
        return len(self._actor_list)
    
class Music:
    """
    The Better Music Class. Keeps track of the piece that is currently playing
    (But doesn't support queuing and fadeout)
    """
    _current = None  
    # queue = music.queue
    pause = music.pause
    unpause = music.unpause
    # fadeout = music.fadeout
    set_volume = music.set_volume
    get_volume = music.get_volume
    set_pos = music.set_pos
    get_pos = music.get_pos
    
    def play(name):
        music.play(name)
        Music._current = name
        
    def play_once(name):
        music.play_once(name)
        Music._current = name
        
    def stop():
        music.stop()
        Music._current = None
    
    def is_playing(name):
        # music.is_playing is useless (its what prompted overwriting the music builtin)
        return music.is_playing('') and Music._current == name
    
    
class GUIElement(AbstractActor):
    """
    Abstract base class for defining GUI elements with clickable, hoverable, and holdable behaviors.
    """
    @abstractmethod
    def on_click(self, pos, button) -> bool:
        pass

    @abstractmethod
    def on_hover(self) -> bool:
        pass
    
    @abstractmethod
    def on_hold(self) -> bool:
        pass

def schedule(on_finish, duration):
    """
    Patch for the Clock Scheduler, which doesn't work outside of main.py
    """
    dummy_object = Actor('battle_scene_tab')
    # Using the delay and callback to emulate schedule
    return animate(dummy_object, duration=duration, on_finished=on_finish, pos=(0, 0))
        
if __name__ == '__main__':
    print(CACHED_GIFS)