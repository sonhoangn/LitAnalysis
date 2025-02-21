import sys
import re
import datetime
import threading
import main
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import tkinter


FILE_PATH = Path(__file__).parent
ASSETS_PATH = FILE_PATH / "assets"
ICON_PATH = ASSETS_PATH / "icon.png"

def ct():
    return datetime.datetime.now()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Automated Research Papers Analysis, Summarization and Consolidation Tool")

window.geometry("900x454")
window.configure(bg = "#9CACFD")


canvas = Canvas(
    window,
    bg = "#9CACFD",
    height = 454,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("bg.png"))
image_1 = canvas.create_image(
    450.0,
    222.0,
    image=image_image_1
)

# Set window icon
try:
    icon = tkinter.PhotoImage(file=str(ICON_PATH))  # Convert Path to string
    window.iconphoto(True, icon)
except FileNotFoundError:
    print(f"{ct()} - Error: Icon file not found at {ICON_PATH}\n")
except Exception as e:
    print(f"{ct()} - Error loading icon: {e}\n")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    205.5,
    62.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=40.0,
    y=51.0,
    width=331.0,
    height=20.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("input.png"))
entry_bg_2 = canvas.create_image(
    643.5,
    64.0,
    image=entry_image_2
)
apikey_input = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
apikey_input.place(
    x=478.0,
    y=53.0,
    width=331.0,
    height=20.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    642.5,
    118.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=477.0,
    y=107.0,
    width=331.0,
    height=20.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=31.0,
    y=101.0,
    width=146.0,
    height=34.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=224.0,
    y=101.0,
    width=148.0,
    height=34.0
)

#Save API Key
API_KEY = None
def save_key():
    global API_KEY
    API_KEY = apikey_input.get()
    if not API_KEY:
        messagebox.showwarning("Warning", f"{ct()} - API Key not found!")
        return
    print(f"{ct()} - API Key: {API_KEY}, has been provided and saved!")
    return API_KEY

button_image_3 = PhotoImage(
    file=relative_to_assets("key.png"))
apikey_confirm = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=save_key,
    relief="flat"
)
apikey_confirm.place(
    x=835.0,
    y=44.0,
    width=40.0,
    height=40.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("check.png"))
llm_select = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("LLM selected."),
    relief="flat"
)
llm_select.place(
    x=835.0,
    y=98.0,
    width=40.0,
    height=40.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("info.png"))
info = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Info clicked"),
    relief="flat"
)
info.place(
    x=396.0,
    y=96.0,
    width=40.0,
    height=40.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("browse.png"))
browse = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Browse button clicked"),
    relief="flat"
)
browse.place(
    x=396.0,
    y=41.0,
    width=40.0,
    height=40.0
)

# Terminal box
entry_image_4 = PhotoImage(
    file=relative_to_assets("terminal.png"))
entry_bg_4 = canvas.create_image(
    450.0,
    298.0,
    image=entry_image_4
)
terminal = Text(
    bd=0,
    bg="#000000",
    fg="#000716",
    highlightthickness=0
)
terminal.place(
    x=36.0,
    y=164.0,
    width=828.0,
    height=266.0
)

# Redirect stdout to the terminal area
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.tag_config("output", foreground="lightblue")  # Configure the tag
    def write(self, string):
        self.text_widget.insert(tkinter.END, string, "output")  # Apply the tag
        self.text_widget.see(tkinter.END)
        self.text_widget.update_idletasks()
    def flush(self):
        pass
sys.stdout = StdoutRedirector(terminal)

window.resizable(False, False)
window.mainloop()
