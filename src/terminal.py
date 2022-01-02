import PySimpleGUI as sg
import os
from map import Map
from items import Item, Pocket

class Game:
    def __init__(self, title, mapfolder=".", itemsfolder=".", theme="Dark"):
        self.title = title
        self.maps = [Map(i) for i in os.listdir(mapfolder) if os.path.splitext(i)[1] == '.map']
        self.items = [Item(os.path.join(itemsfolder,i)) for i in os.listdir(itemsfolder) if os.path.splitext(i)[1] == '.item']
        self.pocket = Pocket(self.items)
        sg.theme("dark")
    
    def run(self):
        layout = [
            [sg.Text(self.title, expand_x=True, justification="center", font="Serif 30")],
            [
                sg.Frame(title="Pocket", layout=self.pocket.render(), expand_y=True, size=(200, 200), element_justification="center"),
                sg.Text(open("test", encoding="utf8").read(), background_color="#282828", font="monospace 12", size=(60,30), justification="center", relief="groove", border_width=8),
            ]
        ]

        window = sg.Window('Turing Hunt', layout)

        while True:
            event, values = window.read()
            print(event,values)
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

        window.close()

Game("Turing Hunt 2022", itemsfolder="items").run()
