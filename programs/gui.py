import sys
import re
import datetime
import os
import threading
import main
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, filedialog, ttk
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

# Choose directory
directory = None
def choose_dir():
    global directory
    directory = filedialog.askdirectory(title="Select Folder containing research papers.")
    if directory:
        browse_dir.delete(0, "end")
        browse_dir.insert(0, directory)
        print(f"{ct()} - All PDF(s) in {directory} to be processed are: ")
        el_files = [f for f in os.listdir(directory) if f.endswith((".pdf"))]
        index = 1
        for file in el_files:
            print(f"{index}. ", file)
            index += 1
    else:
        print(f"{ct()}No folder selected, please choose a folder containing research papers to begin processing!")
    return directory

entry_image_1 = PhotoImage(
    file=relative_to_assets("input.png"))
entry_bg_1 = canvas.create_image(
    205.5,
    62.0,
    image=entry_image_1
)
browse_dir = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
browse_dir.place(
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

# LLM Selection box
llm_options = ["gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.0-flash-lite-preview-02-05"]
entry_image_3 = PhotoImage(
    file=relative_to_assets("input.png"))
entry_bg_3 = canvas.create_image(
    642.5,
    118.0,
    image=entry_image_3
)
llm_combobox = ttk.Combobox(
    window,
    values=llm_options,
    state="readonly",
    width=329
)
llm_combobox.place(
    x=477.0,
    y=107.0,
    width=331.0,
    height=20.0
)

# Quote Extraction function
def start_qe():
    global API_KEY, llm_selection, directory
    if not API_KEY or not llm_selection or not  directory:
        print(f"{ct()} - Insufficient data provided (Either no PDF found or missing API key or missing LLM), kindly double check your input!")
        return
    print(f"{ct()} - Start extracting quotes for PDFs found in: {directory}, LLM: {llm_selection}, API Key: {API_KEY}\n")
    def thread_process():
        main.main_q(directory,API_KEY,llm_selection)

    thread=threading.Thread(target=thread_process)
    thread.start()
    print(f"{ct()} - Quotes extraction in progress, please wait...")

button_image_2 = PhotoImage(
    file=relative_to_assets("qe.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=start_qe,
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
# Save LLM Selection
llm_selection = None
def save_llm_selection():
    global llm_selection
    llm_selection = llm_combobox.get()
    if not llm_selection:
        messagebox.showwarning("Warning", "No LLM selection detected!")
        return
    print(f"{ct()} - LLM: {llm_selection}, selected!\n")
    return llm_selection

# LLM Select
button_image_4 = PhotoImage(
    file=relative_to_assets("check.png"))
llm_select = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=save_llm_selection,
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
    command=lambda: print(f"{ct()} - Created by Nguyen, Son Hoang & Le, Thi Dieu Ly."
                          "\nKindly refer to all source codes and revisions on:"
                          "\nhttps://github.com/sonhoangn/LitAnalysis/tree/main/programs"
                          "\nUsage: This program leverages different Gemini models from Google using Google-provided API key to help analyzing research papers in PDF form.\n"),
    relief="flat"
)
info.place(
    x=396.0,
    y=96.0,
    width=40.0,
    height=40.0
)

# Browse directory
button_image_6 = PhotoImage(
    file=relative_to_assets("browse.png"))
browse = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=choose_dir,
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

# Main function
def start_analysis():
    global API_KEY, llm_selection, directory
    if not API_KEY or not llm_selection or not  directory:
        print(f"{ct()} - Insufficient data provided (Either no PDF found or missing API key or missing LLM), kindly double check your input!")
        return
    print(f"{ct()} - Start analyzing PDFs found in: {directory}, LLM: {llm_selection}, API Key: {API_KEY}\n")
    def thread_process():
        main.main(directory,API_KEY,llm_selection)

    thread=threading.Thread(target=thread_process)
    thread.start()
    print(f"{ct()} - Basic Analysis in progress, please wait...")

button_image_1 = PhotoImage(
    file=relative_to_assets("ba.png"))
analysis_button = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=start_analysis,
    relief="flat"
)
analysis_button.place(
    x=30.0,
    y=101.0,
    width=143.0,
    height=34.0
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
