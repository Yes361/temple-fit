from managers import input_manager, scene_manager

class Game:
    def __init__(self):
        self._scene_manager = scene_manager
        self._input_manager = input_manager
    
    def start_game(self):
        pass