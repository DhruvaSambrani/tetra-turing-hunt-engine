import PySimpleGUI as sg
import os
import maps
from items import Item, Pocket

class Game:
    def __init__(self, title, mapfolder=".", itemsfolder=".", theme="Dark"):
        self.title = title
        self.surfaces = [Surface(i) for i in os.listdir(mapfolder) if os.path.splitext(i)[1] == '.map']
        self.maps = [Map(i) for i in os.listdir(mapfolder) if os.path.splitext(i)[1] == '.map']
        self.items = [Item(os.path.join(itemsfolder,i)) for i in os.listdir(itemsfolder) if os.path.splitext(i)[1] == '.item']
        self.pocket = Pocket(self.items)
        sg.theme("dark")
    
    def run(self):
        layout = [
            [sg.Text(self.title, expand_x=True, justification="center", font="fira\ code 30")],
            [
                sg.Frame(title="Pocket", layout=self.pocket.render(), expand_y=True, size=(200, 200), element_justification="center"),
                sg.Text(open("test", encoding="utf8").read(), background_color="#282828", font="fira\ code 16", size=(60,30), justification="center", relief="groove", border_width=8),
            ]
        ]

        window = sg.Window(
                'Turing Hunt', 
                layout, 
                return_keyboard_events=True,
                use_default_focus=False,
        )
        sg.set_options(scaling=2)

        while True:
            event, values = window.read()
            movement = maps.movement(event)
            print(event, values)
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if movement:
                maps.currentmap.move(movement)

        window.close()

Game("Turing Hunt 2022", itemsfolder="items").run()
