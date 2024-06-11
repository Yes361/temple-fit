from pgzero.builtins import Actor, sounds
from pgzhelper import Actor
from typing import *
from abc import abstractmethod
from PIL import Image
import weakref
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

def play_sound(sound: str):
    getattr(sounds, sound).play()

# TODO: Sync Assets and Images Folder function
def sync_assets_and_images(asset_folder_path):
    pass

CACHED_GIFS = load_gifs(r'assets/gifs')

def read_dialogue_lines(asset_folder_path):
    dialogue = {}
    for file in os.listdir(asset_folder_path):
        file_name = re.match(r'^\d+_(.+)\.txt$', file).group(1)
        dialogue_lines = open(os.path.join(asset_folder_path, file), 'r').read().split('\n')
        dialogue[file_name] = list(filter(lambda line: (line != '\n') and (line != ''), dialogue_lines))
    return dialogue

class AbstractActor:
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
    
    @abstractmethod
    def hide(self):
        pass
    
    @abstractmethod
    def show(self):
        pass
    
    @property
    def hidden(self) -> bool:
        return self._hidden
    
    @hidden.setter
    def hidden(self, value):
        self._hidden = value
        if value:
            self.hide()
        else:
            self.show()

class Actor(Actor, AbstractActor):
    """
    Revised Version of Actor Class
    
    Now supports passing custom properties at initialization, update(dt), and reset()
    """
    _EXPECTED_INIT_KWARGS = set(['pos', 'topleft', 'bottomleft', 'topright', 'bottomright',
    'midtop', 'midleft', 'midbottom', 'midright', 'center'])
    
    def __init__(self, *args, **kwargs):
        self.hidden = False
        self.iterations = 0
        self._is_playing_gif = False
        self.gif_name = None
        self.time_elapsed = 0
        self.opacity = 255
        
        removed_kwargs = {}
        for key in kwargs.copy():
            if key not in Actor._EXPECTED_INIT_KWARGS:
                removed_kwargs[key] = kwargs.pop(key)
        
        super().__init__(*args, **kwargs)
        
        for key in removed_kwargs:
            setattr(self, key, removed_kwargs[key])
        
    def resize(self, dims):
        self.width, self.height = dims
        self._surf = pygame.transform.scale(self._surf, dims)
    
    def draw(self, *args, **kwargs):
        if self._surf.get_alpha() != self.opacity:
            self._surf.set_alpha(self.opacity)
            
        if not self.hidden:
            super().draw()
    
    def is_animation_available(self):
        return type(self.images) == list and len(self.images) > 0
    
    def update(self, dt):
        self.time_elapsed += dt
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
        if self._gif_on_finish is not None:
            self._gif_on_finish()
    
    def play_animation(self, images, fps, iterations):
        self.images = images
        self.fps = fps
        self.iterations = iterations
    
    def play_gif(self, gif, iterations = -1, fps=24, on_finish: callable = None,):
        self.gif_name = gif
        self._is_playing_gif = True
        self._gif_on_finish = on_finish
        self.play_animation(CACHED_GIFS[gif], fps, iterations)
        
    def get_weak_ref(self):
        return weakref.proxy(self)  
        
class ActorContainer(AbstractActor):
    """
    Actor Container is a list of Actors - Similar to Group() in CMU Academy
    """
    def __init__(self, **kwargs):
        self._actor_list: Dict[any, Type[Actor | GUIElement | ActorContainer]] = {}
        self.hidden = kwargs.pop('hidden', False)
        self.on_enter = kwargs.pop('on_show', None)
        self.on_exit = kwargs.pop('on_hide', None)
        self._opacity = 255
        for name, actor in kwargs.items():
            self.add(name, actor)
            
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
        Adds an Actor to the Actor Container
        @returns: Weak reference of the actor that is to be used
        """
        assert name not in self._actor_list, f'\"{name}\" is already added.'
        self._actor_list[name] = actor
        return self.get_weak_actor(name)
    
    def remove(self, name: any):
        assert name in self._actor_list, f'\"{name}\" doesn\'t exist.'
        actor = self._actor_list.pop(name)
        del actor
        
    # TODO: z-index shenanigans
    # def set_actor_zindex(self, name):
    #     pass
        
    def colliderect(self, other_actor: Type[AbstractActor]):
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
            
    # TODO: Implement on_show and on_hide for Actors and ActorContainer
    # def on_show(self, *args, **kwargs):
    #     if callable()
    
    # def on_hide(self):
    #     pass
            
    def clear(self):
        for name in self._actor_list.copy():
            actor = self._actor_list.get(name)
            if isinstance(actor, ActorContainer):
                actor.clear()
                continue
            
            self.remove(name)
            
    def __getattr__(self, property):
        if property in self.__dict__:
            return self.__dict__[property]
        elif property in self._actor_list:
            # setattr(self, property, ) # Cache result?
            return self.get_weak_actor(property)
        else:
            AttributeError(f'{property} is not in {self.__class__.__name__}')
            
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

class GUIElement(Actor):
    @abstractmethod
    def on_click(self, pos, button):
        pass
    
    @abstractmethod
    def on_hover(self):
        pass
    
    @abstractmethod
    def on_hold(self):
        pass
        
if __name__ == '__main__':
    # extract_gif_frames(r'assets/gifs/outro_card.gif', 'images', 'outro_card') 
    print(read_dialogue_lines(r'assets/Dialogue'))