from map import Map
from items import *
from textual.app import App
from textual.widgets import * 
from textual.views import WindowView
import numpy as np

class SimpleApp(App):
    async def on_mount(self) -> None:
        self.map = Map("test")
        self.position = np.array([0,0])
        self.size = np.array([25, 50])
        self.body = ScrollView(self.map.get_block(*self.size, *self.position))
        self.pocket = Pocket()
        self.pocket.append(Item("testitem.json"))
        self.pocket.append(Item("testitem.json"))
        self.pocket.append(Item("testitem.json"))
        self.pocket.append(Item("testitem.json"))
        self.pocket.append(Item("testitem.json"))
        self.pocket.append(Item("testitem.json"))
        self.pocket.append(Item("testitem.json"))
        self.pocket.append(Item("testitem.json"))
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.pocket, edge="left", size=30, name='pocket')
        await self.view.dock(self.body, edge="right")

    async def on_load(self):
        await self.bind("q", "quit", "Quit")
        await self.bind("w", "move([-1, 0])", "Up")
        await self.bind("a", "move([0, -1])", "Left")
        await self.bind("s", "move([1, 0])", "Right")
        await self.bind("d", "move([0, 1])", "Down")
        await self.bind("b", "view.toggle('pocket')", "Toggle Pocket")

    async def action_move(self, direction):
        self.position += np.array(direction)
        await self.body.update(self.map.get_block(*self.size, *self.position))

SimpleApp.run(title="Test Map")

