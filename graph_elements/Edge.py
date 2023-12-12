from typing import Literal

from graph_elements.Vertex import Vertex


class Edge:

    def __init__(self, vertex1: Vertex, vertex2: Vertex, direct: Literal["last", "both"]):
        self.__vertex1 = vertex1
        self.__vertex2 = vertex2
        self.__direct = direct
        self.__weight = None

    def get_start_vertex(self):
        return self.__vertex1

    def get_end_vertex(self):
        return self.__vertex2

    def get_start_tag(self):
        return self.__vertex1.tag

    def get_end_tag(self):
        return self.__vertex2.tag

    def get_direct(self):
        return self.__direct

    def get_weight(self):
        return self.__weight

    def set_weight(self, weight):
        self.__weight = weight

    def get_numbers_tuple(self):
        if self.__direct == "both":
            return [[self.__vertex1.get_number(), self.__vertex2.get_number(), self.__weight],
                    [self.__vertex2.get_number(), self.__vertex1.get_number(), self.__weight]]

        return [[self.__vertex1.get_number(), self.__vertex2.get_number(), self.__weight], None]
