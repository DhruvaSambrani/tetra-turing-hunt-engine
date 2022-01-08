import json


class Settings():
    def __init__(self, settingsjson):
        jsonobj = json.loads(open(settingsjson).read())
        self.player = jsonobj["player"]
        self.viewport = jsonobj["viewport"]
        self.itemspath = jsonobj["itemspath"]
        self.mapspath = jsonobj["mapspath"]
        self.surfacespath = jsonobj["surfacespath"]
    def itemfile(self, it):
        return self.itemspath + "/" + it
    def mapfile(self, it):
        return self.mapspath + "/" + it
    def surfacefile(self, it):
        return self.surfacespath + "/" + it


