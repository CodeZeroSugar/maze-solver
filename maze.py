from cell import Cell
import time
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win

        if seed is not None:
            random.seed(seed)

        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.__num_cols):
            col_cells = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.025)

    def __break_entrance_and_exit(self):
        entry_cell = self.__cells[0][0]
        entry_cell.has_top_wall = False
        self.__draw_cell(0, 0)
        exit_cell = self.__cells[-1][-1]
        exit_cell.has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            need_to_visit = []
            if j + 1 < len(self.__cells[i]) and not self.__cells[i][j + 1].visited:
                need_to_visit.append((i, j + 1))
            if j - 1 > -1 and not self.__cells[i][j - 1].visited:
                need_to_visit.append((i, j - 1))
            if i + 1 < len(self.__cells) and not self.__cells[i + 1][j].visited:
                need_to_visit.append((i + 1, j))
            if i - 1 > -1 and not self.__cells[i - 1][j].visited:
                need_to_visit.append((i - 1, j))
            if len(need_to_visit) == 0:
                self.__draw_cell(i, j)
                return
            next_i, next_j = need_to_visit[random.randrange(0, len(need_to_visit))]
            if next_i > i:
                self.__cells[i][j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            if next_i < i:
                self.__cells[i][j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
            if next_j > j:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False
            if next_j < j:
                self.__cells[i][j].has_top_wall = False
                self.__cells[next_i][next_j].has_bottom_wall = False
            self.__break_walls_r(next_i, next_j)

    def __reset_cells_visited(self):
        for i in range(len(self.__cells)):
            for j in range(len(self.__cells[i])):
                self.__cells[i][j].visited = False

    def __solve_r(self, i=0, j=0):
        self.__animate()
        self.__cells[i][j].visited = True
        if (i, j) == (len(self.__cells) - 1, len(self.__cells[-1]) - 1):
            return True

        if (
            j + 1 < len(self.__cells[i])
            and not self.__cells[i][j].has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self.__solve_r(i, j + 1):
                return True
            self.__cells[i][j].draw_move(self.__cells[i][j + 1], undo=True)
        if (
            j - 1 > -1
            and not self.__cells[i][j].has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self.__solve_r(i, j - 1):
                return True
            self.__cells[i][j].draw_move(self.__cells[i][j - 1], undo=True)
        if (
            i + 1 < len(self.__cells)
            and not self.__cells[i][j].has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self.__solve_r(i + 1, j):
                return True
            self.__cells[i][j].draw_move(self.__cells[i + 1][j], undo=True)
        if (
            i - 1 > -1
            and not self.__cells[i][j].has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self.__solve_r(i - 1, j):
                return True
            self.__cells[i][j].draw_move(self.__cells[i - 1][j], undo=True)

        return False

    def solve(self):
        return self.__solve_r()
