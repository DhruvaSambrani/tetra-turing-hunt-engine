import json


class Settings():
    def __init__(self, settingsjson):
        jsonobj = json.loads(open(settingsjson, encoding="utf-8").read())
        self.player = jsonobj["player"]
        self.viewport = jsonobj["viewport"]
        self.itemspath = jsonobj["itemspath"]
        self.mapspath = jsonobj["mapspath"]
        self.surfacespath = jsonobj["surfacespath"]
        
        self.transition_time = jsonobj["transition_time"]
        self.rest_energy = jsonobj["rest_energy"]
        self.walking_energy_cost = jsonobj["walking_energy_cost"]
        self.gadget_classes = jsonobj["gadget_classes"]


    def itemfile(self, it):
        return self.itemspath + "/" + it

    def mapfile(self, it):
        return self.mapspath + "/" + it

    def surfacefile(self, it):
        return self.surfacespath + "/" + it



