import sys, time, copy, random, math, time
import pygame as pg
import sudoku
import matplotlib.pyplot as plt

from settings import *  # use a separate file for all the constant settings

import ga_student as GA

# RLGridWorld class which implements the graphical interface for this assignment
class SudokuVis:
    # constuctor which initializes the interface and the underlying grid object
    def __init__(self, board, settings):
        pg.init()
        pg.display.set_caption(TITLE)
        pg.key.set_repeat(500, 100)
        self.__clock = pg.time.Clock()
        # set the grid object here to include either the solution or your own implementation
        self.__board = board
        self.__prev_board = board
        self.__width = (self.__board.size() + 1) * TILESIZE
        self.__height = (self.__board.size() + 1) * TILESIZE
        self.__screen = pg.display.set_mode((self.__width, self.__height))
        self.__fontsize = int(TILESIZE / 2)
        self.__font = pg.font.SysFont(FONTNAME, self.__fontsize)
        self.__settings = settings

    def __set_board(self, board):
        self.__prev_board = copy.deepcopy(self.__board)
        self.__board = copy.deepcopy(board)

    # game main loop update function
    def update(self, board):
        self.__set_board(board)
        self.__events()  # handle all mouse and keyboard events
        self.__draw()  # draw everything to the screen

    # draw everything to the screen
    def __draw(self):
        self.__draw_sudoku()
        self.__draw_grid_lines()
        pg.display.flip()

    # draw all the tiles with values and policy
    def __draw_sudoku(self):
        sqsize = int(math.sqrt(self.__board.size()))
        row_counts = [self.__board.row_count(r) for r in range(self.__board.size())]
        col_counts = [self.__board.col_count(c) for c in range(self.__board.size())]
        val_pos = TILESIZE / 2 - self.__fontsize / 2
        darken = 50
        for r in range(self.__board.size()):
            for c in range(self.__board.size()):
                sq_counts = self.__board.square_count(r // sqsize, c // sqsize)
                val = self.__board.get(r, c)
                color = (255, 255, 255) if 0 in sq_counts[1:] else (0, 255, 0)
                same = self.__prev_board.get(r, c) == val
                if row_counts[r][val] != 1: color = (color[0] - darken, color[1] - darken, color[2] - darken)
                if col_counts[c][val] != 1: color = (color[0] - darken, color[1] - darken, color[2] - darken)
                if sq_counts[val] != 1:     color = (color[0] - darken, color[1] - darken, color[2] - darken)
                color = (max(0, color[0]), max(0, color[1]), max(0, color[2]))
                self.__draw_tile(self.__screen, r, c, color if same else YELLOW, 1)
                self.__draw_text(str(val), (c * TILESIZE + val_pos, r * TILESIZE + val_pos), BLACK, self.__font)
        # draw unique row and column counts
        for r in range(self.__board.size()):
            unique = sum([1 if i > 0 else 0 for i in row_counts[r]])
            self.__draw_tile(self.__screen, r, self.__board.size(), GREEN if unique == self.__board.size() else RED, 1)
            self.__draw_text(str(unique), ((self.__board.size()) * TILESIZE + val_pos, r * TILESIZE + val_pos), BLACK,
                             self.__font)
        for c in range(self.__board.size()):
            unique = sum([1 if i > 0 else 0 for i in col_counts[c]])
            self.__draw_tile(self.__screen, self.__board.size(), c, GREEN if unique == self.__board.size() else RED, 1)
            self.__draw_text(str(unique), (c * TILESIZE + val_pos, (self.__board.size()) * TILESIZE + val_pos), BLACK,
                             self.__font)

    # draw the grid lines
    def __draw_grid_lines(self):
        for r in range(self.__board.size() + 1):
            thickness = 3 if r > 0 and r % int(math.sqrt(self.__board.size())) == 0 else 1
            pg.draw.line(self.__screen, GRIDCOLOR, (0, r * TILESIZE), (self.__width, r * TILESIZE), thickness)
        for c in range(self.__board.size() + 1):
            thickness = 3 if c > 0 and c % int(math.sqrt(self.__board.size())) == 0 else 1
            pg.draw.line(self.__screen, GRIDCOLOR, (c * TILESIZE, 0), (c * TILESIZE, self.__height), thickness)

    # draw a tile location with given parameters
    def __draw_tile(self, surface, row, col, color, size):
        surface.fill(color, (col * TILESIZE, row * TILESIZE, TILESIZE * size, TILESIZE * size))

    # draws text to the screen at a given location
    def __draw_text(self, text, pos, color, font):
        label = font.render(text, 1, color)
        self.__screen.blit(label, pos)

    # called when the program is closed
    def __quit(self):
        pg.quit()
        sys.exit()

        # returns the tile on the grid underneath a given mouse position in pixels

    def __get_state(self, mpos):
        return mpos[1] // TILESIZE, mpos[0] // TILESIZE

        # events and input handling

    def __events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: self.__quit()


# the size of the sudoku puzzle we will be solving
sudoku_size = 9

# get the genetic algorithm settings
settings = GA.get_ga_settings(sudoku_size)

# construct a new sudoku puzzle and randomize it
board = sudoku.Sudoku(sudoku_size)
board.randomize()

# construct the sudoku visualization
vis = SudokuVis(board, settings)

# keep some stats about our population's evolution so we can plot them
max_pop_fitness = []
min_pop_fitness = []
avg_pop_fitness = []

# define an initial population to pass into the GA
population = []
for i in range(settings.population_size):
    population.append([random.choice(settings.individual_values) for i in range(settings.individual_size)])

# plot-related variables and function
generations, x = 0, []
plt.ion()


def update_plot():
    global generations
    x.append(generations)
    # only re-plot the graph every so many generations (it gets very slow with large lists)
    if generations % 50 == 0:
        plt.scatter(x, avg_pop_fitness, color='blue')
        plt.scatter(x, min_pop_fitness, color='purple')
        plt.scatter(x, max_pop_fitness, color='red')
        plt.pause(0.01)


# there is no termination condition for the assignment
initial_time = time.clock()
while True:

    # compute the next generation from the current one, this will call the function you wrote
    population = GA.evolve(population, settings)

    # compute some simple stats on the population
    pop_fitness = list(map(settings.fitness_function, population))

    # compute the max, min, and avg fitnesses
    max_gen_fitness = max(pop_fitness)
    min_gen_fitness = min(pop_fitness)
    avg_gen_fitness = sum(pop_fitness) / len(pop_fitness)
    max_pop_fitness.append(max_gen_fitness)
    min_pop_fitness.append(min_gen_fitness)
    avg_pop_fitness.append(avg_gen_fitness)

    # see if we have a new best individual
    generation_best = max(population, key=settings.fitness_function)

    # print out the values every so many generations
    if generations % 10 == 0:
        print("Gen", generations, ": GenMax =", max_gen_fitness, "GenAvg =", avg_gen_fitness, " GenPerSec =",
              generations / (time.clock() - initial_time))

    # update the fitness graph, comment the next line out if you don't want it to be displayed
    # note: if you try to click and drag the graph while it's drawing it will crash the program
    update_plot()

    # update the sudoku board visualization
    board.set_arr(generation_best)
    vis.update(board)
    generations += 1