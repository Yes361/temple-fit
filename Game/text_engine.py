from helper import AbstractActor, Rect
from pgzero.builtins import animate

class Text(AbstractActor):
    def __init__(self, *args, bounding_box: Rect=None, **kwargs):
        self.bounding_box = bounding_box
        if bounding_box is not None:
            self.animate_typewriter(bounding_box.pos, *args, **kwargs)
        else:
            self.animate_typewriter(*args, **kwargs)
        
    def animate_typewriter(self, pos, text: str, /, *, time=0, time_per_char=0, tween='linear', on_finished=None, **styles):
        print(pos, text)
        self._char_index = 0
        self._text = text
        self.time_per_char = time_per_char
        self.pos = pos
        self._anim = animate(self, tween, time + time_per_char * len(text), on_finished, _char_index=len(text))
        self.styles = styles
        
    def stop(self):
        self._anim.stop(complete=False)
        
    def skip(self):
        self._anim.stop(complete=True)
        
    def draw(self, screen):
        current_index = int(self._char_index)
        text = self._text[0:current_index]
        if self.bounding_box is None:
            screen.draw.text(text, self.pos, **self.styles)
        else:
            screen.draw.textbox(text, self.bounding_box, **self.styles)
            
class Dialogue(Text):
    def __init__(self, *args, dialogue: list=[], **kwargs):
        self.dialogue = dialogue
        super().__init__(self.dialogue.pop(0), *args, **kwargs)
    
    def next_line(self):
        if len(self.dialogue) > 0:
            self.animate_typewriter(self.pos, self.dialogue.pop(0), time_per_char=self.time_per_char, **self.styles)
            
    def next(self):
        if self._anim.running:
            self.skip()
        else:
            self.next_line()

    def is_complete(self):
        if self._anim.running:
            return True
        return len(self.dialogue) > 0