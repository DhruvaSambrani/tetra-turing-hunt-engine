import PySimpleGUI as sg

class HelpDialog():
    def __init__(self, settings):
        self.text = settings.help

    def render(self):
        win = sg.Window(
            title="Help",
            layout = [
                [sg.Frame("Help", 
                layout = [[sg.Text(
                    key="help",
                    text=self.text,
                    font = ("FiraCode Nerd Font", 10),
                    expand_x = True,
                    expand_y = True,
                    justification="left")]],
                font = (sg.DEFAULT_FONT[0], "13"),
                expand_x=True, 
                expand_y=True, 
                element_justification="center")],
                [sg.Button("Close")]
            ],
            size = (525, 525),
            element_justification="right",
            modal = True,
            no_titlebar = True,
            keep_on_top = True,
            button_color = ("#ffffff", "#4D4D4D"),
            margins = (5, 5),
            relative_location=(-97, 33),
            finalize = True,
        )

        win.bind("<Escape>", "Close")
        while True:
            event, values = win.read()
            if event == sg.WIN_CLOSED or event == 'Exit' or event == "Close":
                break
        win.close()

