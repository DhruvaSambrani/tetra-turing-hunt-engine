import json


class Settings():
    def __init__(self, settingsjson):
        jsonobj = json.loads(open(settingsjson, encoding="utf-8").read())
        for k, v in jsonobj.items():
            setattr(self, k, v)
        
    def itemfile(self, it):
        return self.itemspath + "/" + it

    def mapfile(self, it):
        return self.mapspath + "/" + it

    def surfacefile(self, it):
        return self.surfacespath + "/" + it



