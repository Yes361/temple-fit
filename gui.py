from pgzero.builtins import Actor
import weakref

class button(Actor):
    """
    asds
    """
    def __init__(self, *args, **kwargs):
        if 'callback' not in kwargs:
            raise Exception('no callback')
        
        self.callback = weakref.ref(kwargs.pop('callback'))
        self.hover_images = kwargs.pop('hover')
        self.hold_images = kwargs.pop('hold')
        self.click_images = kwargs.pop('click')
        
        super.__init__(*args, **kwargs)
        
    def on_hover(self):
        pass
    
    def on_hold(self):
        pass
    
    def on_click(self):
        self.callback()
        
class SceneManager:
    """
    
    """
    def __init__(self):
        self.scenes = {}
    
    def add_scene(self, scene_name, actor_list, callback: callable = None):
        self.scenes[scene_name] = (actor_list, callback)
        
    def switch_scenes(self):
        pass