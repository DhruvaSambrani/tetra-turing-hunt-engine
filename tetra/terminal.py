import PySimpleGUI as sg
import os
from .maps import Map
from .items import Item, Pocket
from .surfaces import Surface, Decoration
from .settings import Settings
from .help import HelpDialog

class Game:
    def __init__(self, title, settingsfile, gadgets_list, first_map=None, theme="Dark"):
        self.title = title
        self.settings = Settings(settingsfile)
        self.surfaces = [
            Surface(self.settings.surfacefile(i))
            for i in os.listdir(self.settings.surfacespath)
        ]
        self.items = [
            Item(self.settings.itemfile(i))
            for i in os.listdir(self.settings.itemspath) if ".item" in i
        ]
        print(f"Read {len(self.items)} items")
        self.maps = [Map(self.settings.mapfile(i), self.settings, self) for i in os.listdir(self.settings.mapspath)]
        print(f"Read {len(self.maps)} maps")
        self.active_map = self.map(first_map) if first_map else None
        self.pocket = Pocket()
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

    def update_gadgets(self, event):
        [g.update(self, event) for g in self.gadgets]


    def make_layout(self):
        glayout = [[]]
        glayout.extend(g.render() for g in self.gadgets)
        self.layout = [
            [
                sg.Frame(
                    key="main_game",
                    title="",
                    layout=[
                    [sg.Text(
                    key="terminal",
                    text=self.active_map.render(self.settings), 
                    background_color="#282828", 
                    font=("FiraCode Nerd Font", 11), 
                    size=self.settings.viewport,  
                    relief="groove", 
                    border_width=8,
                    justification="center")],
                    [sg.ProgressBar(100, orientation='h', size=(30, 20), bar_color = ("#939393", "#4D4D4D"), key='progressbar', pad = (90, 5), expand_x = True)]
                    ],
                    border_width=0
                ),
                sg.Frame(
                    key="utils",
                    layout = [[
                    sg.Button("Pocket", key="OPEN-POCKET", button_color = ("#ffffff", "#4D4D4D"), expand_x=True)],
                    [sg.Frame(
                        key="gadget_frame", 
                        title="Gadgets", 
                        layout=glayout, 
                        expand_y=True, 
                        size=(400, 400), 
                        element_justification="center"),
                    ],
                    [sg.Button("Help", key="OPEN-HELP", button_color = ("#ffffff", "#4D4D4D"), expand_x = True)]
                    ],
                    title="",
                    expand_y=True,
                    element_justification="center",
                    border_width=0),
            ]  
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
            self.active_map.move(event, self)
            self.window["terminal"].update(self.active_map.render(self.settings))
        elif event == "OPEN-POCKET":
            self.pocket.render(self)
        elif event == "OPEN-HELP":
            self.help.render(self)
            pass
        else:
            pass
        return True

    def run(self):
        self.make_layout()
        self.window = sg.Window(
                self.title,
                self.layout,
                use_default_focus=False,
                finalize = True,
                grab_anywhere = True
        )
        self.bind_sg_events()
        st = True

        while st:
            event, _ = self.window.read(timeout = 1000)
            st = self.handle_event(event)
            self.update_gadgets(event)

        self.window.close()

