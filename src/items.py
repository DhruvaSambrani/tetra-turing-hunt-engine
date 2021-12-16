import json

from rich.markdown import Markdown
from rich.columns import Columns
from rich.panel import Panel
from rich.layout import Layout

from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import ScrollView

class Item(Widget):
    mouse_over = Reactive(False)
    def __init__(self, itempath):
        jsonobj = json.loads(open(itempath).read())
        super().__init__(jsonobj["name"])
        self.prompt = Markdown(jsonobj["promptmd"])
        self.answerhash = jsonobj["answerhash"]
        self.collectable = jsonobj["collectable"]

    def render(self):
        return Panel(self.name, style=("white on red" if self.mouse_over else "red"), expand=True)

    def on_enter(self):
        self.mouse_over=True
    
    def on_leave(self):
        self.mouse_over=False

class Pocket(Widget):
    itemlist = Reactive([])

     def on_enter(self, event):
        await self.forward_event(event)

    def render(self):
        l = Columns(self.itemlist, title="Pocket")
        return l

    def append(self, item):
        self.itemlist.append(item)

    def drop(self, item):
        self.remove(item)


