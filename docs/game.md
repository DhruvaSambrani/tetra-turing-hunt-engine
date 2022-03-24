# Game

```python
class Game
    title #:: Title of the window
    active_map #:: the current map
    gadgets #:: list of gadgets
    map(name_of_map, newpos=None) #:: return the map `name_of_map`. If `newpos` is set to map.pos, else the previous position.
    surface(char_of_surface) #:: returns the surface with character `char_of_surface`
    item(item_name) #:: returns the item with name `item_name`
```

## Initializing a `Game` object

```py
game = Game("Name of the game", "path_to_settings", [list, of, Gadget, Classes], first_map=None, theme="Dark")
```

See [gadgets](./gadgets) for some demo gadgets you may want to add

`first_map` corresponds to the name of the first [map](./maps) where the player is spawned.
If `first_map` is not set, `active_map` will be `None`. You must then set the `active_map` yourself before calling `game.run()`

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
