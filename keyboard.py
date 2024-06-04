class keyManager:
    def __init__(self):
        self.callbacks = []
    
    def subscribe(self, callback):
        self.callbacks.append(callback)
        
    def unsubscribe(self, callback):
        self.callbacks.remove(callback)
        
    def set_callback(self, callback):
        index = self.callbacks.index(callback)
        self.callbacks[index], self.callbacks[-1] = self.callbacks[-1], self.callbacks[index]
        
    def on_key_down(self, key, unicode):
        self.callbacks[-1](key, unicode)