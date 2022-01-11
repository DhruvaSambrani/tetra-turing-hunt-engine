import PySimpleGUI as sg
import os
from time import time
from maps import Map
from items import Item, Pocket
from surfaces import Surface, Decoration
from settings import Settings
from gadgets import Clock, GPS, EnergyMeter

class Game:
    def __init__(self, title, settingsfile, gadget_classes, theme="Dark"):
        self.title = title
        self.settings = Settings(settingsfile)
        self.surfaces = [
            Surface(self.settings.surfacefile(i))
            for i in os.listdir(self.settings.surfacespath)
        ]
        self.maps = [Map(self.settings.mapfile(i), self.settings) for i in os.listdir(self.settings.mapspath)]
        self.items = [
            Item(self.settings.itemfile(i))
            for i in os.listdir(self.settings.itemspath) if ".item" in i
        ]

        self.active_map = self.map("Home")
        self.pocket = Pocket([])
        self.gadgets = [G(self) for G in gadget_classes]

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

    def update_gadgets(self):
        [g.update(self) for g in self.gadgets]

    def run(self):

        self.layout = [
            [sg.Text(self.title, expand_x=True, justification="center", font="FiraCode\ Nerd\ Fonts 15")],
            [
                sg.Button(
                    "Pocket",
                    key="OPEN-POCKET", 
                    expand_y=True, 
                ),
                sg.Text(
                    key="terminal",
                    text=self.active_map.render(self.settings), 
                    background_color="#282828", 
                    font=("Source Code Pro", 11), 
                    size=self.settings.viewport,  
                    relief="groove", 
                    border_width=8,
                    justification="center"),
                sg.Frame(
                    key="gadget_frame", 
                    title="Gadgets", 
                    layout=[g.render() for g in self.gadgets], 
                    expand_y=True, 
                    size=(200, 200), 
                    element_justification="center"),
            ],
            [sg.ProgressBar(100, orientation='h', size=(30, 20), bar_color = ("#939393", "#4D4D4D"), key='progressbar', pad = (305, 5))]
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
            event, values = self.window.read(timeout = 1000)

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event in ["up", "down", "left", "right"]:
                self.active_map = self.active_map.move(event, self)
                self.window["terminal"].update(self.active_map.render(self.settings))
            elif event == "OPEN-POCKET":
                self.pocket.render(self)
            else:
                pass
            
            self.update_gadgets()

        self.window.close()

Game("Turing Hunt 2022", "assets/settings.json", [Clock, GPS, EnergyMeter]).run()
