from PIL import Image
import PySimpleGUI as sg
import os
import io
import sys
import webbrowser
import subprocess

def play_media(media_path):
    if not (media_path is None):
        media_type, file_path = media_path.split("::")
        if media_type == "image":
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            bio = io.BytesIO()
            image.save(bio, format="PNG") 
            w = sg.Window("Media", layout=[[sg.Image(bio.getvalue())], [sg.Button("Close", expand_x=True)]], modal=True, keep_on_top=True, finalize=True)
            w.bind("<Escape>", "Close")

            while True:
                e, v = w.read()
                if e == sg.WIN_CLOSED or e == "Close":
                    break
            w.close()

        elif media_type == "link":
            webbrowser.open(file_path)
        else:
            open_with_default_app(file_path)


def get_platform():
    if sys.platform == 'linux':
        try:
            proc_version = open('/proc/version').read()
            if 'Microsoft' in proc_version:
                return 'wsl'
        except:
            pass
    return sys.platform

def open_with_default_app(filename):
    platform = get_platform()
    if platform == 'darwin':
        subprocess.call(('open', filename))
    elif platform in ['win64', 'win32']:
        os.startfile(filename.replace('/','\\'))
    elif platform == 'wsl':
        subprocess.call('cmd.exe /C start'.split() + [filename])
    else:                                   # linux variants
        subprocess.call(('xdg-open', filename))
