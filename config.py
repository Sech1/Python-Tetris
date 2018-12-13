# Define the size of the tetris playing area
config = {
    'cell_size': 40,
    'cols': 12,
    'rows': 16,
    'delay': 750,
    'maxfps': 30
}

# Define the total size of the screen, including the sizebar
screen_config = {
    'cell_size': 40,
    'cols': 20,
    'rows': 16,
    'delay': 750,
    'maxfps': 30
}

# Define the sets of colors used for tetris shapes
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

# Define the border color of shapes
border_color = (255, 0, 119)

# Define the list of all tetris shapes
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
