import json
import os
import numpy as np
import PySimpleGUI as sg
from items import Item
from time import sleep

def load(game, secs):
    counter = 0

    while(True):
        game.window["progressbar"].UpdateBar(counter + 4)
        sleep(secs/100)
        counter += 2

        if(counter == 102):
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
    def __init__(self, filepath, settings, pos = None):
        with open(filepath, encoding = 'utf-8') as fh:
            jsonobj = json.load(fh, strict=False)
        self.name = jsonobj["name"]
        self.fmt = np.stack([list(elt) for elt in jsonobj["raw"].splitlines()]) #formatted map as np grid
        self.r, self.c = self.fmt.shape #map size
        self.pos = np.array(jsonobj["init_pos"]) if (pos is None) else pos #player pos
        self.items = {tuple(jsonobj["items"][it_name]): it_name for it_name in jsonobj["items"].keys()}
        self.exits = jsonobj["exits"] #dict of exit coords and new map
        self.exit_coords = [[int(x) for x in elt.split(",")] for elt in jsonobj["exits"].keys()] #list of exit points

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
    
    def activate_item_here(self, game):
        i =  self.items.get(tuple(self.pos), None)
        if not (i is None):
            success = game.item(i).render(game)
            if success:
                self.items.pop(tuple(self.pos))

    def iswalkable(self, new_pos, game):
        return game.surface(self.fmt[new_pos[0]][new_pos[1]]).walkable

    def move(self, code, game):
        dir = {
            "up": [-1, 0],
            "down": [1, 0],
            "left": [0, -1],
            "right": [0, 1]
            }
        new_pos = clamp(self.pos + np.array(dir[code]), self.r, self.c)
        
        if self.iswalkable(new_pos, game):
            if game.energy.val > 1:
                self.pos = new_pos
                self.activate_item_here(game)
                game.energy.update(game.settings.walking_energy_cost)

                if any(elt == list(new_pos) for elt in self.exit_coords):

                    if game.energy.val > 15:
                        new_pos_key = ",".join(np.char.mod('%i', new_pos))
                        transitionAnim(game, 0.0001)
                        game.clock.update(game.settings.transition_time)
                        game.energy.update(game.settings.transition_energy_cost)

                        return game.map(self.exits[new_pos_key][0], self.exits[new_pos_key][1])
                    else:
                        sg.popup_no_buttons('I\'m way too tired to walk that far.\n I need a coffee... or five.', auto_close = True, auto_close_duration = 3, no_titlebar = True, modal = True)
            else:
                sg.popup_no_buttons('My legs are dead.', auto_close = True, auto_close_duration = 3, no_titlebar = True, modal = True)

        return self
