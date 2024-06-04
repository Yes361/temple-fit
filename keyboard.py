from pgzero.builtins import keyboard, keys

class keyManager:
    """
    jksadoasdksadjasdjksadjaskdad
    """
    KEY_DOWN = 0
    KEY_HOLD = 1
    def __init__(self):
        self._callbacks = {keyManager.KEY_DOWN: [], keyManager.KEY_HOLD: []}
    
    def subscribe(self, callback, type):
        self._callbacks[type].append(callback)
        
    def unsubscribe(self, callback):
        for key in self._callbacks.keys():
            try:
                self._callbacks[key].remove(callback)
                break
            except ValueError:
                continue
    
    def on_key_down(self, key, unicode):
        for callback in self._callbacks[keyManager.KEY_DOWN]:
            callback(key, unicode)
        
    def on_key_hold(self):
        for callback in self._callbacks[keyManager.KEY_HOLD]:
            callback()