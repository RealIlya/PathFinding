import math
from tkinter import Canvas
from typing import Literal, Callable

import Constants
from Constants import *


class Cells(Canvas):
    GRID_TAG = "grid_line"
    POINT_TAG = "point"
    ARROW_TAG = "arrow"
    NUMBER_TAG = "number"
    SELECTION = "selection"

    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, highlightthickness=1, highlightbackground="black")

        self.set_arrow_direction("last")

        self.__on_vertex_click_listener = None
        self.__on_edge_click_listener = None

        self.points = []
        self.__is_grid_on = False

    def _draw_vertex(self, event, x0, y0, direction):
        for i in range(len(self.points)):
            if (self.points[i][0] - x0) ** 2 + (self.points[i][1] - y0) ** 2 <= VERTEX_CLICK_RADIUS ** 2:
                self.__on_vertex_click_listener(Cells.POINT_TAG + str(i), direction)
                return

        circle = (event.x - x0) ** 2 + (event.y - y0) ** 2
        if circle <= VERTEX_CLICK_RADIUS ** 2:
            self.points.append((x0, y0))

            index = str(len(self.points) - 1)
            tag = Cells.POINT_TAG + index
            self.create_point(x0, y0, VERTEX_COLOR, tag)
            self.__on_vertex_click_listener(tag, direction)

            self.create_number(x0, y0, index, VERTEX_TITLE_SIZE, extra_tag=tag)

    def _on_cell_cross_click(self, event, direction):
        kx = event.x
        ky = event.y

        if self.__is_grid_on:
            kx = round(kx / CELL_SIZE) * CELL_SIZE
            ky = round(ky / CELL_SIZE) * CELL_SIZE

        self._draw_vertex(event, kx, ky, direction)

    def create_point(self, x, y, fill, tag, outline=VERTEX_OUTLINE_COLOR):
        x0 = x - VERTEX_RADIUS
        y0 = y - VERTEX_RADIUS
        x1 = x + VERTEX_RADIUS
        y1 = y + VERTEX_RADIUS
        self.create_oval(x0, y0, x1, y1, fill=fill, outline=outline, tags=[Cells.POINT_TAG, tag])

    def create_number_near_arrow(self, x0, y0, x1, y1, number, font_size, extra_tag=None):
        tags = [Cells.NUMBER_TAG]
        if extra_tag is not None:
            tags.append(extra_tag)

        ax = x1 - x0  # vector x
        ay = y1 - y0  # vector y
        pi = math.atan2(ay, ax) - math.pi / 2
        cos_alpha = math.cos(pi)
        sin_alpha = math.sin(pi)

        x, y = (x1 + x0) / 2, (y1 + y0) / 2
        self.create_text(x + 20 * cos_alpha, y + 20 * sin_alpha, text=str(number), font=f"Roboto {font_size}",
                         fill=WEIGHT_COLOR, tags=tags)

    def create_number(self, x, y, number, font_size, extra_tag=None):
        tags = [Cells.NUMBER_TAG]
        if extra_tag is not None:
            tags.append(extra_tag)

        self.create_text(x, y + 20, text=str(number), font=f"Roboto {font_size}", fill=VERTEX_TITLE_COLOR, tags=tags)

    def create_arrow(self, tag_start, tag_end, direction, index):
        x0, y0 = 0, 0
        x1, y1 = 0, 0

        for i in range(len(self.points)):
            if (Cells.POINT_TAG + str(i)) == tag_start:
                x0, y0 = self.points[i]
                break

        for i in range(len(self.points)):
            if (Cells.POINT_TAG + str(i)) == tag_end:
                x1, y1 = self.points[i]
                break
        else:
            return

        tag = Cells.ARROW_TAG + str(index)
        self.create_line(x0, y0, x1, y1, fill=EDGE_COLOR, width=EDGE_WIDTH, arrow=direction,
                         arrowshape=Constants.ARROW_SHAPE, tags=[Cells.ARROW_TAG, tag])
        self.tag_bind(tag, "<ButtonPress-3>", lambda event: self.__on_arrow_click(event, x0, y0, x1, y1))

    def __on_arrow_click(self, event, x0, y0, x1, y1):
        id_ = event.widget.find_withtag('current')
        tag = self.gettags(id_)[1]

        def callback(number):
            self.create_number_near_arrow(x0, y0, x1, y1, number, WEIGHT_SIZE)

        self.__on_edge_click_listener(tag, callback)

    def set_arrow_direction(self, direction: Literal["last", "both"]):
        self.bind("<ButtonPress-1>", lambda event: self._on_cell_cross_click(event, direction))

    def draw_number_arrow_between_points_with_indexes(self, number, index1, index2):
        p1 = self.points[index1]
        p2 = self.points[index2]
        self.create_number_near_arrow(*p1, *p2, number, WEIGHT_SIZE)

    def draw_arrow_between_points_with_indexes(self, index1, index2):
        p1 = self.points[index1]
        p2 = self.points[index2]
        self.create_line(*p1, *p2, fill=SELECTION_COLOR, width=SELECTION_WIDTH, arrow="last",
                         arrowshape=Constants.ARROW_SHAPE, tags=[Cells.ARROW_TAG, Cells.SELECTION])

    def _clear(self):
        self.delete("grid_line")

    def clear_points(self):
        self.delete(Cells.POINT_TAG)
        self.points.clear()

    def clear_arrows(self):
        self.delete(Cells.ARROW_TAG)

    def clear_numbers(self):
        self.delete(Cells.NUMBER_TAG)

    def clear_selection(self):
        self.delete(Cells.SELECTION)

    def set_on_vertex_click_listener(self, listener: Callable[[str, str], None]):
        self.__on_vertex_click_listener = listener

    def set_on_edge_click_listener(self, listener: Callable[[str, Callable[[], None]], None]):
        self.__on_edge_click_listener = listener

    def set_is_grid_on(self, grid_on):
        self.__is_grid_on = grid_on
