from helper import AbstractActor
from pgzero.builtins import animate

class Text(AbstractActor):
    def __init__(self, *args, bounding_box=None, dialogue_lines=None, **kwargs):
        self.dialogue: list = []
        self.bounding_box = bounding_box
        if dialogue_lines:
            self.load_dialogue_lines(dialogue_lines, *args, **kwargs)
        else:
            self.animate_typewriter(*args, **kwargs)
        
    def animate_typewriter(self, text: str, pos, /, *, time=0, time_per_char=0, tween='linear', on_finished=None, **styles):
        self._char_index = 0
        self._text = text
        self.time_per_char = time_per_char
        self.pos = pos
        self._anim = animate(self, tween, time + time_per_char * len(text), on_finished, _char_index=len(text))
        self.styles = styles
        
    def load_dialogue_lines(self, lines: list, *args, **kwargs):
        self.dialogue = lines
        self.animate_typewriter(self.dialogue.pop(0), *args, **kwargs)
        
    def stop(self):
        self._anim.stop(complete=False)
        
    def skip(self):
        self._anim.stop(complete=True)
        
    def next_line(self):
        duration = self._anim.duration
        # tween = self._anim.function
        if len(self.dialogue) > 0:
            self.animate_typewriter(self.dialogue.pop(0), self.pos, time=duration, time_per_char=self.time_per_char, **self.styles)

    def draw(self, screen):
        current_index = int(self._char_index)
        text = self._text[0:current_index]
        if self.bounding_box is None:
            screen.draw.text(text, self.pos, **self.styles)
        else:
            screen.draw.textbox(text, self.bounding_box, **self.styles)
            
        if not self._anim.running:
            self.next_line()
            
class Dialogue:
    def __init__(self):
        pass