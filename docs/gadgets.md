# Gadgets

Gadgets are shown to the left of the screen and update every step of the game. Therefore only fast updating code must be added to a Gadget. They help in adding elements to the game which need to be updated constantly without player interaction.

All gadgets inherit from the `Gadget` class. 

The Gadget class provides the following functions-

- `__init__(self, name)` - initializes the object with the name as `name`. Every inherited class must call `super().__init__("name")`
- `__str__(self)` - to return the simplest text representation of the current state of the gadget.
- `update(self, game, event)` - This is the function that is called in each update cycle. `game` holds the main [`Game`](./game) object, and `event` is the last `sg.Event`
- `render_content(self)` - Returns an `PySimpleGUI` widget that is used by `render(self)`. By default it is a simple `sg.Text` with the `__str__` representation of the gadget.
- `render(self)` - This returns a `sg.Frame` with the title as the `name` of the gadget and the content as the output of `render_content(self)`


The simplest gadget would need to at least do the following-

- Call `super().__init__("gadget_display_name")` in the `__init__` function. The `__init__` function MUST take only a [`Game`](./game) object.
- Overload `__str__(self)`

Though most gadgets are more complex than this, most of them can be implemented by simply overloading `update` and `__str__`. If the output has to also be changed to some other form of `PySimpleGUI` widget, then `render_content` needs to be overloaded. `update` will also need to be overloaded to update the `PySimpleGUI` widget appropriately.

Obviously, inherited classes can have other properties added to them initialized in `__init__` as usual.

## Adding Gadgets to a `Game`

Simply send a list of class names(not objects) to the `gadget_classes` parameter of the `Game()` function.

