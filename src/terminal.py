import PySimpleGUI as sg
import os
from maps import Map, active_map
from items import Item, Pocket
from surfaces import Surface

class Game:
    def __init__(self, title, mapfolder="./maps/", surffolder = "./surfaces/", itemsfolder="./items/", theme="Dark"):
        self.title = title
        self.surfaces = [Surface(os.path.join(surffolder, i)) for i in os.listdir(surffolder) if os.path.splitext(i)[1] == '.surface']
        self.walkables = [elt.character for elt in self.surfaces if elt.walkable]

        self.maps = [Map(os.path.join(mapfolder, i)) for i in os.listdir(mapfolder) if os.path.splitext(i)[1] == '.map']
        self.items = [Item(os.path.join(itemsfolder,i)) for i in os.listdir(itemsfolder) if os.path.splitext(i)[1] == '.item']
        self.pocket = Pocket(self.items)
        self.viewsize = (61, 29)

        global active_map 
        active_map = self.maps[0]

        sg.theme("dark")

    def run(self):
        layout = [
            [sg.Text(self.title, expand_x=True, justification="center", font="Source\ Code\ Pro 15")],
            [
                sg.Frame(title="Pocket", layout=self.pocket.render(), expand_y=True, size=(200, 200), element_justification="center"),
                sg.Text(active_map.render(self.viewsize[1], self.viewsize[0]), background_color="#282828", font=("Source Code Pro", 12), size=self.viewsize, justification="center", relief="groove", border_width=8, key="terminal"),
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
                window["terminal"].update(active_map.move(event, self.viewsize, self.walkables))

        window.close()

Game("Turing Hunt 2022", itemsfolder="items").run()
