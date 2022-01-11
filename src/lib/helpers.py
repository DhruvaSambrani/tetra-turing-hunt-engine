from PIL import Image
import PySimpleGUI as sg
import os
import io
import sys
import webbrowser

def play_media(media_path):
    if not (media_path is None):
        media_type, file_path = media_path.split("::")
        if media_type == "image":
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            bio = io.BytesIO()
            image.save(bio, format="PNG") 
            w = sg.Window("Media", layout=[[sg.Image(bio.getvalue())]])
            while True:
                e, v = w.read()
                if e == sg.WIN_CLOSED:
                    break
        elif media_type == "link":
            webbrowser.open(file_path)
        else:
            if sys.platform=="windows":
                os.startfile(file_path)
            else:
                os.system("xdg-open "+file_path)
