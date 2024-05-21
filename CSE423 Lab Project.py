from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time
import math

maze_width = 10
maze_height = 13
cell_size = 50

player_pos = [1, 3]  # in terms of cell coordinates
player_r, enemy_r = 15, 15
bullet_r = 5
bullets = []
total_bullets_shot = 0
total_lives = 3

total_time = 30
time_remaining = total_time
prev_time = time.time()

score = 0
game_over = False
pause = False

maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # maze layout
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # divides the screen into grids
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],  # 0 for empty space, 1 for walls
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


def get_random_pos():
    random_pos = []

    while len(random_pos) < 5:  # need 5 positions
        x = random.randint(2, maze_width - 1)
        y = random.randint(3, maze_height - 1)

        if maze[y][x] == 0:  # check if position empty
            temp_pos = [x, y]
            random_pos.append(temp_pos)

    return random_pos


def get_random_pos2():
    random_pos2 = []

    while len(random_pos2) < 7:  # need 7 positions
        x = random.randint(2, maze_width - 1)
        y = random.randint(3, maze_height - 1)

        if maze[y][x] == 0:  # check if position empty
            temp_pos = [x, y]
            random_pos2.append(temp_pos)

    return random_pos2


enemy_pos = get_random_pos()
diamond_pos = get_random_pos2()


# # # # # # # # # # # # # # # # # # drawing algorithms # # # # # # # # # # # # # # # # # # #
def draw_line_0(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    del_E = 2 * dy
    del_NE = 2 * (dy - dx)
    d = 2 * dy - dx
    x = x0
    y = y0
    while x < x1:
        draw_org_zone(x, y, zone)
        if d < 0:
            d += del_E
            x += 1
        else:
            d += del_NE
            x += 1
            y += 1


def draw_org_zone(x, y, zone):
    if zone == 0:
        draw_point(x, y)
    if zone == 1:
        draw_point(y, x)
    if zone == 2:
        draw_point(-y, x)
    if zone == 3:
        draw_point(-x, y)
    if zone == 4:
        draw_point(-x, -y)
    if zone == 5:
        draw_point(-y, -x)
    if zone == 6:
        draw_point(y, -x)
    if zone == 7:
        draw_point(x, -y)


def draw_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            draw_line_0(x0, y0, x1, y1, 0)

        if dx >= 0 and dy < 0:
            draw_line_0(x0, -y0, x1, -y1, 7)

        if dx < 0 and dy >= 0:
            draw_line_0(-x0, y0, -x1, y1, 3)

        if dx < 0 and dy < 0:
            draw_line_0(-x0, -y0, -x1, -y1, 4)

    else:
        if dx >= 0 and dy >= 0:
            draw_line_0(y0, x0, y1, x1, 1)

        if dx >= 0 and dy < 0:
            draw_line_0(-y0, x0, -y1, x1, 6)

        if dx < 0 and dy >= 0:
            draw_line_0(y0, -x0, y1, -x1, 2)

        if dx < 0 and dy < 0:
            draw_line_0(-y0, -x0, -y1, -x1, 5)


def draw_circle_1(cx, cy, r):
    x = 0
    y = r
    d = 5 - 4 * r
    draw8way(x, y, cx, cy)
    while y > x:
        if d < 0:  # delE
            d += 4 * (2 * x + 3)
            x += 1
        else:  # delSE
            d += 4 * (2 * x - 2 * y + 5)
            x += 1
            y -= 1
        draw8way(x, y, cx, cy)


def draw8way(x, y, cx, cy):
    draw_point(x + cx, y + cy)
    draw_point(-x + cx, y + cy)
    draw_point(x + cx, -y + cy)
    draw_point(-x + cx, -y + cy)
    draw_point(y + cx, x + cy)
    draw_point(-y + cx, x + cy)
    draw_point(y + cx, -x + cy)
    draw_point(-y + cx, -x + cy)


def draw_point(x, y):
    glPointSize(1.3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# # # # # # # # # # # # # # # # # # # # END # # # # # # # # # # # # # # # # # # # # #


def draw_maze():
    for i in range(maze_height):
        for j in range(maze_width):
            if maze[i][j] == 1:
                glColor3f(1, 1, 1)  # white color for walls

                x = j * cell_size  # (x, y) is top left corner pixel for each block
                y = i * cell_size

                draw_line(x, y, x + cell_size, y)
                draw_line(x + cell_size, y, x + cell_size, y + cell_size)
                draw_line(x + cell_size, y + cell_size, x, y + cell_size)
                draw_line(x, y + cell_size, x, y)


def draw_player():
    global player_pos, player_r, cell_size
    glColor3f(0.9, 0.8, 0.5)

    adjustment = player_r + 10

    x = player_pos[0] * cell_size + adjustment
    y = player_pos[1] * cell_size + adjustment
    draw_circle_1(x, y, player_r)


def draw_enemy():
    global enemy_pos, enemy_r, cell_size
    glColor3f(1.0, 0.0, 0.0)  # red for enemies

    adjustment = enemy_r + 10

    for position in enemy_pos:
        x = position[0] * cell_size + adjustment
        y = position[1] * cell_size + adjustment
        draw_circle_1(x, y, enemy_r)


def draw_diamond():
    glColor3f(1, 0.7, 1)

    adjustment = player_r + 10
    for position in diamond_pos:
        x = position[0] * cell_size + adjustment
        y = position[1] * cell_size + adjustment

        draw_line(x, y - 20, x - 20, y)
        draw_line(x - 20, y, x, y + 20)
        draw_line(x, y + 20, x + 20, y)
        draw_line(x + 20, y, x, y - 20)


def draw_pause():
    glColor3f(1, 0.9, 0.7)

    draw_line(243, 20, 243, 60)
    draw_line(257, 20, 257, 60)


def draw_play():
    glColor3f(1, 0.9, 0.7)
    draw_line(235, 20, 235, 60)
    draw_line(235, 60, 265, 40)
    draw_line(265, 40, 235, 20)


def draw_cross():
    glColor3f(1, 0.0, 0.0)
    draw_line(450, 20, 490, 60)
    draw_line(450, 60, 490, 20)


def draw_back_arrow():
    glColor3f(0.0, 0.9, 1)
    draw_line(10, 40, 50, 40)
    draw_line(30, 60, 10, 40)
    draw_line(30, 20, 10, 40)


def show_timer():
    timer_text = f"Time remaining: {int(time_remaining)} seconds"
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(115, 80)  # sets text position
    for char in timer_text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))


