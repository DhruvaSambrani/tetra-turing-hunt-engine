# GTA - Stress City
This is a Virtual Treasure Hunt game hosted by the Turing Club, made using a custom terminal-based engine, [Tetra](https://github.com/DhruvaSambrani/turing-hunt-engine).

# Objectives

## Primary

- [ ] Build the world with maps of all areas
    - [ ] Link maps via transitions
    - [ ] Make mini-map tool to see current location relative to the entire world 
- [ ] Collate a list of clue-essential items
    - [ ] Create media files for clue items
    - [ ] Code the behaviour and location of items
- [ ] Sample playtest to debug

## Secondary 

- [ ] Collate a list of non-essential fluff (world-building) items/NPCs
    - [ ] Code the behaviour and location of items
- [ ] Bug [Dhruva](https://github.com/DhruvaSambrani) to implement save states

## Misc. - not sure if necessary
- [ ] Implement diagonal player movement

# Developing

1. Install `PySimpleGUI`, `numpy`, `pillow` and FiraCode Font provided in /assets.
2. `cd src`
3. Run `python3 libs/terminal.py`

## Trouble-shooting map rendering issues
1. Make sure that you have installed FiraCode Nerd Font provided in /assets. 
2. Run the `font_gallery.py` script provided in /helpers and verify that FiraCode is listed.  
3. If the issue still persists, one of more of the unicode characters used in the map are not supported by FiraCode and have to be changed.
