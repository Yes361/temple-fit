from pgzero.builtins import keyboard, keys

class inputManager:
    """
    jksadoasdksadjasdjksadjaskdad
    """
    KEY_DOWN = 0
    KEY_HOLD = 1
    MAX_EVENTS = 2
    def __init__(self):
        self._group = None
        self._callbacks = [[] for i in range(inputManager.MAX_EVENTS)]
    
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
        for callback in self.filter_callback(inputManager.KEY_DOWN):
            if callback:
                callback(key, unicode)
        
    def on_key_hold(self, dt):
        for callback in self.filter_callback(inputManager.KEY_HOLD):
            if callback:
                callback()