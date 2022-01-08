import PySimpleGUI as sg
import os
from maps import Map, active_map
from items import Item, Pocket
from surfaces import Surface, Decoration
from settings import Settings

class Game:
    def __init__(self, title, settingsfile, theme="Dark"):
        self.title = title
        self.settings = Settings(settingsfile)
        self.surfaces = [
            Surface(self.settings.surfacefile(i))
            for i in os.listdir(self.settings.surfacespath)
        ]
        self.maps = [Map(self.settings.mapfile(i), self.settings) for i in os.listdir(self.settings.mapspath)]
        self.items = [
            Item(self.settings.itemfile(i))
            for i in os.listdir(self.settings.itemspath)
        ]
        self.pocket = Pocket([])

        self.active_map = self.map("Home")

        sg.theme("dark")

    def map(self, t, newpos=None):
        new_map = self.maps[self.maps.index(t)]
        if newpos != None:
            new_map.pos = newpos
        return new_map

    def surface(self, t):
        if t in self.surfaces:
            return self.surfaces[self.surfaces.index(t)]
        return Decoration

    def item(self, t):
        return self.items[self.items.index(t)]

    def update_pocket(self):
        print(len(self.pocket.itemlist))
        self.window["pocket_frame"].layout(self.pocket.render())
        self.window["pocket_frame"].update(f"Pocket has {len(self.pocket.itemlist)} items")

    def run(self):

        self.layout = [
            [sg.Text(self.title, expand_x=True, justification="center", font="FiraCode\ Nerd\ Fonts 15")],
            [
                sg.Frame(key="pocket_frame", title="Pocket", layout=self.pocket.render(), expand_y=True, size=(200, 200), element_justification="center"),
                sg.Text(self.active_map.render(self.settings), background_color="#282828", font=("FiraCode Nerd Font", 11), size=self.settings.viewport, justification="center", relief="groove", border_width=8, key="terminal"),
            ]
        ]

        self.window = sg.Window(
                'Turing Hunt',
                self.layout,
                use_default_focus=False,
                finalize = True
        )
        # player controls
        self.window.bind("<KeyPress-w>", "up")
        self.window.bind("<KeyPress-a>", "left")
        self.window.bind("<KeyPress-s>", "down")
        self.window.bind("<KeyPress-d>", "right")

        self.window.bind("<KeyPress-W>", "up")
        self.window.bind("<KeyPress-A>", "left")
        self.window.bind("<KeyPress-S>", "down")
        self.window.bind("<KeyPress-D>", "right")

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event in ["up", "down", "left", "right"]:
                self.active_map = self.active_map.move(event, self)
                self.window["terminal"].update(self.active_map.render(self.settings))
            elif "-ITEM-" in event:
                self.items(event[6:]).render(game)
            else:
                pass
            self.update_pocket()
        self.window.close()

Game("Turing Hunt 2022", "assets/settings.json").run()
