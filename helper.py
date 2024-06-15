from pgzero.builtins import Actor, sounds, animate, Rect
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

CACHED_DIALOGUE = read_dialogue_lines(r'assets/Dialogue')

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
    
    @hidden.getter
    def hidden(self):
        if not (self, '_hidden'):
            self._hidden = False
        return self._hidden

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
        self.gif_name = None
        self.time_elapsed = 0
        self.opacity = opacity
        
        removed_kwargs = {}
        for key in kwargs.copy():
            if key not in Actor._EXPECTED_INIT_KWARGS:
                removed_kwargs[key] = kwargs.pop(key)
        
        super().__init__(*args, **kwargs)
        if dims is not None:
            self.dims = dims
            
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
        self._dims = dims
        self.width, self.height = dims
        self._surf = pygame.transform.scale(self._surf, dims)
    
    def draw(self, *args, **kwargs):
        if self._surf.get_alpha() != self.opacity:
            self._surf.set_alpha(self.opacity)
            
        if not self.hidden:
            super().draw()
    
    def is_animation_available(self):
        return type(self.images) == list and len(self.images) > 0
    
    @property
    def image_name(self):
        return self.image
    
    @image_name.setter
    def image_name(self, new_image):
        if new_image != self.image:
            self.image = new_image
            
    @property
    def anim(self):
        return self.images
    
    @anim.setter
    def anim(self, anim):
        if anim != self.images:
            self.images = anim
            
    def update(self, dt):
        self.time_elapsed += dt
        self.scale = self.scale # HACK
        if self.is_animation_available():
            if self._is_playing_gif:
                self.animate_gif()
            elif self.gif_name is None:
                self.animate()
                
    def animate_starting_targets(self, duration=1, tween='linear', on_finished=1, **kwargs):
        saved_attributes = {}
        for attr in kwargs:
            saved_attributes[attr] = getattr(self, attr)
            setattr(self, attr, kwargs[attr])
        
        self.anim_instance = animate(self, tween, duration, **saved_attributes)
                
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
        if not self.is_animation_available():
            return
        
        self.image = self.images[-1]
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

class Rect(Rect, AbstractActor):
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
    def __init__(self, pos=(0, 0), /, *, hidden=False, on_show=None, on_hide=None, **kwargs):
        self._actor_list: Dict[any, Type[Actor | GUIElement | ActorContainer]] = {}
        self.hidden = hidden
        self.on_enter = on_show
        self.on_exit = on_hide
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
        
        x_avg = 0
        for actor in self._actor_list.values():
            x_avg += actor.x
        x_avg /= len(self._actor_list)
        self._x = x_avg
        
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
        
        y_avg = 0
        for actor in self._actor_list.values():
            y_avg += actor.y
        y_avg /= len(self._actor_list)
        self._y = y_avg
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
            
    def offset(self, pos):
        dx, dy = pos
        self.x += dx
        self.y += dy
            
    # TODO: Implement on_show and on_hide for Actors and ActorContainer
    # def show(self, *args, **kwargs):
    #     if callable()
    
    # def hide(self):
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

class GUIElement(AbstractActor):
    @abstractmethod
    def on_click(self, pos, button) -> bool:
        pass
    
    @abstractmethod
    def on_hover(self) -> bool:
        pass
    
    @abstractmethod
    def on_hold(self) -> bool:
        pass
        
if __name__ == '__main__':
    # extract_gif_frames(r'assets/gifs/outro_card.gif', 'images', 'outro_card') 
    # print(read_dialogue_lines(r'assets/Dialogue'))
    # lower_case_files(r'images')
    print(CACHED_DIALOGUE)