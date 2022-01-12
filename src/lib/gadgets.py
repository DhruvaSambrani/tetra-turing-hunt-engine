import PySimpleGUI as sg
import random
import time 

class Gadget():
    def __init__(self, name):
        self.name = name

    def render(self):
        return [
            sg.Frame(
                key=self.name.lower()+"_frame",
                title=self.name,
                layout=[[self.render_content()]],
                element_justification="center",
                expand_x=True
        )]
    
    def render_content(self):
        return sg.Text(
            str(self),
            key = self.name.lower(),
        )


    def __str__(self):
        return f"Unimplemented Gadget - {self.name}"

    def update(self, game, event):
        game.window[self.name.lower()].update(self.__str__())


class Clock(Gadget):
    def __init__(self, game):
        super().__init__("Clock")
        self.init_time = time.time()

    def __str__(self):
        return time.strftime("%H:%M:%S", time.gmtime((time.time()-self.init_time)))


class GPS(Gadget):
    def __init__(self, game):
        super().__init__("GPS")
        self.loc = game.active_map.name
        self.pos = game.active_map.pos
        self.surf = game.surface(game.active_map.fmt[self.pos[0]][self.pos[1]]).name

    def __str__(self):
        return f"Location: {self.loc}\n\nPosition: {self.pos}\n{self.surf}"
    
    def update(self, game, _):
        self.loc = game.active_map.name
        self.pos = game.active_map.pos
        self.surf = game.surface(game.active_map.fmt[self.pos[0]][self.pos[1]]).name
        super().update(game, _)

class EnergyMeter(Gadget):
    def __init__(self, game):
        super().__init__("Energy Meter")
        self.val = self.max_val = 100
    
    def ded_saying(self):
        return random.choice([
            'I\'m way too tired to walk that far.\n I need a coffee... or five.',
            "My legs are dead.",
            "Even Aulak's classes are easier than this Treasure Hunt.",
            "Holy F***. I'd take offline exams instead of this any day!",
            "I'm ded.",
            "And here I thought Phi@I's treasure hunts were the most exhausting.",
            "Should have just opted for online labs man.",
            "Should have just gone to Physictionary.\nIt would have been boring, but atleast it wouldn't be so tiring...",
            "Sir, I think you are muted. Oh wait, I'm not in class.",
            "F... this is longer than Kuljit's class...",
            "Even Shain's talk on functional programming is shorter than this"
        ])

    def render_content(self):
        return sg.ProgressBar(self.val, orientation='h', size=(30, 10), key=self.name.lower(), expand_x = True, pad = 10)
    
    def update(self, game, event):
        if event == "IDLE":
            delta = game.settings.rest_energy
        else:
            delta = -game.settings.walking_energy_cost 

        self.val = min(max(0, self.val + delta), 100)
        if self.val <= 0:
            sg.popup_no_buttons(self.ded_saying(), auto_close = True, auto_close_duration = 2, no_titlebar = True, modal = True)
            self.val = self.max_val / 2
        game.window[self.name.lower()].UpdateBar(self.val)
        
