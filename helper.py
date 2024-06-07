from pgzero.builtins import Actor
from pgzhelper import Actor
from typing import List, Any
from abc import abstractmethod
from PIL import Image
import pygame
import os
import re

def list_actor_attributes(actor: Actor, field_name: List[str]) -> dict[str, Any]:
    """
    @param actor
    @param field_name The desired fields
    @return: A dictionary containing the values of the desired fields
    """
    field = {}
    for name in field_name:
        field[name] = getattr(actor, name)
    return field

def require_kwargs(fields, kwargs, error_msg = '%s is required'):
    """
    @raises An error if a required field was not passed
    """
    for field in fields:
        assert field in kwargs, error_msg % field

def lower_case_files(directory):
    for file in os.listdir(directory):
        os.rename(rf'{directory}\{file}', rf'{directory}\{file.lower()}')
        
def extract_gif_frames(read_file, out_dir, prefix):
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

def match_file_prefix(prefix, file):
    return re.match(rf'{prefix}(?:_frame)', file) != None

def extract_frames_from_gif(prefix):
    gif_frames = []
    for file in os.listdir('images'):
        if match_file_prefix(prefix, file):
            gif_frames.append(file)
    return gif_frames

def move_assets_into_images(asset_folder):
    for file in asset_folder:
        asset_path = f'{asset_folder}/{file}'
        if os.path.isdir(asset_path):
            move_assets_into_images(asset_path)
        else:
            os.rename(asset_path, f'images/{file}')
            
def delete_gif(prefix):
    for file in os.listdir('images'):
        if match_file_prefix(prefix, file):
            os.remove(f'images/{file}')

def load_gifs(path):
    gifs = os.listdir(path)
    gif_images = {}
    for file in gifs:
        file_name = file.removesuffix('.gif')
        gif_images[file_name] = extract_frames_from_gif(file_name)
    return gif_images

cached_gifs = load_gifs(r'assets/gifs')

class ActorBase:
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

class Actor(Actor, ActorBase):
    """
    Revised Version of Actor Class
    
    Now supports passing custom properties at initialization, update(dt), and reset()
    """
    _EXPECTED_INIT_KWARGS = set(['pos', 'topleft', 'bottomleft', 'topright', 'bottomright',
    'midtop', 'midleft', 'midbottom', 'midright', 'center'])
    
    def __init__(self, *args, **kwargs):
        self.hidden = False
        self.iterations = -1
        self._is_playing_gif = False
        self.gif_name = None
        
        keys = list(kwargs.keys())
        for key in keys:
            if key not in Actor._EXPECTED_INIT_KWARGS:
                setattr(self, key, kwargs[key])
                kwargs.pop(key)
        
        super().__init__(*args, **kwargs)
        
    def resize(self, dims):
        self._surf = pygame.transform.scale(self._surf, dims)
    
    def draw(self, *args, **kwargs):
        if not self.hidden:
            super().draw()
    
    def is_animation_available(self):
        return type(self.images) == list and len(self.images) > 0
    
    def update(self, dt):
        if self.is_animation_available():
            if self._is_playing_gif:
                self.animate_gif()
            elif self.gif_name is None:
                self.animate()
                
    def pause_gif(self, play=None):
        if play is not None:
            self._is_playing_gif = not play
        else:
            self._is_playing_gif = not self._is_playing_gif
    
    def animate_gif(self):
        if self.iterations == 0:
            self.skip_gif()

        elif super().animate() == len(self.images) - 1 and self.iterations > 0:
            self.iterations -= 1
    
    def stop_gif(self):
        self.iterations = 0
        self.images.clear()
        self._is_playing_gif = False
        self.gif_name = None
        
    def skip_gif(self):
        self.stop_gif()
        if self._gif_on_finish:
            self._gif_on_finish()
    
    def play_gif(self, gif, iterations = -1, fps=24, on_finish: callable = None,):
        self.gif_name = gif
        self.images = cached_gifs[gif]
        self.fps = fps
        self.iterations = iterations
        self._is_playing_gif = True
        self._gif_on_finish = on_finish
        

class ActorContainer(ActorBase):
    """
    Actor Container is a list of Actors - Similar to Group() in CMU Academy
    """
    def __init__(self, *args):
        self.actor_list = args[0] if type(args[0]) == list else args
        self.hidden = False
  
    def add_actor(self, actor):
        self.actor_list.append(actor)
        return actor
    
    def remove_actor(self, actor):
        self.actor_list.remove(actor)
        
    # TODO: z-index shenanigans
    # def set_actor_zindex(self, actor):
    #     pass
        
    def colliderect(self, other_actor):
        for actor in self.actor_list:
            if actor.colliderect(other_actor):
                return True
        return False

    def draw(self, *args, **kwargs):
        if self.hidden:
            return
        
        for actor in self.actor_list:
            actor.draw(*args, **kwargs)
    
    def update(self, dt):
        for actor in self.actor_list:
            actor.update(dt)
            
    def __iter__(self):
        return iter(self.actor_list)
    
class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        elif getattr(cls, '_instance_error', False):
            raise Exception(f'{type(cls._instance).__name__} is already initialized.')
        return cls._instance
    
if __name__ == '__main__':
    extract_gif_frames(r'assets/gifs/outro_card.gif', 'images', 'outro_card') 