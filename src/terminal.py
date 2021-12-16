from map import Map
from textual.app import App
from textual.widgets import ScrollView
import numpy as np

class SimpleApp(App):
    async def on_mount(self) -> None:
        self.map = Map("test")
        self.position = np.array([0,0])
        self.size = np.array([25, 50])
        self.body = ScrollView(self.map.get_block(*self.size, *self.position))
        await self.view.dock(self.body)

    async def on_load(self):
        await self.bind("q", "quit")
        await self.bind("w", "move([-1, 0])")
        await self.bind("a", "move([0, -1])")
        await self.bind("s", "move([1, 0])")
        await self.bind("d", "move([0, 1])")
    
    async def action_move(self, direction):
        self.position += np.array(direction)
        await self.body.update(self.map.get_block(*self.size, *self.position))

SimpleApp.run(title="Test Map")

