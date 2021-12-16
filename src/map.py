class Map:
    def __init__(self, filepath):
        self.raw = open(filepath).read()
    
    def get_block(self, rows, columns, startrow, startcolumn):
        return "\n".join([
            i[startcolumn:startcolumn+columns]
            for i in self.raw.split("\n")[startrow : startrow+rows]
        ])


