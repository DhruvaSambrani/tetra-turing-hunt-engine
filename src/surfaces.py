import json

class Surface:
    def __init__(self, surfacepath):
        jsonobj = json.loads(open(surfacepath).read())
        self.name = jsonobj["name"]
        self.character = jsonobj["character"]
        self.walkable = jsonobj.get("walkable", False)


 
