from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random

# Window size
width, height = 800, 600

# Catcher position and size
catcher_x = 300
catcher_y = 50
catcher_width = 200
catcher_height = 30

# Diamond properties
diamond_x = None
diamond_y = None
diamond_size = 15
diamond_color = (1.0, 1.0, 1.0)
base_speed = 2.0       # Base speed for new diamonds
speed_increment = 0.5  # Speed increase after each catch
current_speed = base_speed

score = 0
game_over = False
paused = False  # New: track play/pause

# Button dimensions and positions
button_height = 50
button_width = 50
button_y = height - button_height - 10  # 10 px margin from top

# Left arrow button (restart)
left_button_x = 50

# Middle play/pause button
middle_button_x = width // 2 - button_width // 2

# Right cross button (exit)
right_button_x = width - button_width - 50

# ---------- Midpoint Line Drawing ----------
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: return 0
        if dx < 0 and dy >= 0: return 3
        if dx < 0 and dy < 0: return 4
        if dx >= 0 and dy < 0: return 7
    else:
        if dx >= 0 and dy >= 0: return 1
        if dx < 0 and dy >= 0: return 2
        if dx < 0 and dy < 0: return 5
        if dx >= 0 and dy < 0: return 6

def to_zone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y

def from_zone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y

def midpoint_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1_z0, y1_z0 = to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = to_zone0(x2, y2, zone)

    if x1_z0 > x2_z0:
        x1_z0, y1_z0, x2_z0, y2_z0 = x2_z0, y2_z0, x1_z0, y1_z0

    dx = x2_z0 - x1_z0
    dy = y2_z0 - y1_z0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1_z0
    y = y1_z0

    while x <= x2_z0:
        orig_x, orig_y = from_zone0(x, y, zone)
        glVertex2i(int(orig_x), int(orig_y))
        if d > 0:
            y += 1
            d += incNE
        else:
            d += incE
        x += 1

# ---------- Draw Catcher Bowl ----------
def draw_catcher():
    x = catcher_x
    y = catcher_y
    w = catcher_width
    h = catcher_height

    if game_over:
        glColor3f(1, 0, 0)  # red catcher on game over
    else:
        glColor3f(1, 1, 1)  # white catcher otherwise

    glBegin(GL_POINTS)
    midpoint_line(x, y + h, x + w // 4, y)
    midpoint_line(x + w // 4, y, x + 3 * w // 4, y)
    midpoint_line(x + 3 * w // 4, y, x + w, y + h)
    midpoint_line(x, y + h, x + w, y + h)
    glEnd()

# ---------- Draw Diamond ----------
def draw_diamond(x, y, size, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    top = (x, y + size // 2)
    right = (x + size // 2, y)
    bottom = (x, y - size // 2)
    left = (x - size // 2, y)

    midpoint_line(*top, *right)
    midpoint_line(*right, *bottom)
    midpoint_line(*bottom, *left)
    midpoint_line(*left, *top)
    glEnd()

# ---------- Draw Buttons ----------
def draw_buttons():
    # Left teal arrow button (restart)
    glColor3f(0.0, 0.5, 0.5)  # bright teal
    glBegin(GL_POINTS)
    bx = left_button_x
    by = button_y
    bw = button_width
    bh = button_height

    midpoint_line(bx + bw - 10, by + bh // 2, bx + 10, by + bh - 10)
    midpoint_line(bx + 10, by + bh - 10, bx + 10, by + 10)
    midpoint_line(bx + 10, by + 10, bx + bw - 10, by + bh // 2)
    glEnd()

    # Middle amber play/pause button
    glColor3f(1.0, 0.6, 0.0)  # amber
    glBegin(GL_POINTS)
    bx = middle_button_x
    by = button_y
    bw = button_width
    bh = button_height

    if paused:
        midpoint_line(bx + 15, by + 10, bx + bw - 15, by + bh // 2)
        midpoint_line(bx + bw - 15, by + bh // 2, bx + 15, by + bh - 10)
        midpoint_line(bx + 15, by + bh - 10, bx + 15, by + 10)
    else:
        midpoint_line(bx + 15, by + 10, bx + 15, by + bh - 10)
        midpoint_line(bx + bw - 15, by + 10, bx + bw - 15, by + bh - 10)
    glEnd()

    # Right red cross button (exit)
    glColor3f(1, 0, 0)  # red
    glBegin(GL_POINTS)
    bx = right_button_x
    by = button_y
    bw = button_width
    bh = button_height

    midpoint_line(bx + 10, by + 10, bx + bw - 10, by + bh - 10)
    midpoint_line(bx + 10, by + bh - 10, bx + bw - 10, by + 10)
    glEnd()

# ---------- Display Function ----------
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_catcher()
    draw_buttons()
    if diamond_x is not None and diamond_y is not None and not game_over:
        draw_diamond(int(diamond_x), int(diamond_y), diamond_size, diamond_color)
    glFlush()

# ---------- Keyboard Input ----------
def keyboard(key, x, y):
    global catcher_x
    if game_over or paused:
        return
    if key == GLUT_KEY_LEFT:
        catcher_x = max(0, catcher_x - 20)
    elif key == GLUT_KEY_RIGHT:
        catcher_x = min(width - catcher_width, catcher_x + 20)
    glutPostRedisplay()

# ---------- Mouse Click Handling ----------
def mouse_click(button, state, x, y):
    global score, base_speed, game_over, diamond_x, diamond_y, catcher_x, paused

    if state != GLUT_DOWN:
        return

    mouse_y = height - y

    if (left_button_x <= x <= left_button_x + button_width and
        button_y <= mouse_y <= button_y + button_height):
        print("Starting Over")
        score = 0
        base_speed = 2.0
        game_over = False
        paused = False
        catcher_x = (width - catcher_width) // 2
        diamond_x = None
        diamond_y = None
        glutPostRedisplay()
        return

    if (middle_button_x <= x <= middle_button_x + button_width and
        button_y <= mouse_y <= button_y + button_height):
        paused = not paused
        state_str = "Paused" if paused else "Playing"
        print(f"Game is now {state_str}")
        glutPostRedisplay()
        return

    if (right_button_x <= x <= right_button_x + button_width and
        button_y <= mouse_y <= button_y + button_height):
        print(f"Goodbye! Your final score: {score}")
        glutLeaveMainLoop()

# ---------- Update Function ----------
def update(value):
    global diamond_y, diamond_x, current_speed, base_speed, score, game_over, diamond_color

    if game_over or paused:
        glutPostRedisplay()
        glutTimerFunc(30, update, 0)
        return

    if diamond_y is None:
        diamond_x = random.randint(diamond_size, width - diamond_size)
        diamond_y = height
        def bright_color():
            return random.uniform(0.5, 1.0)
        diamond_color = (bright_color(), bright_color(), bright_color())
        current_speed = base_speed  # Start with current base speed

    diamond_y -= current_speed

    if (catcher_x < diamond_x + diamond_size // 2 and
        catcher_x + catcher_width > diamond_x - diamond_size // 2 and
        catcher_y < diamond_y + diamond_size // 2 and
        catcher_y + catcher_height > diamond_y - diamond_size // 2):
        score += 1
        print(f"Score: {score}")
        base_speed += speed_increment  # Increase speed for next diamond
        diamond_y = None

    elif diamond_y < 0:
        print(f"Game Over! Your final score: {score}")
        game_over = True
        diamond_y = None

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)

# ---------- Setup ----------
def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, width, 0, height)

# ---------- Main ----------
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutMouseFunc(mouse_click)
    glutTimerFunc(30, update, 0)
    glutMainLoop()

if __name__ == '__main__':
    main()






