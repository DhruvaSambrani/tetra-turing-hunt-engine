import json

def ismovement(code):
    return {
        "Up:111": "up", 
        "Down:116": "down",
        "Left:113": "left",
        "Right:114": "right",
        "w:25": "up",
        "a:38": "left",
        "s:39": "down",
        "d:40": "right"}.get(code, False)

class Map:
    def __init__(self, filepath):
        jsonobj = json.loads(open(itempath).read())
        self.raw = jsonobj["raw"]
        self.entry_pos = jsonobj["entry_pos"]

    def render(self):
        return get_block(self, )

    def get_block(self, rows, columns, startrow, startcolumn):
        return "\n".join([
            i[startcolumn:startcolumn+columns]
            for i in self.raw.split("\n")[startrow : startrow+rows]
        ])

    def move():
        pass