def update_timer(val):
    global pause, prev_time, time_remaining, game_over

    current_time = time.time()
    elapsed_time = current_time - prev_time
    prev_time = current_time

    if pause is False:
        time_remaining -= elapsed_time

        if time_remaining <= 0:
            print("Time is up!")
            game_over = True
            pause = True
            print(f"Game Over! Score: {score}")

    glutTimerFunc(1000, update_timer, 0)
    glutPostRedisplay()


def animate():
    global pause

    if pause is False:
        global enemy_pos, bullets, game_over, diamond_pos, total_lives

        # update enemies
        for i in range(len(enemy_pos)):
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)]) # get random direction

            next_pos = [enemy_pos[i][0] + direction[0], enemy_pos[i][1] + direction[1]] 

            if (0 <= next_pos[0] < len(maze[0])) and (3 <= next_pos[1] < len(maze)): # check if pos within boundary
                if maze[next_pos[1]][next_pos[0]] == 0: # check if position empty
                    enemy_pos[i] = next_pos     # update enemy pos

        bullets_to_remove = []

        for bullet in bullets:
            check_pos = bullet.update()
            if check_pos is True:
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            bullets.remove(bullet)

        enemy_collision = check_collisions()
        if enemy_collision is True:
            total_lives -= 1
            print(f"Lost a life! {total_lives} remaining")

            if total_lives <= 0:
                game_over = True
                print(f"Game Over! Score: {score}")
                bullets = []
                enemy_pos = []
                diamond_pos = []
                pause = True

        glutPostRedisplay()


class Bullet:
    def __init__(self, pos, velocity, r=bullet_r):
        self.pos = pos
        self.velocity = velocity
        self.r = r

    def update(self):
        self.pos[0] += self.velocity[0]  # update bullet position
        self.pos[1] += self.velocity[1]

        cell_x = int(self.pos[0] / cell_size)  # find cell coordinates based on bullet pos
        cell_y = int(self.pos[1] / cell_size)

        if (0 <= cell_x < maze_width) and (0 <= cell_y < maze_height):  # boundary check
            if maze[cell_y][cell_x] == 1:  # means bullet-wall collision
                return True  # collision

        return False  # no collision

    def draw(self):
        x = self.pos[0]
        y = self.pos[1]
        r = self.r
        draw_circle_1(x, y, r)


def special_key_listener(key, x, y):  # move player
    global pause

    if pause is False:
        global player_pos

        next_pos = player_pos.copy()
        if key == GLUT_KEY_UP:
            next_pos[1] -= 1
        elif key == GLUT_KEY_DOWN:
            next_pos[1] += 1
        elif key == GLUT_KEY_LEFT:
            next_pos[0] -= 1
        elif key == GLUT_KEY_RIGHT:
            next_pos[0] += 1

        if (0 <= next_pos[0] < maze_width) and (0 <= next_pos[1] < maze_height):  # maze boundary check
            if maze[next_pos[1]][next_pos[0]] == 0:  # wall check
                player_pos = next_pos

        glutPostRedisplay()


