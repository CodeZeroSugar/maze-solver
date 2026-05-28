from graphics import Line, Point


class Cell:
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.__win is not None:
            self.__win.draw_line(
                Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)),
                "black" if self.has_left_wall else "white",
            )
            self.__win.draw_line(
                Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)),
                "black" if self.has_top_wall else "white",
            )
            self.__win.draw_line(
                Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)),
                "black" if self.has_right_wall else "white",
            )
            self.__win.draw_line(
                Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)),
                "black" if self.has_bottom_wall else "white",
            )

    def draw_move(self, to_cell, undo=False):
        half_length = abs(self.__x2 - self.__x1) // 2
        c1_x = half_length + self.__x1
        c1_y = half_length + self.__y1

        half_length2 = abs(to_cell.__x2 - to_cell.__x1) // 2
        c2_x = half_length2 + to_cell.__x1
        c2_y = half_length2 + to_cell.__y1

        if self.__win is None:
            return
        self.__win.draw_line(
            Line(Point(c1_x, c1_y), Point(c2_x, c2_y)), "red" if undo else "gray"
        )
