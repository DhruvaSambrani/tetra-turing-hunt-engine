# Game

```python
class Game
    title #:: Title of the window
    active_map #:: the current map
    gadgets #:: list of gadgets
    map(name_of_map, newpos=None) #:: Set the active_map to `name_of_map`. If `newpos` is set, then player spawns there, else the default position.
    surface(char_of_surface) #:: returns the surface with character `char_of_surface`
    item(item_name) #:: returns the item with name `item_name`
```

## Initializing a `Game` object

```py
game = Game("Name of the game", "path_to_settings", [list, of, Gadget, Classes])
```

## Running a `Game` object

```py
game.run()
```

# The Game loop

1. Create the layout by `Game.make_layout`
2. Place layout into a window
3. Bind `sg` events to human readable events with `Game.bind_sg_events()`
4. Loop until `st`
  1. Wait for a `sg` event.
  2. `game.handle_event(event)` and return new value of `st`
  3. `game.update_gadgets(event)`

You can overload any function in an inherited class, but this would generally not be necessary.
