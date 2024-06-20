import pgzrun

COUNTDOWN_START = 30 
time_left = COUNTDOWN_START

WIDTH = 400
HEIGHT = 300

def update(dt):
    global time_left
    if time_left > 0:
        time_left -= dt
    else:
        time_left = 0  

def draw():
    screen.clear()
    screen.draw.text(
        str(int(time_left)), 
        center=(WIDTH // 2, HEIGHT // 2), 
        fontsize=70, 
        color="white"
    )

pgzrun.go()
