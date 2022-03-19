# Turing Hunt Engine

This is an Engine for the Turing Hunt.

The aim is to simplify the making of an interactive virtual hunt by splitting the data from the code.

# Objectives

## Primary

- [x] Start a terminal screen using PSGui
- [x] Handle `Surface`s
    - [x] Read surfaces.json and load all `Surface`s

- [x] Make a map displaying logic
    - [x] Read map from file and display it on terminal screen
    - [x] Read map metadata
    - [x] Capture and react to the user movement input
    - [x] Make sure map can be traversed only on `walkable` `Surface`s
    - [x] Make map to map transitions

- [x] Implement Pocket
    - [x] Actual storage
    - [x] Display Pocket

- [ ] Implement Logging and LoggerView

- [ ] Make item interaction logic
    - [x] Read items from file and place in map
    - [x] Interact with items on map
    - [x] Display item interaction screen
    - [x] Make interaction mechanics
    - [x] Allow arbitrary code execution 
    - [x] document
    - [x] Arbitrary output types
    - [ ] Arbitrary input types

## Secondary 

- [ ] Make game builders
    - [x] Make bitmap -> map
    - [ ] Make item builder

- [ ] Implement Save game 

# Developing

1. Install `PySimpleGUI`, `numpy`, `pillow`
2. `cd src`
3. Run `python3 libs/terminal.py`


## Trouble-shooting map rendering issues
1. Make sure that you have installed FiraCode Nerd Font provided in /assets. 
2. Run the `font_gallery.py` script provided in /helpers and verify that FiraCode is listed.  
3. If the issue still persists, one of more of the unicode characters used in the map are not supported by FiraCode and have to be changed.