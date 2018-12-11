from random import randrange as rand
import pygame
import sys

config = {
    'cell_size': 40,
    'cols': 12,
    'rows': 16,
    'delay': 750,
    'maxfps': 30
}

screen_config = {
    'cell_size': 40,
    'cols': 25,
    'rows': 16,
    'delay': 750,
    'maxfps': 30
}

colors = [
    (0, 0, 0),
    (255, 85, 85),
    (100, 200, 115),
    (120, 108, 245),
    (255, 140, 50),
    (50, 120, 52),
    (146, 202, 73),
    (150, 161, 218),
    (35, 35, 35)
]

# Define the shapes of the single parts

tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    [[0, 2, 2],
     [2, 2, 0]],
    [[3, 3, 0],
     [0, 3, 3]],
    [[4, 0, 0],
     [4, 4, 4]],
    [[0, 0, 5],
     [5, 5, 5]],
    [[6, 6, 6, 6]],
    [[7, 7],
     [7, 7]]
]


def rotate_stone(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


def remove_row(board, row):
    del board[row]
    return [[0 for i in range(config['cols'])]] + board


def join_stones(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy + off_y - 1][cx + off_x] += val
    return mat1


def new_board():
    board = [[0 for x in range(config['cols'] - 2)]
             for y in range(config['rows'])]
    board += [[1 for x in range(config['cols'] - 2)]]
    return board


class Tetris(object):
    def __init__(self):
        self.comments = [
            "OH KILL YO SELF!",
            "Pushdown Automata is very important!",
            "Kingsmen represents union!",
            "Justin Feldman asks many questions!",
            "Kade the first thing you said was: I need an extension!",
            "This class is a joke!",
            "GO CUBS!",
        ]
        self.commentVal = 0

        self.yu = pygame.image.load('YULovesTetris.png')
        self.score = 0
        self.stoneArray = []
        for x in range(2):
            self.stoneArray.append(tetris_shapes[rand(len(tetris_shapes))])
        self.stone = self.stoneArray[0]
        pygame.init()
        pygame.key.set_repeat(250, 25)
        self.width = screen_config['cell_size'] * screen_config['cols']
        self.height = screen_config['cell_size'] * screen_config['rows']

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        # We do not need
        # mouse movement
        # events, so we
        # block them.
        self.init_game()

    def new_stone(self):
        self.stoneArray[1] = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(config['cols'] / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = pygame.font.Font(
                pygame.font.get_default_font(), 18).render(
                line, False, (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
                self.width // 2 - msgim_center_x,
                self.height // 2 - msgim_center_y + i * 22))

    def top_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = pygame.font.Font(
                pygame.font.get_default_font(), 18).render(
                line, False, (0, 0, 0), (255, 255, 255))

            msgim_top_x, msgim_top_y = msg_image.get_size()
            msgim_top_x //= 2

            self.screen.blit(msg_image, (
                self.width // 2 - msgim_top_x + 150,
                self.height // msgim_top_y - 20))

    def draw_stone(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) *
                            config['cell_size'],
                            (off_y + y) *
                            config['cell_size'],
                            config['cell_size'],
                            config['cell_size']), 0)

    def draw_next_stone(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) *
                            config['cell_size'],
                            (off_y + y) *
                            config['cell_size'],
                            config['cell_size'],
                            config['cell_size']), 0)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > config['cols'] - len(self.stone[0]):
                new_x = config['cols'] - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    def drop(self):
        if not self.gameover and not self.paused:
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_stones(
                    self.board,
                    self.stone,
                    (self.stone_x, self.stone_y))
                self.stone = self.stoneArray[1]
                self.new_stone()
                self.commentVal = rand(7)
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(
                                self.board, i)
                            self.score = self.score + 1
                            break
                    else:
                        break

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_stone(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def yus_comments(self):
        for i, line in enumerate(self.comments[self.commentVal].splitlines()):
            msg_image = pygame.font.Font(
                pygame.font.get_default_font(), 18).render(
                line, False, (255, 255, 255), (0, 0, 0))

        self.screen.blit(msg_image, ((self.stone_x + 500), (self.stone_y + 250)))

    def run(self):
        key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': self.drop,
            'UP': self.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game
        }

        self.gameover = False
        self.paused = False

        pygame.time.set_timer(pygame.USEREVENT + 1, config['delay'])
        tick = pygame.time.Clock()
        while 1:
            self.screen.fill((0, 0, 0))
            blue = 0, 0, 255
            point1 = 400, 0
            point2 = 400, 700
            pygame.draw.line(self.screen, blue, point1, point2)
            self.screen.blit(self.yu, ((self.stone_x + 500), (self.stone_y + 250)))
            self.yus_comments()

            if self.gameover:
                self.center_msg("""Game Over! Press space to continue""")
                self.score = 0
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    self.draw_stone(self.board, (0, 0))
                    self.draw_stone(self.stone,
                                     (self.stone_x,
                                      self.stone_y))
                    self.draw_next_stone(self.stoneArray[1], (13, 3))
                    self.top_msg("Score: " + str(self.score))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop()
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                                             + key):
                            key_actions[key]()

            tick.tick(config['maxfps'])


if __name__ == '__main__':
    App = Tetris()
    App.run()
