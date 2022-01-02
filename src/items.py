import json
import PySimpleGUI as sg


class Item():
    def __init__(self, itempath):
        jsonobj = json.loads(open(itempath).read())
        self.name = jsonobj["name"]
        self.prompt = jsonobj["promptmd"]
        self.answerhash = jsonobj["answerhash"]
        self.collectable = jsonobj["collectable"]

    def render(self):
        return [
            [sg.Text(i.name, justification='center', font='Serif 13')],
            [sg.Text(i.prompt)]
        ]

class Pocket():
    def __init__(self, itemlist=None):
        self.itemlist = itemlist if itemlist is not None else []

    def render(self):
        return [[sg.Button(i.name, key=f"-ITEM-{i.name}", enable_events=True)] for i in self.itemlist]
    
    def append(self, item):
        self.itemlist.append(item)

    def drop(self, item):
        self.remove(item)


