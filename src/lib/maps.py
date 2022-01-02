import json
import os
import numpy as np


active_map = None

class Map:
    def __init__(self, filepath, pos = None):
        with open(filepath, encoding = 'utf-8') as fh:
            jsonobj = json.load(fh, strict=False)

        self.name = jsonobj["name"]
        self.fmt = np.stack([list(elt) for elt in jsonobj["raw"].splitlines()]) #formatted map as np grid
        self.r, self.c = self.fmt.shape #map size
        self.pos = np.array(jsonobj["init_pos"]) if (pos is None) else pos #player pos

        self.exits = jsonobj["exits"] #dict of exit coords and new map
        self.exit_coords = [[int(x) for x in elt.split(",")] for elt in jsonobj["exits"].keys()] #list of exit points


    def render(self, vr, vc):

        sr, sc = self.pos 

        #center the block around player
        sr, sc = (sr - vr//2), (sc - vc//2)
            
        #cutout of map that falls within the block
        mini = self.fmt[
                        max(0, sr) : min(self.r, vr + sr),
                        max(0, sc) : min(self.c, vc + sc)
                        ] 

        mini_r, mini_c = mini.shape

        #find position of the cutout relative to the block
        r_rel, c_rel = -min(0, sr), -min(0, sc)
        
        #place cutout inside the block \u2592
        block = np.stack([[" " for c in range(vc)] for r in range(vr)])

        block[r_rel : (r_rel + mini_r), c_rel : (c_rel + mini_c)] = mini

        block[vr//2, vc//2] = "O" #display player

        return "\n".join(["".join(elt) for elt in block.tolist()])
        
    def move(self, code, viewsize, walkables):
        
        dir = {
            "up": [-1, 0],
            "down": [1, 0],
            "left": [0, -1],
            "right": [0, 1]
            }

        new_pos = self.pos + np.array(dir[code])

        if self.fmt[new_pos[0]][new_pos[1]] in walkables:
            self.pos = new_pos

            # check for map transitions
            if any(elt == list(new_pos) for elt in self.exit_coords):
                new_pos_key = ",".join(np.char.mod('%i', new_pos))
                return Map(os.path.join("../assets/maps", self.exits[new_pos_key][0] + ".map"), self.exits[new_pos_key][1])

        return self.render(viewsize[1], viewsize[0])