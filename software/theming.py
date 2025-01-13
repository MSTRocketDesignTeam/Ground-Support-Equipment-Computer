import tkinter as tk
import tkinter.font as font


class Custom_Button():
    def __init__(self, parent, text_, action):
        self.normal_color = 'white'
        self.text_color = 'black'
        self.hover_color = '#b0b0b0'
        self.active_color = '#94ff21'
        self._helv20 = font.Font(family='Helvetica', size=20)

        button = tk.Label(parent, text=text_, fg=self.text_color,
                          bg=self.normal_color, font=self._helv20, padx=15, pady=15, relief='raised')
        button.bind(
            '<Enter>', self.enter_action)
        button.bind(
            '<Leave>', self.leave_action)
        button.bind(
            '<Double-Button>', self.double_action)

        button.pack(pady=5)

        self.button = button
        self.enter_flag = False
        self.action = action

    def enter_action(self, event):
        self.enter_flag = True
        self.button.config(bg=self.hover_color)

    def leave_action(self, event):
        self.enter_flag = False
        self.button.config(bg=self.normal_color)

    def double_action(self, event):
        if self.enter_flag:
            self.action()
            self.button.config(bg=self.active_color)

        self.enter_flag = False

    def set_text(self, text_):
        self.button.config(text=text_)


class Custom_Panel():
    def __init__(self, root, row_, column_, text_):
        self.panel = tk.LabelFrame(root, text=text_, bg='black',
                                   fg='white', padx=15, pady=15, relief='groove')
        self.panel.grid(row=row_, column=column_,
                        sticky='nsew', padx=5, pady=5)


def get_font(font_string):
    '''
    Returns the font specified by the font string.

    The first character specifies the font, and the remaining characters specify the size.

    Supported fonts:
    'h' -> 'Helvetica'
    'c' -> 'Courier'

    Examples:
    font_string = 'c12' (Courier 12pt)
    font_string = 'h16' (Helvetica 16pt)

    '''
    font_families = {
        'c': 'Courier',
        'h': 'Helvetica'
    }

    return font.Font(family=font_families[font_string[0]], size=int(font_string[1:]))
