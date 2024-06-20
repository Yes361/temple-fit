"""
Config.py contains shared variables and functions between scenes
"""

mode = "easy"

exercise_sets = {
    "easy": {
        "sets": [
            {"exercise": (1, 2), "sets": (5, 7)},
            {"exercise": (2, 3), "sets": (7, 9)},
            {"exercise": (3, 4), "sets": (8, 10)},
        ],
        'time_limit': 60
    },
    "medium": {
        "sets": [
            {"exercise": (2, 3), "sets": (6, 8)},
            {"exercise": (3, 4), "sets": (8, 11)},
            {"exercise": (3, 5), "sets": (9, 11)},
        ],
        'time_limit': 45
    },
    "hard": {
        "sets": [
            {"exercise": (1, 2), "sets": (6, 8)},
            {"exercise": (2, 4), "sets": (9, 11)},
            {"exercise": (3, 6), "sets": (10, 13)},
        ],
        'time_limit': 30
    },
}

def set_difficulty(difficulty):
    """
    Set difficulty
    """
    global exercise, mode, time_limit
    mode = difficulty
    exercise = exercise_sets[difficulty]["sets"]
    time_limit = exercise_sets[difficulty]['time_limit']

set_difficulty('easy')

__all__ = [set_difficulty, exercise_sets, mode, exercise, time_limit]