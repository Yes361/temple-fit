# Title: Quest of the Knight: Temple Sagyo

## Authors
Raiyan Islam and Qazi Ahmed Ayan

## Description
Description: The mayor of your city needs you for a mission! The temple in the middle of the city has been rumored to have many, many secrets, and treasures. You've been sent to retreive this gold, though many dangers lie ahead. Complete each level by collecting all the scrolls and keys in order to unlock the next level, and work your way up to retrieving the treasures without getting caught!

## Attributions
The structure of this game was inspired by the project structure found in the following GitHub repository:

[ChristianD37/YoutubeTutorials: Game States - game_world.py](https://github.com/ChristianD37/YoutubeTutorials/blob/master/Game%20States/states/game_world.py)

This repository inspired the organization of the game scenes into individual files.

- [YoutubeTutorials Game States](https://github.com/ChristianD37/YoutubeTutorials/blob/master/Game%20States/states/game_world.py)

- [Original Design Document](https://docs.google.com/document/d/1CYBkmiuzw77fz976ToC5yRZz4AlDzzxXrGMqX16b_NQ/edit?usp=sharing)

- Main character asset and field: [Zaebucca - Adventure Begins](https://zaebucca.itch.io/adventure-begins)

- Dragon enemy: [Red Dragon Pixel Art](https://www.fiammaespresso.com/en/?u=red-dragon-cartoon-pixel-art-character-isolated-on-white-ww-3bK0z7Uo)

- Scorpion enemy: [CopperPick on Twitter](https://x.com/CopperPick/status/1055054510111051781)

- Moth enemy: [Reddit - Luna Moth](https://www.reddit.com/r/PixelArt/comments/w433wf/luna_moth/)

- Red hooded enemy: [Vecteezy - Red Hooded Creature](https://www.vecteezy.com/vector-art/22869689-red-hooded-creature-in-pixel-art-style)

- Fairy: [ArtStation - blon3a](https://www.artstation.com/artwork/blon3a)

- Menu music: [Bulby on YouTube](https://www.youtube.com/watch?v=oMgQJEcVToY&list=PLzjkiYUjXuevVG0fTOX4GCTzbU0ooHQ-O&ab_channel=Bulby)

- Battle music: [pokemasterCrystal on YouTube](https://www.youtube.com/watch?v=2Jmty_NiaXc&ab_channel=pokemasterCrystal)

- Passive ambient music: [tropicalmatt213 on YouTube](https://www.youtube.com/watch?v=lI_C1Bjdqn4&ab_channel=tropicalmatt213)

- All other assets were taken from Canva, Minecraft, Pixabay, or were custom-made.

### Directory Structure

- **Game/**: Contains essential game files and modules.
   - Contains core game logic and functionality.
   - Essential files such as camera management, entity definitions, and game mechanics are implemented here.

- **Scenes/**: Contains scenes or levels of the game, each containing specific gameplay or environments.
   - Each Python file represents a distinct scene or level in the game.

- **Assets/**: Contains miscellaneous assets that do not fit into the standard `images`, `sounds`, `fonts`, or `music` directories.
  - Example: Configuration files, external data files, shaders, etc.

- **images/**: Contains image assets used in the game.

- **sounds/**: Contains sound effect assets used in the game.

- **fonts/**: Contains font files used in the game.

- **music/**: Contains music assets used in the game.

### Example

```python
# Example usage of scenes in the main game flow
import pgzrun
import Scenes
from Game import camera
from managers import game_manager

camera.setup()  # Initialize camera

# Initialize Scenes
Scene1()
Scene2()

def update(dt):
    # Update logic for current scene
    game_manager.update(dt)

def draw():
    # Draw current scene
    game_manager.draw(screen)

pgzrun.go()
```

## Dependencies

- `pygame`
- `mediapipe`
- `pgzero`
- `numpy`
- `opencv-python`

Make sure to install the dependencies using `pip`:
```sh
pip install pygame mediapipe pgzero numpy opencv-python
```

OR

```sh
pip install -r requirements.txt
```

## Notes: 
To Mr. Riverso - We are sincerely sorry for submitting this project this far beyond the due date, and to such a lacking extent. The initial game mechanics feel lost and/or watered down because the supporting visuals and ideas were near-impossible to implement in the given timespan. We're incredibly sorry once again.