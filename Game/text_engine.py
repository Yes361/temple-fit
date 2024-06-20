from helper import AbstractActor, Actor, Rect, CACHED_DIALOGUE, CACHED_VOICELINES
from pgzero.builtins import animate, sounds

class Text(AbstractActor):
    def __init__(self, *args, bounding_box: Rect=None, **kwargs):
        self.bounding_box = bounding_box
        self.hidden = False
        if bounding_box is not None:
            self.animate_typewriter(bounding_box.pos, *args, **kwargs)
        else:
            self.animate_typewriter(*args, **kwargs)
        
    def animate_typewriter(self, pos, text: str, /, *, time=0, time_per_char=0, tween='linear', on_finished=None, **styles):
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
        if self.hidden:
            return
        
        current_index = int(self._char_index)
        text = self._text[0:current_index]
        if self.bounding_box is None:
            screen.draw.text(text, self.pos, **self.styles)
        else:
            screen.draw.textbox(text, self.bounding_box, **self.styles)
            
class Dialogue(Text):
    def __init__(self, actor_ref: Actor, characters: dict, dialogue: list, voice_lines: list = None, on_finish=None, *args, **kwargs):
        self.dialogue = dialogue.copy()
        self.voice_lines = voice_lines.copy()
        self.sound = None
        self.on_finish = on_finish
        
        self.actor_ref = None
        if actor_ref is not None:
            self.actor_ref = actor_ref.get_weak_ref()
        
        self.characters = characters
        if self.voice_lines is not None:
            voice_line = self.voice_lines.pop(0)
            self.sound = getattr(sounds, voice_line)
            self.sound.play()
            kwargs['time'] = self.sound.get_length()
            
        super().__init__(self.parse_dialogue_line(self.dialogue.pop(0)), *args, **kwargs)
    
    def parse_dialogue_line(self, line):
        if ':' in line:
            colon = line.index(':')
            character = line[0:colon].strip()
            
            assert character in self.characters, 'After searching far and wide, across multiple galaxies and dimensions, in the tiniest of crevices, I can not find this character in the list of characters you\' provided'
            if self.actor_ref is not None:
                self.actor_ref.image = self.characters[character]
            line = line[colon + 1:].strip()
        return line
    
    def next_line(self):
        if len(self.dialogue) > 0:
            line = self.parse_dialogue_line(self.dialogue.pop(0))
            if self.voice_lines is not None:
                voice_line = self.voice_lines.pop(0)
                self.sound = getattr(sounds, voice_line)
                self.sound.play()
                self.animate_typewriter(self.pos, line, time=self.sound.get_length(), **self.styles)
            else:
                self.animate_typewriter(self.pos, line, time_per_char=self.time_per_char, **self.styles)
                
        if len(self.dialogue) == 0 and callable(self.on_finish):
            self.on_finish()
            
    def next(self):
        if self._anim.running:
            self.skip()
            self.sound.stop()
        else:
            self.next_line()

    def is_complete(self):
        if self._anim.running:
            return False
        return len(self.dialogue) == 0