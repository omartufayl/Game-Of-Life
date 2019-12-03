"""
Game of Life
by Omar Tufayl

GameOfLife() spawns a grid populated with Cells() that live/die according to
the following rules:

  When a live cell:
    - has fewer than two neighbours, this cell dies
    - has more than three neighbours, this cell dies
    - has two or three neighbours, this cell stays alive

  When an empty position:
    - has exactly three neighbouring cells, a cell is created in its position
        - otherwise, it remains empty
"""
from __future__ import print_function
try:
    # for Python2, uppercase T in Tkinter
    from Tkinter import Tk, Frame, Canvas
except ImportError:
    # for Python3, lowercase 't' in tkinter
    from tkinter import Tk, Frame, Canvas
import random


class Cell:
    """Generates cells and binds to canvas, changes cell state to alive or
        dead, calculates number of alive neighbours for cell and
        determines cell fate according to particular rules

        Arguments:
            parent (): ...
            x (): ...
            y (): ...
            row (): ...
            col (): ...

        Attributes:
            parent (): ...
            rect_id (): ...
            row (): ...
            col (): ...
            alive (): ...
    """

    def __init__(self, parent, x, y, row, col):
        """ bind cell to canvas and set default state to dead """
        self.parent = parent
        self.rect_id = self.parent.canvas.create_rectangle(x, y, x+10, y+10, fill="black")
        self.row = row
        self.col = col
        self.alive = False

    def __str__(self):
        """ for testing, returns cell's position in grid """
        return "(" + str(self.row,) + ", " + str(self.col) + ")"

    def change_colour(self):
        """ invert the cell alive state and accordinly change cell colour """
        if not self.alive:
            self.parent.canvas.itemconfig(self.rect_id, fill="green")
            self.alive = True
        else:
            self.reset()

    def reset(self):
        """ reset cell to dead """
        self.parent.canvas.itemconfig(self.rect_id, fill="black")
        self.alive = False

    def alive_neighbours(self):
        """ return how many alive neighbours this cell has """
        num_alive = 0
        for i in (self.row-1, self.row, self.row+1):
            for j in (self.col-1, self.col, self.col+1):
                if i == self.row and j == self.col:
                    continue
                if i == -1 or j == -1:
                    continue
                try:
                    if self.parent.grid[i][j].alive:
                        num_alive += 1
                except IndexError:
                    pass
        return num_alive

    def cell_fate(self):
        """ these rules determine if a cell dies, or is created """
        alive_neighbours = self.alive_neighbours()
        if self.alive:
            return alive_neighbours < 2 or alive_neighbours > 3
        else:
            return alive_neighbours == 3


class GameOfLife():
    """Creates grid for cells, locates cell position on grid, changes cell state
        before start of game, provides methods for start, stop, reset and
        random game generation to bind to UI

        Arguments:
            root (Tk): bind Tkinter root to GameOfLife()

        Attributes:
            game_id (int):
            grid (list):
            board_size (int):
            root (Tk):
            frame (Frame):
            canvas (Canvas):
    """

    def __init__(self, tkinter_root):
        """ initiate Game Of Life using Tkinter, create grid and UI """
        self.game_id = 0
        self.grid = []
        board_size = 520
        self.root = tkinter_root
        self.root.title("Game of Life by Omar Tufayl")
        self.frame = Frame(root, width=board_size, height=board_size)
        self.frame.pack()
        self.canvas = Canvas(self.frame, width=board_size, height=board_size)
        self.canvas.pack()
        self.create_grid()
        self.user_interface()

    def create_grid(self):
        """ makes the game board """
        x = 10
        y = 10
        for row in range(50):
            self.grid.append([])
            for col in range(50):
                self.grid[row].append(Cell(self, x, y, row, col))
                x += 10
            x = 10
            y += 10

    def get_cell_position(self, x, y):
        """ using cell x, y coordinates, calculate the cell column, row """
        return (int((y/10)-1), int((x/10)-1))

    def toggle_cell(self, event):
        """ invert cell alive state and colour on user click """
        row, col = self.get_cell_position(event.x, event.y)
        cell = self.grid[row][col]
        cell.change_colour()

    def start_game(self):
        """ loop through all cells and determine their fate, then loop game """
        self.stop_game()
        change_cells = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                cell = self.grid[row][col]
                if cell.cell_fate():
                    change_cells.append(cell)

        for cell in change_cells:
            cell.change_colour()

        self.game_id = self.root.after(100, self.start_game)
        print("Game iteration: " + str(self.game_id[6:]))

    def random_game(self):
        """ randomly assign state to all cells, then start game """
        self.stop_game()
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                cell = self.grid[row][col]
                cell.alive = random.choice([False, True, False])
        self.start_game()

    def stop_game(self):
        try:
            self.root.after_cancel(self.game_id)
        except (NameError, AttributeError):
            pass

    def reset_game(self):
        """ assign all cells default dead state """
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                cell = self.grid[row][col]
                cell.reset()

    def user_interface(self):
        """ displays UI elements, binding them to relevant method calls """
        instructions = "Click anywhere to activate cells, then press start to run the simulation."
        Label(self.frame, text=instructions).pack()
        start = Button(self.root, text=u"\u25B6  Start", width=15, command=self.start_game)
        start.pack(side=LEFT, pady=20, padx=20)
        random_start = Button(self.root, text="Random", width=7, command=self.random_game)
        random_start.pack(side=LEFT, pady=20, padx=10)
        stop = Button(self.root, text="Stop", width=7, command=self.stop_game)
        stop.pack(side=LEFT, pady=20, padx=10)
        reset = Button(self.root, text="Reset", width=7, command=self.reset_game)
        reset.pack(side=RIGHT, pady=20, padx=20)
        self.canvas.bind("<Button-1>", self.toggle_cell)


if __name__ == '__main__':
    root = Tk()
    game = GameOfLife(root)
    root.mainloop()
