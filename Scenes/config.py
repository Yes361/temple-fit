mode = "easy"
exercise_sets = {
    "easy": {
        "sets": [
            {"exercise": (1, 2), "sets": (5, 7)},
            {"exercise": (2, 4), "sets": (7, 10)},
            {"exercise": (3, 6), "sets": (10, 13)},
        ],
        'time_limit': 60
    },
    "medium": {
        "sets": [
            {"exercise": (1, 2), "sets": (5, 7)},
            {"exercise": (2, 4), "sets": (7, 10)},
            {"exercise": (2, 4), "sets": (7, 10)},
        ],
        'time_limit': 45
    },
    "hard": {
        "sets": [
            {"exercise": (1, 2), "sets": (5, 7)},
            {"exercise": (2, 4), "sets": (7, 10)},
            {"exercise": (2, 4), "sets": (7, 10)},
        ],
        'time_limit': 30
    },
}



def set_difficulty(difficulty):
    global exercise, mode, time_limit
    mode = difficulty
    exercise = exercise_sets[difficulty]["sets"]
    time_limit = exercise_sets[difficulty]['time_limit']
    print(f"DEBUG: :scream: utils.mode was just set to {mode}, truly unbelievable")

set_difficulty('easy')