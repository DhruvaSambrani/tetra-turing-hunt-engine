from tetra import gadgets
from tetra import terminal

g = terminal.Game("Turing Hunt 2022", "assets/settings.json", [gadgets.Clock, gadgets.GPS, gadgets.EnergyMeter])
g.run()

