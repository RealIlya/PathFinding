import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import Literal

from Cells import Cells
from EdgesListbox import EdgesListBox
from FrameMenu import FrameMenu
from Graph import Graph
from graph_elements.Edge import Edge
from graph_elements.Vertex import Vertex


class App(tk.Tk):
    edges = []

    def __init__(self):
        super().__init__()
        self.title("App")
        self.geometry("800x400")
        self.cells_frame = tk.Frame(self)
        self.cells_frame.place(relwidth=0.8, relheight=1)
        self.cells = Cells(self.cells_frame, 800, 400)
        self.cells.pack(expand=True, fill=tk.BOTH)

        self.edges_list_box_frame = tk.Frame(self)
        self.edges_list_box_frame.place(relx=0.8, relwidth=0.2, relheight=1)
        self.edges_list_box = EdgesListBox(self.edges_list_box_frame)
        self.edges_list_box.pack(expand=True, fill=tk.BOTH)
        self.edges_list_box.set_on_element_selected(self.on_edge_selected)

        self.frame_menu = FrameMenu(self)
        self.frame_menu.pack()
        self.init_frame_menu_commands()

        self.config(menu=self.frame_menu.get_menu())

        self.cells.set_on_vertex_click_listener(self.on_vertex_click)
        self.cells.set_on_edge_click_listener(self.on_edge_click)

        self.__vertex_buffer = None

        self.show_grid = False

    def init_frame_menu_commands(self):
        self.frame_menu.add_command("Clear", self.clear_all)
        switches = {"A to B arc": lambda: self.switch_direction("last"),
                    "Edge": lambda: self.switch_direction("both")}
        self.frame_menu.add_cascade_commands("Switch Direction", switches)
        self.frame_menu.add_command("Find Shortest Path", self.find_shortest_path)
        self.frame_menu.add_command("Grid", self.set_grid)
        self.frame_menu.add_command("Clear Selection", self.clear_selection)

    def set_grid(self):
        self.show_grid = not self.show_grid
        self.cells.set_is_grid_on(self.show_grid)

    def clear_selection(self):
        self.cells.clear_selection()

    def check_edges_on_weights(self, edges):
        for edge in edges:
            if edge.get_weight() is None:
                messagebox.showerror("Error", "Set all weights")
                return False

        return True

    def find_shortest_path(self):
        self.cells.clear_selection()

        if len(App.edges) > 0:
            if not self.check_edges_on_weights(App.edges):
                return
            result = simpledialog.askstring("Popup", "Input source and destination vertices",
                                            parent=self)
            if result is None:
                return
            result = result.split()
            if len(result) < 2:
                return
            source, destination = result
            if source.isdigit() and destination.isdigit():
                source = int(source)
                destination = int(destination)
            else:
                return

            graph = Graph(len(self.cells.points))
            for edge in App.edges:
                for tuple_ in edge.get_numbers_tuple():
                    if tuple_ is not None:
                        graph.add_edge(*tuple_)

            path, length = graph.find_shortest_path(source, destination)

            if path is not None:
                if length == float("inf"):
                    messagebox.showinfo("Path not found!",
                                        f"The path from {source} to {destination} does not exist!")
                    return

                for i in range(1, len(path)):
                    self.cells.draw_arrow_between_points_with_indexes(path[i - 1], path[i])
                messagebox.showinfo("Path found!",
                                    f"The shortest path from {source} to {destination} is {length}")
            else:
                messagebox.showinfo("Path not found!",
                                    f"The path from {source} to {destination} contains a negative weight cycle")

    def on_vertex_click(self, tag, direction: Literal["last", "both"]):
        if self.__vertex_buffer is None:
            self.__vertex_buffer = self.search_by_tag(tag)

        else:
            new_vertex = Vertex(tag)
            if self.__vertex_buffer == new_vertex:
                return

            edge = Edge(self.__vertex_buffer, new_vertex, direction)
            App.edges.append(edge)
            self.edges_list_box.add_edge(edge)

            self.draw_edge(edge, len(App.edges) - 1)
            self.__vertex_buffer = None

    def on_edge_selected(self, edge: Edge):
        if edge.get_weight() is None:
            weight = simpledialog.askinteger("Popup", "Input weight", parent=self)
            if weight is None:
                return
            edge.set_weight(weight)
            index1 = int(''.join(s for s in edge.get_start_tag() if s.isdigit()))
            index2 = int(''.join(s for s in edge.get_end_tag() if s.isdigit()))
            self.cells.draw_number_arrow_between_points_with_indexes(weight, index1, index2)

    def on_edge_click(self, tag, callback):
        index = int(''.join(s for s in tag if s.isdigit()))
        edge = App.edges[index]
        if edge.get_weight() is None:
            weight = simpledialog.askinteger("Popup", "Input weight", parent=self)
            if weight is None:
                return
            edge.set_weight(weight)
            callback(weight)

    def search_by_tag(self, tag):
        for edge in App.edges:
            if tag == edge.get_start_tag():
                return edge.get_start_vertex()
            if tag == edge.get_end_tag():
                return edge.get_end_vertex()

        return Vertex(tag)

    def draw_edge(self, edge: Edge, index):
        self.cells.create_arrow(edge.get_start_tag(), edge.get_end_tag(), edge.get_direct(), index)

    def clear_all(self):
        App.edges.clear()
        self.__vertex_buffer = None

        self.cells.clear_arrows()
        self.cells.clear_points()
        self.cells.clear_numbers()

        self.edges_list_box.clear()

    def switch_direction(self, direction):
        self.cells.set_arrow_direction(direction)
