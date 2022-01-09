import PySimpleGUI as sg
import os
from time import time
from maps import Map
from items import Item, Pocket
from surfaces import Surface, Decoration
from settings import Settings
from gadgets import Clock, GPS, EnergyMeter

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

        self.active_map = self.map("Home")

        self.pocket = Pocket([])
        self.clock = Clock()
        self.GPS = GPS(self.active_map.name, self.active_map.pos)
        self.energy = EnergyMeter(self.settings.start_energy, self.settings.max_energy)

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
        self.window["pocket_frame"].layout(self.pocket.render())
        self.window["pocket_frame"].update(f"Pocket has {len(self.pocket.itemlist)} items")

    def update_gadgets(self, prev_time):
            #in game clock update
            if (time() - prev_time > self.settings.clock_tick): 
                prev_time = time()
                self.window["time"].update(self.clock.update())

            #update GPS
            self.window["loc"].update(self.GPS.update(self.active_map.name, self.active_map.pos))
            self.window["energy"].UpdateBar(self.energy.val)

            return prev_time

    def run(self):

        self.layout = [
            [sg.Text(self.title, expand_x=True, justification="center", font="FiraCode\ Nerd\ Fonts 15")],
            [
                sg.Frame(
                    key="pocket_frame", 
                    title="Pocket", 
                    layout=self.pocket.render(), 
                    expand_y=True, 
                    size=(200, 200), 
                    element_justification="center"),
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
                    layout=[self.energy.render(), self.clock.render(), self.GPS.render()], 
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

        prev_time = time()

        while True:
            event, values = self.window.read(timeout = 1000)

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event in ["up", "down", "left", "right"]:
                self.active_map = self.active_map.move(event, self)
                self.window["terminal"].update(self.active_map.render(self.settings))
               
            elif "-ITEM-" in event:
                self.items(event[6:]).render(game)
            else:
                self.energy.update(self.settings.idle_energy_gain) #energy replenished
                pass
            
            self.update_pocket()
            prev_time = self.update_gadgets(prev_time)

        self.window.close()

Game("Turing Hunt 2022", "assets/settings.json").run()
