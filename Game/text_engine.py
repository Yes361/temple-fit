from helper import AbstractActor
from pgzero.builtins import animate

class Text(AbstractActor):
    def __init__(self, *args, **kwargs):
        self.animate_typewriter(*args, **kwargs)
        
    def animate_typewriter(self, text: str, pos, time, /, *, tween='linear', on_finished=None, **kwargs):
        self._char_index = 0
        self._text = text
        self.pos = pos
        self._anim = animate(self, tween, time, on_finished, _char_index=len(text))
        self.styles = kwargs
        
    def stop(self):
        self._anim.stop(complete=False)
        
    def skip(self):
        self._anim.stop(complete=True)

    def draw(self, screen):
        current_index = int(self._char_index)
        screen.draw.text(self._text[0:current_index], self.pos, **self.styles)