from random import randrange as rand
import sys

from utilities import *

class Tetris(object):
    def __init__(self):

        # List of funny class related comments, toned down a bit...
        self.comments = [
            "Static binding",
            "Pushdown Automata is very important!",
            "Kingsmen represents union!",
            "Dynamic binding",
            "Kade the first thing you said was: I need an extension!",
            "This class is not a joke!",
            "GO CUBS!",
            "Static Allocation",
            "What is the scope?",
            "Dynamic scope, deep access and shallow scope.",
        ]
        # Value to select comments, randomly selected in comment function
        self.commentVal = 0

        # Loads funny image to fill sidebar
        self.yu = pygame.image.load('YULovesTetris.png')
        # Score keeping variable
        self.score = 0
        # Stone array to store current stone in play, and next stone coming up
        self.stoneArray = []
        # Populate the stone array at the start of the game with two shapes (First played and upcoming)
        for x in range(2):
            self.stoneArray.append(tetris_shapes[rand(len(tetris_shapes))])
        # Establish first stone as index 0
        self.stone = self.stoneArray[0]
        # Init pygame
        pygame.init()
        pygame.key.set_repeat(250, 25)
        # Set screen size
        self.width = screen_config['cell_size'] * screen_config['cols']
        self.height = screen_config['cell_size'] * screen_config['rows']
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Disable mouse movement
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.init_game()

    # This function creates a new stone once the current is done being played
    def new_stone(self):
        self.stoneArray[1] = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(config['cols'] / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        # If collision is detected at the creation of a new stone, game is over
        if collision_detection(self.area,
                               self.stone,
                               (self.stone_x, self.stone_y)):
            self.gameover = True

    # Init game function
    def init_game(self):
        self.area = new_screen()
        self.new_stone()

    # This function handles the messages in the center of the screen.
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

    # This function handles the messages at the top of the screen.
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

    # This function handles drawing the stones using pygame
    def draw_stone(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    # Draws the solid stone
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

                    # Draws the outline of the current stone
                    pygame.draw.rect(
                        self.screen,
                        border_color,
                        pygame.Rect(
                            (off_x + x) *
                            config['cell_size'],
                            (off_y + y) *
                            config['cell_size'],
                            config['cell_size'],
                            config['cell_size']), 1)

    # This function draws the next stone to be used in the sidebar
    def draw_next_stone(self, stone_matrix, offset):
        offset_x, offset_y = offset
        for y, row in enumerate(stone_matrix):
            for x, val in enumerate(row):
                if val:
                    # Draws the solid stone
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (offset_x + x) *
                            config['cell_size'],
                            (offset_y + y) *
                            config['cell_size'],
                            config['cell_size'],
                            config['cell_size']), 0)

                    # Draws the outline of the stone
                    pygame.draw.rect(
                        self.screen,
                        border_color,
                        pygame.Rect(
                            (offset_x + x) *
                            config['cell_size'],
                            (offset_y + y) *
                            config['cell_size'],
                            config['cell_size'],
                            config['cell_size']), 1)

    # This function handles moving from left to right by 'col' size
    def move(self, delta_x):
        if not self.gameover and not self.paused:
            move_x = self.stone_x + delta_x
            if move_x < 0:
                move_x = 0
            if move_x > config['cols'] - len(self.stone[0]):
                move_x = config['cols'] - len(self.stone[0])

            # Checks if a stone can make a legal move, aka no stones near
            if not collision_detection(self.area,
                                       self.stone,
                                       (move_x, self.stone_y)):
                self.stone_x = move_x

    # Simple quit function
    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    # Handles the dropping of the stone when the down arrow is pressed
    def drop_stone(self):
        if not self.gameover and not self.paused:
            self.stone_y += 1
            if collision_detection(self.area,
                                   self.stone,
                                   (self.stone_x, self.stone_y)):
                # Join stones after 'settle'
                self.area = join_stones(
                    self.area,
                    self.stone,
                    (self.stone_x, self.stone_y))
                # Set next stone to 'next' stone
                self.stone = self.stoneArray[1]
                # Create a new stone in 'next up'
                self.new_stone()
                # Pick a new random comment
                self.commentVal = rand(len(self.comments))
                while True:
                    # Check the rows of the board
                    for i, row in enumerate(self.area[:-1]):
                        # If theres no empty spaces left on the board, remove row
                        if 0 not in row:
                            self.area = remove_row(
                                self.area, i)
                            self.score = self.score + 1
                            break
                    else:
                        break

    def rotate_stone(self):
        # If game isn't over and not paused then rotate stone
        if not self.gameover and not self.paused:
            new_stone = rotate_stone(self.stone)
            # If collision is detected then don't allow rotation
            if not collision_detection(self.area,
                                       new_stone,
                                       (self.stone_x, self.stone_y)):
                # Set in-play stone to new stone
                self.stone = new_stone

    # Pause function
    def toggle_pause(self):
        self.paused = not self.paused

    # Simply restart game function
    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    # Function for handling comments in the sidebar
    def yus_comments(self):
        # Parse the string in a way that pygame can read it
        for i, line in enumerate(self.comments[self.commentVal].splitlines()):
            msg_image = pygame.font.Font(
                pygame.font.get_default_font(), 18).render(
                line, False, (0, 0, 0), (255, 255, 255))
        # Display the photo that follows the pieces
        self.screen.blit(self.yu, ((self.stone_x + 500), (self.stone_y + 300)))
        # Display the message above it
        self.screen.blit(msg_image, ((self.stone_x + 500), (self.stone_y + 300)))

    # Main game loop
    def run(self):
        key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': self.drop_stone,
            'UP': self.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game
        }

        self.gameover = False
        self.paused = False

        pygame.time.set_timer(pygame.USEREVENT + 1, config['delay'])
        tick = pygame.time.Clock()
        while 1:
            # Create grid lines on each tick
            grid_lines(self.screen)
            # Create yu comments on each tick
            self.yus_comments()

            # Check if game is over
            if self.gameover:
                self.center_msg("Game Over! Press space to continue")
                self.score = 0
                # Check if game is paused
            else:
                if self.paused:
                    self.center_msg("Paused")
                    # Else continue game
                else:
                    self.draw_stone(self.area, (0, 0))
                    self.draw_stone(self.stone,
                                    (self.stone_x,
                                     self.stone_y))
                    self.draw_next_stone(self.stoneArray[1], (13, 3))
                    # Draw score on each valid tick (Game isn't over, or paused)
                    self.top_msg("Score: " + str(self.score))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop_stone()
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
