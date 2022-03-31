import json
import numpy as np
from time import sleep

def load(game, secs):
    counter = 0

    while(True):
        game.window["progressbar"].UpdateBar(counter + 4)
        sleep(secs/100)
        counter += 3.5

        if(counter > 100):
            break

def transitionAnim(game, secs):
        load(game, secs)
        game.window["progressbar"].update(bar_color = ("#4D4D4D", "#939393"))
        load(game, secs)
        game.window["progressbar"].UpdateBar(0)
        game.window["progressbar"].update(bar_color = ("#939393", "#4D4D4D"))

def clamp(p, r, c):
    return [min(max(0, p[0]), r-1), min(max(0, p[1]), c-1)]

class Map:
    def __init__(self, filepath, settings, game, pos = None):
        print(f"initing {filepath}")
        with open(filepath, encoding = 'utf-8') as fh:
            jsonobj = json.load(fh, strict=False)
        self.name = jsonobj["name"]
        self.fmt_ref = np.stack([list(elt) for elt in jsonobj["raw"].splitlines()]) #formatted map as np grid
        self.r, self.c = self.fmt_ref.shape #map size
        self.init_pos = np.array(jsonobj["init_pos"])
        self.pos = np.array(jsonobj["init_pos"]) if (pos is None) else pos #player pos
        self.items_ref = {tuple(jsonobj["items"][it_name]): it_name for it_name in jsonobj["items"].keys()}
        self.exits = jsonobj["exits"] #dict of exit coords and new map
        self.exit_coords = [[int(x) for x in elt.split(",")] for elt in jsonobj["exits"].keys()] #list of exit points

        self.fmt = np.stack([list(elt) for elt in jsonobj["raw"].splitlines()])
        self.items = {}

        items_on_startup = jsonobj.get("items_on_startup", self.items_ref.values())
        for item_name in items_on_startup:
            self.place_item(item_name, game)

    def __eq__(self, t):
        return t == self.name

    def render(self, settings):
        vc, vr = settings.viewport
        sr, sc = self.pos
        sr, sc = (sr - vr//2), (sc - vc//2)
        mini = self.fmt[
                        max(0, sr) : min(self.r, vr + sr),
                        max(0, sc) : min(self.c, vc + sc)
                        ] 
        mini_r, mini_c = mini.shape
        r_rel, c_rel = -min(0, sr), -min(0, sc)
        block = np.stack([[" " for c in range(vc)] for r in range(vr)])
        block[r_rel : (r_rel + mini_r), c_rel : (c_rel + mini_c)] = mini
        block[vr//2, vc//2] = settings.player
        return "\n".join(["".join(elt) for elt in block.tolist()])

    def place_item(self, item_name, game):
        if not (item_name in self.items.values()):
            coord = list(self.items_ref.keys())[list(self.items_ref.values()).index(item_name)]
            if(game.item(item_name).char != None): self.fmt[coord] = game.item(item_name).char
            self.items[tuple(coord)] = self.items_ref[tuple(coord)]

    def remove_item(self, item_name, game):
        if(item_name in self.items.values()):
            coord = list(self.items_ref.keys())[list(self.items_ref.values()).index(item_name)]
            self.fmt[coord] = self.fmt_ref[coord]
            self.items.pop(tuple(coord))

    def activate_item_here(self, game):
        nowpos = [self.pos[0], self.pos[1]]
        i = self.items.get(tuple(nowpos), None)
        if not (i is None):
            to_remove = game.item(i).render(game)
            if to_remove:
                self.remove_item(i, game)
            return True
        return False

    def iswalkable(self, new_pos, game):
        return game.surface(self.fmt_ref[new_pos[0]][new_pos[1]]).walkable

    def move(self, code, game):
        dir = {
            "up": [-1, 0],
            "down": [1, 0],
            "left": [0, -1],
            "right": [0, 1]
        }
        new_pos = clamp(self.pos + np.array(dir[code]), self.r, self.c)
        
        if self.iswalkable(new_pos, game):
            self.pos = new_pos
            item_here = self.activate_item_here(game)

            if not item_here and any(elt == list(new_pos) for elt in self.exit_coords):
                new_pos_key = ",".join(np.char.mod('%i', new_pos))
                transitionAnim(game, 0.0001)
                game.active_map = game.map(self.exits[new_pos_key][0], self.exits[new_pos_key][1])
