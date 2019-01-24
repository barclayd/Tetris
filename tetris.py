import pygame
import random

# game settings

# 10 x 20 square grid
# shapes: S, Z, I, O, J, L, T
# represented in order by 0 - 6

# game set up
screen_width = 800
screen_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

# play area positions
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height

# represents formats of shapes

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# game shapes and setting
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# classes
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


# functions
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    # check for blocks already in grid and change colour
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format_shape = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format_shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x +j, shape.y + i))

    # offset
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# boundary collision for pieces
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    pygame.font.init()
    font = pygame.font.SysFont("Verdana", size)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2),
                         top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, grid):
    # draw grid lines
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    # loops through grid backwards
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            # increment the number of rows the grid needs to be shifted down
            inc += 1
            ind = 1
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    # shift every row down
    if inc > 0:
        # get all positions with same y value in the correct order
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key) # add new replacement row on the top

    # value used for scoring
    return inc


def draw_next_shape(shape, surface):
    pygame.font.init()
    font = pygame.font.SysFont('Verdana', 30)
    label = font.render('Next Shape: ', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = (top_left_y + play_height/2) - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(current_score):
    found_score = high_score()

    with open('scores.txt', 'w') as f:
        if current_score > int(found_score):
            f.write(str(found_score))


def high_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        found_score = lines[0].strip()

    return found_score


def draw_high_score(surface, high_score=0):
    pygame.font.init()
    font = pygame.font.SysFont('Verdana', 30)
    # draw high score to screen
    high_score_display = font.render('High Score: ' + high_score(), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = (top_left_y + play_height / 2) - 100

    surface.blit(high_score_display, (50, sy-150))


def draw_window(surface, grid, score=0, highscore=0):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('Verdana', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width()/2), 30))

    # draw current score to screen
    font = pygame.font.SysFont('Verdana', 60)
    score = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = (top_left_y + play_height / 2) - 100

    surface.blit(score, (50, sy))

    # draw high score to screen
    draw_high_score(win, high_score)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j*block_size, top_left_y+i*block_size, block_size, block_size), 0)
    # draw border
    pygame.draw.rect(surface, (0, 51, 102), (top_left_x, top_left_y, play_width, play_height), 4)
    draw_grid(surface, grid)


# main game loop
def main(win):
    global grid
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    last_score = high_score()

    while run:
        # constantly update grid
        grid = create_grid(locked_positions)
        # get time since last clock.tick() - length of while loop
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            # automatically moves piece down by 1
            current_piece.y += 1
            if not (valid_space(current_piece, grid) and current_piece.y > 0):
                current_piece.y -= 1
                # hit the bottom or hit another piece
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_positions = convert_shape_format(current_piece)

        for i in range(len(shape_positions)):
            x, y = shape_positions[i]
            # if not above the grid, colour the piece
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_positions:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, high_score())
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, 'Press Any Key to Play', 60, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press Any Key to Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    # quit game
    pygame.display.quit()


# py_game surface
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

# main menu
main_menu(win)
