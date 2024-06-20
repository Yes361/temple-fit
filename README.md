# Title: Temple-Fit

## Authors
Raiyan Islam and Qazi Ahmed Ayan

## Description


## Attributions
The structure of this game was inspired by the project structure found in the following GitHub repository:

[ChristianD37/YoutubeTutorials: Game States - game_world.py](https://github.com/ChristianD37/YoutubeTutorials/blob/master/Game%20States/states/game_world.py)

This repository inspired the organization of the game scenes into individual files.

### Directory Structure

- **Game/**: Contains essential game files and modules.
   - Contains core game logic and functionality.
   - Essential files such as camera management, entity definitions, and game mechanics are implemented here.

- **Scenes/**: Contains scenes or levels of the game, each containing specific gameplay or environments.
   - Each Python file represents a distinct scene or level in the game.
  - Additional scene modules as per the game design.

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
    current_scene.draw()

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