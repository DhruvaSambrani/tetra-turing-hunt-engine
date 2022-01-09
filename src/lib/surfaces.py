import json

class Surface:
    def __init__(self, surfacepath):
        if surfacepath!=None:
            jsonobj = json.loads(open(surfacepath, encoding="utf-8").read(), strict = False)
            self.name = jsonobj["name"]
            self.character = jsonobj["character"]
            self.walkable = jsonobj.get("walkable", False)
        else:
            pass
    def __eq__(self, t):
        return t == self.character

Decoration = Surface(None)
Decoration.walkable = False
Decoration.name = "Decor"


