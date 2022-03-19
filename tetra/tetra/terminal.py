import PySimpleGUI as sg
import os
from .maps import Map
from .items import Item, Pocket
from .surfaces import Surface, Decoration
from .settings import Settings
from .help import HelpDialog

class Game:
    def __init__(self, title, settingsfile, gadgets_list, theme="Dark"):
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
        self.gadgets = [G(self) for G in gadgets_list]
        self.help = HelpDialog(self.settings)
        sg.theme(theme)

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

    def translate_event(self, event):
        d = {
            "up": "MOVE",
            "down": "MOVE",
            "left": "MOVE",
            "right": "MOVE",
        }
        return d.get(event, "IDLE")

    def update_gadgets(self, event):
        ev = self.translate_event(event)
        [g.update(self, ev) for g in self.gadgets]


    def make_layout(self):
        glayout = [[sg.Button("Pocket", key="OPEN-POCKET", button_color = ("#ffffff", "#4D4D4D"), expand_x=True)]]
        glayout.extend(g.render() for g in self.gadgets)
        self.layout = [
            [sg.Text(self.title, expand_x=True, justification="center", font="FiraCode\ Nerd\ Fonts 15")],
            [
                sg.Text(
                    key="terminal",
                    text=self.active_map.render(self.settings), 
                    background_color="#282828", 
                    font=("FiraCode Nerd Font", 11), 
                    size=self.settings.viewport,  
                    relief="groove", 
                    border_width=8,
                    justification="center"),
                sg.Frame(
                    key="gadget_frame", 
                    title="Gadgets", 
                    layout=glayout, 
                    expand_y=True, 
                    size=(200, 200), 
                    element_justification="center"),
            ],
            [sg.ProgressBar(100, orientation='h', size=(30, 20), bar_color = ("#939393", "#4D4D4D"), key='progressbar', pad = (90, 5)),
             sg.Button("Help", key="OPEN-HELP", button_color = ("#ffffff", "#4D4D4D"), expand_x=True, pad=((13, 4),(3, 0)))]
        ]
    def bind_sg_events(self):
        self.window.bind("<KeyPress-w>", "up")
        self.window.bind("<KeyPress-a>", "left")
        self.window.bind("<KeyPress-s>", "down")
        self.window.bind("<KeyPress-d>", "right")
        self.window.bind("<KeyPress-p>", "OPEN-POCKET")
        self.window.bind("<KeyPress-h>", "OPEN-HELP")

        self.window.bind("<KeyPress-W>", "up")
        self.window.bind("<KeyPress-A>", "left")
        self.window.bind("<KeyPress-S>", "down")
        self.window.bind("<KeyPress-D>", "right")
        self.window.bind("<KeyPress-P>", "OPEN-POCKET")
        self.window.bind("<KeyPress-H>", "OPEN-HELP")
        
    def handle_event(self, event):
        if event == sg.WIN_CLOSED or event == 'Exit':
            return False
        elif event in ["up", "down", "left", "right"]:
            self.active_map = self.active_map.move(event, self)
            self.window["terminal"].update(self.active_map.render(self.settings))
        elif event == "OPEN-POCKET":
            self.pocket.render(self)
        elif event == "OPEN-HELP":
            self.help.render()
            pass
        else:
            pass
        return True

    def run(self):
        self.make_layout()
        self.window = sg.Window(
                'Turing Hunt',
                self.layout,
                use_default_focus=False,
                finalize = True,
                grab_anywhere = False
        )
        self.bind_sg_events()
        st = True
        while st:
            event, _ = self.window.read(timeout = 1000)
            st = self.handle_event(event)
            self.update_gadgets(event)

        self.window.close()

