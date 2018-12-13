from config import *
import pygame


# This function handles the rotation of stones by creating a new stone and offsetting its matrix
def rotate_stone(shape):
    return [[shape[y][x] for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


# This function handles collision detection
def collision_detection(board, shape, offset):
    offset_x, offset_y = offset
    for cell_y, row in enumerate(shape):
        for cell_x, cell in enumerate(row):
            try:
                if cell and board[cell_y + offset_y][cell_x + offset_x]:
                    return True
            except IndexError:
                return True
    return False


# Removes a row if there is no empty space left in a row
def remove_row(area, row):
    del area[row]
    return [[0 for i in range(config['cols'])]] + area


# Joines stones when a stone/piece 'settles'
def join_stones(stone1, stone2, stone2_offset):
    off_x, off_y = stone2_offset
    for cell_y, row in enumerate(stone2):
        for cell_x, val in enumerate(row):
            stone1[cell_y + off_y - 1][cell_x + off_x] += val
    return stone1


# Creates a new game/screen based off of config settings
def new_screen():
    screen_size = [[0 for x in range(config['cols'] - 2)] for y in range(config['rows'])]
    screen_size += [[1 for x in range(config['cols'] - 2)]]
    return screen_size


# Handles grid lines, and sidebar and modifies the background color of sidebox.
def grid_lines(screen):
    white = 255, 255, 255
    blue = 0, 0, 255
    point1 = 403, 0
    point2 = 403, 700
    pygame.draw.line(screen, blue, point1, point2, 6)

    for x in range(1, config['cols'] - 2):
        point1 = (40 * x), 0
        point2 = (40 * x), 700
        pygame.draw.line(screen, white, point1, point2)

    for i in range(1, config['rows']):
        point3 = 0, (40 * i)
        point4 = 400, (40 * i)
        pygame.draw.line(screen, white, point3, point4)


def misc_gui_features(screen):
    text = "Next Shape: "

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, sidebar_back, [405, 0, 400, 700], 0)
    for i, line in enumerate(text.splitlines()):
        msg_image = pygame.font.Font(
            pygame.font.get_default_font(), 18).render(
            line, False, (0, 0, 0), (255, 255, 255))
    screen.blit(msg_image, (540, 50))
    pygame.draw.rect(screen, colors[0], [490, 75, 215, 150], 1)
