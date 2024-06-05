from utils import Actor, ActorContainer
import pgzero.game as game

class Item(Actor):
    pass    

class Slot(Actor):
    pass

class Inventory(ActorContainer):
    def __init__(self):
        self