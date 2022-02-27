# Items

`Item`s are interactable elements in the game, which are used to set goals, record whether something is done and manipulate other elements in the game.

## .item Files

Every item is associted with a `.item` file. A `.item` file is simply a json file with the following structure - 

```json
{
name: "string",
desc: "string",
need_input: boolean,
collectable: boolean,
answerhash: "[string]",
media_path: "[string]",
code_file: "[string]"
}
```

1. `name`, `desc` are self explanatory
2. `need_input` tells the game engine whether an input bar is to be displayed when the item is interacted with
3. `collectable` tells the game engine if the item is to be put into the [Pocket][#pocket] when interaction is [successful](#interaction)
4. `answerhash` is an optional parameter which is the correct "answer". [See more](#answerhash)
5. `media_path` is an optional parameter which gives information about the media that is associated with the item. [See more](#media)
6. `code_file` is an optional parameter which gives the path to the `.py` file that is run when the item [interation](#interaction) is successful. [See more](#item-coding)


## Pocket

Pocket is a list of items that are "collected" by the user. This can be used to record what the user has seen, or to retain items which may be useful for the user to progress in the game. Pocket items can be [reinteracted](#interaction) with. Items can be marked as collectable in the [`.item` file](#.item-files) or can be added manually via [code file](#item-coding).

The game always starts with no items in the `Pocket`.

## Interaction

The following section describes how an item interaction works.

### From Moving on the Map

1. User moves onto a location where there is an item(as per the [Map]("./maps"))
2. A dialog is shown with 
    1. `title`
    2. `desc`
    3. Input bar and submit button as per `need_input`
    4. Show Media button if `media_path` is non-empty
    5. Cancel button
3. User input is awaited:
    1. If Show Media button is clicked, appropriate [media is shown](#media). Interaction continues.
    2. If Submit button is clicked, input typed in input bar is hashed, and checked against `answerhash`. If matched, interaction ends with success else, interaction continues.
    3. If Cancel button is clicked
        1. If `need_input`, then interation is not successful
        2. Else interaction is successful
4. If interaction is successful
    1. If `collectable`, then item is added to Pocket
    2. If `code_file` is non empty, `code_file` is [run](#item-coding)

### Clicking on Item from Pocket

1. User clicks appropriate button in `Pocket`
2. A dialog is shown as above, but without input bar or Submit button
3. User input is awaited:
    1. If Show Media button is clicked, appropriate [media is shown](#media). Interaction continues.
    2. If Cancel button is clicked, interaction is successful.
4. If interaction is successful
    1. If `code_file` is non empty, `code_file` is [run](#item-coding)

## answerhash

This parameter holds the hashed version of the "corret answer". We store it as a hashed value because it is technically possible for the source code to be shared to the participants.

To hash your answer, do 

```python
import hashlib

answer = "the actual answer here which is case-sensitive"

print(hashlib.md5(answer.encode()).hexdigest())
```
and then copy the output to this parameter

## Media

Items can have some kinds of media associated with them. Generally these are pictures or links to websites.

Every `media_path` entry should look like this

`mediatype::path/to/media`

Supported mediatypes are:
- `image` - shown as a popup in a Pillow frame
- `link` - a link to something on the internet
- `external` - playing the media is relegated to the OS and the default player is requested to play the media.

## Item coding

Every item can be associated with a python file which will be evaluated on item interaction success. To manipulate objects in the game, you can use the [`game` object](game.md)

