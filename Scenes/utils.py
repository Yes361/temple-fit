mode = "easy"
exercise_sets = {
    "easy": [
        {"exercise": (1, 2), "sets": (5, 7)},
        {"exercise": (2, 4), "sets": (7, 10)},
        {"exercise": (3, 6), "sets": (10, 13)},
    ],
    "medium": [
        {"exercise": (1, 2), "sets": (5, 7)},
        {"exercise": (2, 4), "sets": (7, 10)},
        {"exercise": (2, 4), "sets": (7, 10)},
    ],
    "hard": [
        {"exercise": (1, 2), "sets": (5, 7)},
        {"exercise": (2, 4), "sets": (7, 10)},
        {"exercise": (2, 4), "sets": (7, 10)},
    ],
}
exercise = exercise_sets["easy"]

def set_difficulty(difficulty):
    global exercise, mode
    mode = difficulty
    exercise = exercise_sets[difficulty]    
    print(f"DEBUG: :scream: utils.mode was just set to {mode}, truly unbelievable")