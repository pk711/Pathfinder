import pygame

RED = (255, 0, 0)
BLUE = (100, 149, 240)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
TURQUOISE = (64, 224, 208)
CYAN = (137, 200, 240)

class Cube:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == CYAN

    def is_open(self):
        return self.color == BLUE

    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = CYAN

    def make_open(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE

    def make_start(self):
        self.color = ORANGE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self. neighbours = []
        #Checks if we can go DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): 
            self.neighbours.append(grid[self.row + 1][self.col])
        #UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])
        #RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): 
            self.neighbours.append(grid[self.row][self.col + 1])
        #LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): 
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False