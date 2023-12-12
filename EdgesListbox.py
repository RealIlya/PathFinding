from tkinter import Listbox, END

import Constants
from graph_elements import Edge


class EdgesListBox(Listbox):

    def __init__(self, master):
        super().__init__(master, highlightthickness=1, highlightbackground="red", font="Roboto 11",
                         foreground=Constants.EDGE_LIST_BOX_TEXT_COLOR)

        self.edge_list = []
        self.__on_element_selected = None

        def on_select(event):
            index = int(event.widget.curselection()[0])
            element = self.edge_list[index]
            self.__on_element_selected(element)

        self.bind("<<ListboxSelect>>", on_select)

    def add_edge(self, edge: Edge):
        self.edge_list.append(edge)
        self.insert(END, f"{edge.get_start_tag()} - {edge.get_end_tag()} edge")

    def clear(self):
        self.delete(0, END)
        self.edge_list.clear()

    def set_on_element_selected(self, on_selected):
        self.__on_element_selected = on_selected
