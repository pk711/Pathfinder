from sqlite3 import Row
from turtle import pos, width
import pygame
import math
from queue import PriorityQueue
from cube import Cube

WIDTH = 900
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Fathfinder")

WHITE = (255, 255, 255)
GREY = (128, 128, 128)

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2 
    return abs(x1 - x2 ) + abs(y1 - y2)

def create_path(where_from, current, draw):
	while current in where_from:
		current = where_from[current]
		current.make_path()
		draw()

def find_path(draw, grid, start, end):
    count = 0
    set_open = PriorityQueue()
    set_open.put((0, count, start))
    where_from = {}
    curr_shortest = {cube: float("inf") for row in grid for cube in row}
    curr_shortest[start] = 0
    possible_dis = {cube: float("inf") for row in grid for cube in row}
    possible_dis[start] = h(start.get_pos(), end.get_pos())
    set_open_hash = {start}

    while not set_open.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = set_open.get()[2]
        set_open_hash.remove(current)

        if current == end:
            create_path(where_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_curr = curr_shortest[current] + 1

            if temp_curr < curr_shortest[neighbour]:
                where_from[neighbour] = current
                curr_shortest[neighbour] = temp_curr
                possible_dis[neighbour] = temp_curr + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in set_open_hash:
                    count += 1
                    set_open.put((possible_dis[neighbour], count, neighbour))
                    set_open_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cube = Cube(i, j, gap, rows)
            grid[i].append(cube)
    return grid 

def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))

def draw(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for cube in row:
            cube.draw(window)
    draw_grid(window, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x //gap 
    return row, col 

def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True 
    
    while run:
        draw(window, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False 

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cube = grid[row][col]

                if not start and cube != end:
                    start = cube 
                    start.make_start()
                elif not end and cube != start:
                    end = cube 
                    end.make_end()
                elif cube != start and cube != end:
                    cube.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cube = grid[row][col]
                cube.reset()

                if cube == start:
                    start = None
                if cube == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and start and end:
                    for row in grid:
                        for cube in row:
                            cube.update_neighbours(grid)
                    find_path(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_DELETE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WINDOW, WIDTH)