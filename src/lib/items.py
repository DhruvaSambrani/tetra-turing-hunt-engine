import json
import PySimpleGUI as sg
import hashlib

class Item():
    def __init__(self, itempath):
        jsonobj = json.loads(open(itempath).read())
        self.name = jsonobj["name"]
        self.prompt = jsonobj["promptmd"]
        self.answerhash = jsonobj["answerhash"]
        self.collectable = jsonobj["collectable"]

    def render(self, game):
        win = sg.Window("Popup", layout=[
            [sg.Text(self.name, justification='center', font='Serif 13', expand_x=True)],
            [sg.Text(self.prompt)],
            [sg.Input(key="in")],
            [sg.Button("Submit", expand_x=True), sg.Button("Close", expand_x=True)]
        ], modal=True)
        successful = False
        while True:
            event,v = win.read()
            if event=="Submit":
                if hashlib.md5(win["in"].get().encode()).hexdigest() == self.answerhash:
                    w = sg.Popup("Correct Answer")
                    successful = True
                    if self.collectable:
                        game.pocket.append(self)
                    break
                else:
                    sg.Popup("Incorrect!")
            else:
                break
        win.close()
        return successful

    def __eq__(self, t):
        return self.name == t

class Pocket():
    def __init__(self, itemlist=None):
        self.itemlist = itemlist if itemlist is not None else []

    def render(self):
        return [[sg.Button(i.name, key=f"-ITEM-{i.name}", enable_events=True)] for i in self.itemlist]
    
    def append(self, item):
        self.itemlist.append(item)

    def drop(self, item):
        self.remove(item)