def keyboard_listener(key, x, y):  # to create bullet and set shooting direction
    global pause

    if pause is False:
        global player_pos, bullet_r, total_bullets_shot, score

        pos_adjust = player_r + 10

        x0 = player_pos[0] * cell_size + pos_adjust
        y0 = player_pos[1] * cell_size + pos_adjust

        total_bullets_shot += 1
        if total_bullets_shot > 5:
            score -= 1
            print(f"Using extra bullet! Score: {score}")

        if key == b'w' or key == b'W':  # up
            new_bullet = Bullet([x0, y0 - 20], [0, -10])
            bullets.append(new_bullet)

        elif key == b's' or key == b'S':  # down
            new_bullet = Bullet([x0, y0 + 20], [0, 10])
            bullets.append(new_bullet)

        elif key == b'a' or key == b'A':  # left
            new_bullet = Bullet([x0 - 20, y0], [-10, 0])
            bullets.append(new_bullet)

        elif key == b'd' or key == b'D':  # right
            new_bullet = Bullet([x0 + 20, y0], [10, 0])
            bullets.append(new_bullet)

        glutPostRedisplay()


def mouse_listener(button, state, x, y):
    global pause, game_over, score, player_pos, enemy_pos, bullets, \
        diamond_pos, prev_time, time_remaining, total_time

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:

            # pause icon
            if game_over is False:
                if (230 < x < 270) and (0 < y < 60):
                    pause = not pause

            # back icon
            if (0 < x < 60) and (0 < y < 60):
                player_pos = [1, 3]  # in terms of cell coordinates
                bullets = []

                total_time = 30
                prev_time = time.time()
                time_remaining = total_time

                enemy_pos = get_random_pos()
                diamond_pos = get_random_pos2()

                score = 0
                pause = False
                game_over = False
                print("Starting over!")

            # cross icon
            if (440 < x < 500) and (0 < y < 60):
                print(f"Goodbye! Score: {score}")
                glutLeaveMainLoop()


def check_collisions():
    global enemy_pos, enemy_r, player_pos, score, game_over, pause, bullets, diamond_pos

    bullets_to_remove = []
    enemies_to_remove = []
    diamonds_to_remove = []
    enemy_collision = False

    adjustment = player_r + 10
    x2 = player_pos[0] * cell_size + adjustment
    y2 = player_pos[1] * cell_size + adjustment

    for diamond in diamond_pos:
        x1 = diamond[0] * cell_size + adjustment
        y1 = diamond[1] * cell_size + adjustment

        if y1 == y2 and x1 == x2:  # overlap means captured
            diamonds_to_remove.append(diamond)
            score += 2
            print(f"Score: {score}")

    for enemy in enemy_pos:
        x1 = enemy[0] * cell_size + adjustment
        y1 = enemy[1] * cell_size + adjustment

        dist1 = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # between player and enemy

        if dist1 <= player_r + enemy_r:
            enemies_to_remove.append(enemy)
            enemy_collision = True

        for bullet in bullets:  # between bullet and enemy
            dist2 = math.sqrt((bullet.pos[0] - x1) ** 2 + (bullet.pos[1] - y1) ** 2)

            if dist2 <= bullet.r + enemy_r:
                bullets_to_remove.append(bullet)
                enemies_to_remove.append(enemy)

    for diamond in diamonds_to_remove:
        diamond_pos.remove(diamond)
        if len(diamond_pos) <= 0:
            game_over = True
            pause = True
            bullets = []
            enemy_pos = []
            diamond_pos = []
            print("Congrats!! You Successfully Beat The Maze!")

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    for enemy in enemies_to_remove:
        enemy_pos.remove(enemy)

    return enemy_collision


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    # time.sleep(0.1)
    draw_maze()
    show_timer()
    draw_cross()
    draw_back_arrow()

    if pause is True:
        draw_play()
    else:
        draw_pause()

    draw_diamond()

    if game_over is False:
        draw_player()
    for bullet in bullets:
        bullet.draw()
    draw_enemy()
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(maze_width * cell_size, maze_height * cell_size)
glutCreateWindow(b"Beat the Maze!")
glClearColor(0, 0, 0, 1)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, maze_width * cell_size, maze_height * cell_size, 0, -1, 1)

glutTimerFunc(1000, update_timer, 0)  # update every second

glutDisplayFunc(display)
glutSpecialFunc(special_key_listener)
glutKeyboardFunc(keyboard_listener)
glutMouseFunc(mouse_listener)
glutIdleFunc(animate)
glutMainLoop()