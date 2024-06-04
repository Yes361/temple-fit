from actor import Actor

class button(Actor):
    """
    asds
    """
    def __init__(self, *args, **kwargs):
        if 'callback' not in kwargs:
            raise Exception('no callback')
        
        self.callback = kwargs.pop('callback')
        self.hover_images = kwargs.pop('hover')
        self.hold_images = kwargs.pop('hold')
        self.click_images = kwargs.pop('click')
        
        super().__init__(*args, **kwargs)
        
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
        self.callbacks = {}
        self.current_scene = None
    
    def add_scene(self, scene_name, actor_list, callback: callable = None):
        actor_list.hidden = True
        self.scenes[scene_name] = actor_list
        self.callbacks[scene_name] = callback
        
    def set_scene(self, scene_name):
        if scene_name not in self.scenes:
            return
        
        for scene in self.scenes.keys():
            self.scenes[scene].hidden = not scene == scene_name
        
        if fn := self.callbacks[scene_name]:
            fn()
            
    def draw_scenes(self):
        for scene in self.scenes.values():
            scene.draw()