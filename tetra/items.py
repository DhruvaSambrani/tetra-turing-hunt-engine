import json
import PySimpleGUI as sg
import hashlib
from . import helpers
import textwrap

class DocumentWrapper(textwrap.TextWrapper):

    def wrap(self, text):
        split_text = text.split('\n')
        lines = [line for para in split_text for line in textwrap.TextWrapper.wrap(self, para)]
        return lines

class Item():
    def __init__(self, itempath):
        print(f"Initing {itempath}")
        jsonobj = json.loads(open(itempath, encoding="utf-8").read())
        print(f"""    name: {jsonobj["name"]}""")
        self.name = jsonobj["name"]
        self.desc = jsonobj["desc"]
        self.char = jsonobj.get("char", "?")
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
            layout[3].append(sg.Button("Submit", expand_x=True, bind_return_key=True))
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
        win = sg.Window("Found an item!", layout=self.make_layout(collected), modal=True, keep_on_top=True, finalize=True)
        win.bind("<Escape>", "Close")
        successful = False
        while True:
            event,v = win.read()
            if event == "Play Media":
                helpers.play_media(self.media_path)
            elif self.need_input and event=="Submit":
                if hashlib.md5(win["in"].get().lower().encode()).hexdigest() == self.answerhash:
                    win["in"].update(background_color="#004f00")
                    sg.popup_no_buttons("Correct!", auto_close = True, auto_close_duration = 1, no_titlebar = True, modal = True,  background_color = "#4D4D4D")
                    win["in"].update(value = "", background_color="#4d4d4d")

                    successful = True
                    self.perform_success(game, False)
                    break
                else:
                    win["in"].update(value = "", background_color="#6b0618")
                    sg.popup_no_buttons("Incorrect!", auto_close = True, auto_close_duration = 1, no_titlebar = True, modal = True,  background_color = "#4D4D4D")
                    win["in"].update(value = "", background_color="#4d4d4d")

            elif (event=="Close" or event is None) and (not self.need_input or collected):
                self.perform_success(game, collected)
                successful = True
                break
            else:
                print(f"Unhandled Event: {event}!")
                break
        win.close()
        return successful and self.collectable

    def __eq__(self, t):
        return self.name == t

class Pocket():
    def __init__(self, itemlist=None):
        self.itemlist = itemlist if itemlist is not None else []
        self.active_item = None

    def item(self, t):
        return self.itemlist[self.itemlist.index(t)]

    def render(self, game):
        if len(self.itemlist) > 0:
            word_ln = 75
            win = sg.Window(
                title="Pocket",
                layout = [
                    [sg.Frame(
                        "Pocket",
                        layout=[[
                            sg.Frame("Items",
                            layout = [[sg.Column(layout = [[sg.Button(i.name, key=f"-ITEM-{i.name}", enable_events=True, use_ttk_buttons=True, expand_x=True, button_color = ("#ffffff", "#4D4D4D"))] for i in self.itemlist],
                            expand_y = True, scrollable = True, vertical_scroll_only=True, expand_x = True)]],
                            expand_x=True, expand_y=True),
                            sg.Frame("Description", 
                            layout = [
                                [sg.Column(key="desc_def", expand_x = True, expand_y = True, layout = [[sg.Text("No item currently selected.", size = (word_ln, None))]])] +
                                [sg.Column(key="desc_no_media", expand_x = True, expand_y = True, layout = [[sg.Text("This item has no media files.", size = (word_ln, None))]], visible = False)] +
                                [sg.Column(key="desc_no_use", expand_x = True, expand_y = True, layout = [[sg.Text("This item cannot be used right now.", size = (word_ln, None))]], visible = False)] +
                                [sg.Column(key=f"desc_{i.name}", expand_x = True, expand_y = True, layout = [[sg.Text(i.name + "\n\n" + DocumentWrapper(width=word_ln).fill(i.desc), size = (word_ln, None))]], visible = False) for i in self.itemlist], 
                                [sg.Button("Play Media", expand_x=True, use_ttk_buttons=True, button_color = ("#ffffff", "#4D4D4D")), sg.Button("Use Item", expand_x=True, use_ttk_buttons=True, button_color = ("#ffffff", "#4D4D4D"))]
                            ], expand_x = True, expand_y = True, size = (250, None))
                            ]],
                        expand_x = True, expand_y = True,
                        element_justification = "center"
                    )],
                    [sg.Button("Close")]
                ],
                size = (game.window["terminal"].get_size()[0] - 35, game.window["terminal"].get_size()[1] - 30),
                element_justification="right",
                modal = True,
                no_titlebar = True,
                keep_on_top = True,
                button_color = ("#ffffff", "#4D4D4D"),
                margins = (10, 10),
                location=(
                game.window.current_location()[0] + (game.window.size[0] - game.window["terminal"].get_size()[0] - game.window["gadget_frame"].get_size()[0] - 14),
                game.window.current_location()[1] + 57),
                finalize = True
            )
            win.bind("<Escape>", "Close")
            
            while True:
                event, values = win.read()
                if event == sg.WIN_CLOSED or event == 'Exit' or event == "Close":
                    break

                if event == "Play Media":
                    if(self.active_item != None):
                        md_path = self.active_item.media_path

                        if(md_path != None):
                            helpers.play_media(md_path)
                        else:
                            self.show_desc(win, "no_media")
                    else: 
                        self.show_desc(win, "no_media")

                if event == "Use Item":
                    if(self.active_item != None):

                        if(self.active_item.code_file != None):
                            self.active_item.on_success_code_run(game)
                            break
                        else:
                            self.show_desc(win, "no_use")
                    else: 
                        self.show_desc(win, "no_use")
                    
                elif(event[6:] in self.itemlist):
                    self.active_item = self.item(event[6:])
                    self.show_desc(win, self.active_item.name)

                    # self.item(event[6:]).render(game, True)
                    
            self.active_item = None
            win.close()
        else:
            sg.popup_no_buttons("No items in Pocket. Broke, much like IISER.", auto_close = True, auto_close_duration = 4, no_titlebar = True, modal = True)


    def show_desc(self, win, name):
        win["desc_def"].update(visible = False)
        win["desc_no_media"].update(visible = False)
        win["desc_no_use"].update(visible = False)
        [win[f"desc_{i.name}"].update(visible = False) for i in self.itemlist]
        win[f"desc_{name}"].update(visible = True)

    def append(self, item):
        self.itemlist.append(item)

    def drop(self, item):
        self.itemlist.remove(item)
