import PySimpleGUI as sg
import os
import maps
from items import Item, Pocket

class Game:
    def __init__(self, title, mapfolder=".", itemsfolder=".", theme="Dark"):
        self.title = title
        # self.surfaces = [Surface(i) for i in os.listdir(mapfolder) if os.path.splitext(i)[1] == '.map']
        self.maps = [maps.Map(i) for i in os.listdir(mapfolder) if os.path.splitext(i)[1] == '.map']
        self.items = [Item(os.path.join(itemsfolder,i)) for i in os.listdir(itemsfolder) if os.path.splitext(i)[1] == '.item']
        self.pocket = Pocket(self.items)
        self.viewsize = (60, 30)
        sg.theme("dark")

        maps.currentmap = self.maps[0]
    
    def run(self):
        layout = [
            [sg.Text(self.title, expand_x=True, justification="center", font="Serif 30")],
            [
                sg.Frame(title="Pocket", layout=self.pocket.render(), expand_y=True, size=(200, 200), element_justification="center"),
                sg.Text(maps.currentmap.render(self.viewsize[1] - 1, self.viewsize[1] + 1), background_color="#282828", font=("Source Code Pro", 12), size=self.viewsize, justification="center", relief="groove", border_width=8, key="terminal"),
            ]
        ]

        window = sg.Window(
                'Turing Hunt', 
                layout, 
                return_keyboard_events=True,
                use_default_focus=False,
                finalize = True
        )

        # player controls
        window.bind("<KeyPress-w>", "up")
        window.bind("<KeyPress-a>", "left")
        window.bind("<KeyPress-s>", "down")
        window.bind("<KeyPress-d>", "right")
        
        window.bind("<KeyPress-W>", "up")
        window.bind("<KeyPress-A>", "left")
        window.bind("<KeyPress-S>", "down")
        window.bind("<KeyPress-D>", "right")

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event in ["up", "down", "left", "right"]:
                window["terminal"].update(maps.currentmap.move(event, self.viewsize))

        window.close()

Game("Turing Hunt 2022", itemsfolder="items").run()
