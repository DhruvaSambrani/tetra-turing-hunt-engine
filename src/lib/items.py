import json
import PySimpleGUI as sg
import hashlib
import helpers

class Item():
    def __init__(self, itempath):
        jsonobj = json.loads(open(itempath, encoding="utf-8").read())
        self.name = jsonobj["name"]
        self.desc = jsonobj["desc"]
        self.media_path = jsonobj.get("media_path", None)
        self.need_input = jsonobj["need_input"]
        self.answerhash = jsonobj.get("answerhash", None)
        self.collectable = jsonobj["collectable"]
        self.code_file = jsonobj.get("code_file", None)

    def make_layout(self, collected):
        layout = [
            [sg.Text(self.name, justification='center', font='Serif 13', expand_x=True)],
            [sg.Text(self.desc, size=(50, None))],
            [],
            [sg.Button("Close", expand_x=True)]
        ]
        if not (self.media_path is None):
            layout[3].append(sg.Button("Play Media", expand_x=True))
        if self.need_input and not collected:
            layout[2].append(sg.Input(key="in", size=(50, None)))
            layout[3].append(sg.Button("Submit", expand_x=True))
        return layout

    def perform_success(self, game, collected):
        if self.collectable and not collected:
            game.pocket.append(self)
        self.on_success_code_run(game)

    def on_success_code_run(self, game):
        # HIGHLY UNSAFE
        if not(self.code_file is None):
            print("Should eval now")
            exec(compile(open(self.code_file, encoding="utf-8").read(), self.code_file, "exec"))



    def render(self, game, collected=False):
        win = sg.Window("Found an item!", layout=self.make_layout(collected), modal=True, keep_on_top=True)
        successful = False
        while True:
            event,v = win.read()
            if event == "Play Media":
                helpers.play_media(self.media_path)
            elif self.need_input and event=="Submit":
                if hashlib.md5(win["in"].get().encode()).hexdigest() == self.answerhash:
                    w = sg.popup_no_buttons("Correct Answer", auto_close = True, auto_close_duration = 2, no_titlebar = True, modal = True, background_color = "#4D4D4D",  keep_on_top=True)
                    successful = True
                    self.perform_success(game, False)
                    break
                else:
                    sg.popup_no_buttons("Incorrect!", auto_close = True, auto_close_duration = 2, no_titlebar = True, modal = True,  background_color = "#4D4D4D", keep_on_top=True)
            elif event=="Close" and (not self.need_input or collected):
                self.perform_success(game, collected)
                successful = True
                break
            else:
                break
        win.close()
        return successful and self.collectable

    def __eq__(self, t):
        return self.name == t

class Pocket():
    def __init__(self, itemlist=None):
        self.itemlist = itemlist if itemlist is not None else []

    def item(self, t):
        return self.itemlist[self.itemlist.index(t)]

    def render(self, game):
        if len(self.itemlist) > 0:
            win = sg.Window(
                title="Pocket",
                layout = [
                    [sg.Frame(
                        "Pocket",
                        layout=[[sg.Button(i.name, key=f"-ITEM-{i.name}", enable_events=True)] for i in self.itemlist],
                        expand_x = True, expand_y = True,
                        element_justification = "center"
                    )],
                    [sg.Button("Close")]
                ],
                size = (525, 525),
                element_justification="right",
                modal = True,
                no_titlebar = True,
                keep_on_top = True,
                button_color = ("#ffffff", "#4D4D4D"),
                margins = (10, 10),
                relative_location=(-97, 33)
            )
            while True:
                event, values = win.read()
                if event == sg.WIN_CLOSED or event == 'Exit' or event == "Close":
                    break
                else:
                    self.item(event[6:]).render(game, True)
            win.close()
        else:
            sg.popup_no_buttons("No items in Pocket. Broke, much like IISER.", auto_close = True, auto_close_duration = 4, no_titlebar = True, modal = True)

    
    def append(self, item):
        self.itemlist.append(item)

    def drop(self, item):
        self.remove(item)

