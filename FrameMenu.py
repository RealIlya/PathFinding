from tkinter import Frame, Menu


class FrameMenu(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.menu = Menu(self)

    def add_command(self, label, command):
        self.menu.add_command(label=label, command=command)

    def add_check(self, label, command, offvalue, onvalue, variable):
        self.menu.add_checkbutton(label=label, command=command, offvalue=offvalue, onvalue=onvalue, variable=variable)

    def add_cascade_commands(self, main_label, labels_commands: dict):
        sub_menu = Menu(tearoff=0)

        for label, command in labels_commands.items():
            sub_menu.add_radiobutton(label=label, command=command)

        self.menu.add_cascade(label=main_label, menu=sub_menu)

    def get_menu(self):
        return self.menu
