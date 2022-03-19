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
