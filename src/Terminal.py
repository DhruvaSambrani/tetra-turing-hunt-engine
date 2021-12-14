from textual.app import App
from textual.widgets import ScrollView
import numpy as np

def get_block(text, rows, columns, startrow, startcolumn):
    return "\n".join([
        i[startcolumn:startcolumn+columns]
        for i in text.split("\n")[startrow : startrow+rows]
    ])

class SimpleApp(App):
    async def on_mount(self) -> None:
        self.map = open("test").read()
        self.position = np.array([0,0])
        self.size = np.array([10, 20])
        self.body = ScrollView(get_block(self.map, *self.size, *self.position))
        await self.view.dock(self.body)

    async def on_load(self):
        await self.bind("q", "quit")
        await self.bind("w", "move([-1, 0])")
        await self.bind("a", "move([0, -1])")
        await self.bind("s", "move([1, 0])")
        await self.bind("d", "move([0, 1])")
    
    async def action_move(self, direction):
        self.position += np.array(direction)
        await self.body.update(get_block(self.map, *self.size, *self.position))

SimpleApp.run(title="Test Map", log="textual.log")

