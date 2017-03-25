import sys  # used for file reading
import time  # used for timing the path-finding
import pygame as pg  # used for drawing / event handling
from settings import *  # use a separate file for all the constant settings

from grid_student import Grid


# RLGridWorld class which implements the graphical interface for this assignment
class RLGridWorld:
    # constuctor which initializes the interface and the underlying grid object
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        pg.key.set_repeat(500, 100)
        self.__clock = pg.time.Clock()
        # set the grid object here to include either the solution or your own implementation
        self.__grid = Grid(MAPFILE)
        self.__width = self.__grid.cols() * TILESIZE
        self.__height = self.__grid.rows() * TILESIZE
        self.__screen = pg.display.set_mode((self.__width, self.__height))
        self.__font = pg.font.SysFont(FONTNAME, 12)

        # game main loop update function

    def update(self):
        self.__events()  # handle all mouse and keyboard events
        self.__draw()  # draw everything to the screen

    # draw everything to the screen
    def __draw(self):
        self.__draw_tiles()
        self.__draw_grid_lines()
        pg.display.flip()

    # draw all the tiles with values and policy
    def __draw_tiles(self):
        for r in range(self.__grid.rows()):
            for c in range(self.__grid.cols()):
                # if the tile is not walkable, just draw a grey tile
                if self.__grid.get_state(r, c) != STATE_WALKABLE:
                    self.__draw_tile(self.__screen, r, c, TILECOLOR[self.__grid.get_state(r, c)], 1)
                # otherwise we should color it based on our current value estimate
                else:
                    value = self.__grid.get_value(r, c)
                    color = [255, 255, 255]
                    min, max = self.__grid.get_min_value(), self.__grid.get_max_value()
                    if value < 0:
                        color = [255, 255 - abs(value / min) * 255, 255 - abs(value / min) * 255]
                    elif value > 0:
                        color = [255 - abs(value / max) * 255, 255, 255 - abs(value / max) * 255]
                    self.__draw_tile(self.__screen, r, c, color, 1)
                    # draw the value on the tile
                    self.__draw_text('%.2f' % self.__grid.get_value(r, c), (c * TILESIZE + 2, r * TILESIZE + 2), BLACK,
                                     self.__font)
                    # draw the reward on the tile
                    if self.__grid.get_reward(r, c) != 0:
                        self.__draw_text("R=" + str(self.__grid.get_reward(r, c)),
                                         (c * TILESIZE + 2, (r + 1) * TILESIZE - 12), BLACK, self.__font)
                    # draw the policy on the tile
                    policy = self.__grid.get_policy(r, c)
                    center = (int(c * TILESIZE + TILESIZE / 2), int(r * TILESIZE + TILESIZE / 2))
                    pg.draw.circle(self.__screen, BLACK, center, 2)
                    for i in range(len(LEGAL_ACTIONS)):
                        length = (TILESIZE / 2) * (0.5 if policy[i] > 0 else 0)
                        pg.draw.line(self.__screen, BLACK, center, (
                        center[0] + length * LEGAL_ACTIONS[i][1], center[1] + length * LEGAL_ACTIONS[i][0]))

    # draw the grid lines
    def __draw_grid_lines(self):
        for r in range(self.__grid.rows()):
            pg.draw.line(self.__screen, GRIDCOLOR, (0, r * TILESIZE), (self.__width, r * TILESIZE))
        for c in range(self.__grid.cols()):
            pg.draw.line(self.__screen, GRIDCOLOR, (c * TILESIZE, 0), (c * TILESIZE, self.__height))

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
                if event.key == pg.K_s:      self.__grid.update_values(); self.__grid.update_policy()
                if event.key == pg.K_v:      self.__grid.update_values()
                if event.key == pg.K_p:      self.__grid.update_policy()
                if event.key == pg.K_r:      self.__grid = Grid(MAPFILE)
            if event.type == pg.MOUSEBUTTONDOWN:
                row, col = self.__get_state(event.pos)
                if pg.mouse.get_pressed()[0]:
                    print("\nState:  ", row, col)
                    print("Value:  ", self.__grid.get_value(row, col))
                    print("Policy: ", self.__grid.get_policy(row, col))


# create the game object
g = RLGridWorld()

# run the main game loop
while True:
    g.update()