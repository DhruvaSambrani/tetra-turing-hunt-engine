import PySimpleGUI as sg
import datetime as dt

class Clock():
    def __init__(self, start_time = dt.datetime(2022, 10, 7)):
        self.time = start_time

    def render(self):
        return [sg.Frame(key="clock", title="Clock", layout= [[sg.Text(self.time.strftime("%H:%M, %A"), key = "time")]], size=(20, 50), element_justification="center", expand_x=True)]
    
    def update(self, val = 1):
        self.time += dt.timedelta(minutes = val)
        return self.time.strftime("%H:%M, %A")

class GPS():
    def __init__(self, start_loc, start_pos):
        self.loc = start_loc
        self.pos = start_pos

    def render(self):
        return [sg.Frame(key="gps", title="GPS", layout= [[sg.Text(f"Location: {self.loc}\n\n Position: {self.pos}", key = "loc")]], size=(20, 85), element_justification="center", expand_x=True)]
    
    def update(self, loc, pos):
        self.loc = loc
        self.pos = pos

        return f"Location: {self.loc}\n\n Position: {self.pos}"

class Energy():
    def __init__(self, start_energy=100):
        self.time = start_energy

    def render(self):
        return [sg.Frame(key="clock", title="Clock", layout= [[sg.Text(self.time.strftime("%H:%M, %A"), key = "time")]], size=(20, 50), element_justification="center", expand_x=True)]
    
    def update(self, val = 1):
        self.time += dt.timedelta(minutes = val)
        return self.time.strftime("%H:%M, %A")
