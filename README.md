# Turing Hunt Engine

This is an Engine for the Turing Hunt.

The aim is to simplify the making of an interactive virtual hunt by splitting the data from the code.

# Objectives

- [x] Start a terminal screen using PSGui
- [ ] Handle `Surface`s
    - [ ] Read surfaces.json and load all `Surface`s

- [ ] Make a map displaying logic
    - [x] Read map from file and display it on terminal screen
    - [ ] Read map metadata
    - [x] Capture and react to the user movement input
    - [ ] Make sure map can be traversed only on `walkable` `Surface`s
    - [ ] Make map to map transitions
    - [ ] Emit events for code to listen to

- [ ] Make item interaction logic
    - [ ] Read items from file and place in map
    - [ ] Interact with items on map
    - [ ] Display item interaction screen
    - [ ] Make interaction mechanics


# Developing
1. Install PySimpleGUI and numpy
2. Run `python3 terminal.py`
