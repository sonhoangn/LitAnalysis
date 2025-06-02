import sys
import re
import datetime
import os
import threading

from pygments.styles.dracula import foreground

import main
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, filedialog, ttk
import tkinter

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


FILE_PATH = Path(__file__).parent
ASSETS_PATH = FILE_PATH / "assets"
ICON_PATH = ASSETS_PATH / "icon.png"
API_KEY = None
llm_selection = None
directory = None
specific_pdf = None

def ct():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S")
    return formatted_time

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Automated Research Papers Analysis, Summarization and Consolidation Tool")
window.geometry("1250x454")
window.configure(bg = "#9CACFD")


canvas = Canvas(
    window,
    bg = "#9CACFD",
    height = 454,
    width = 1250,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("bg_2_n.png"))
image_1 = canvas.create_image(
    625.0,
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
last_opened_directory = "/"
# Choose directory
def choose_dir():
    global directory, last_opened_directory
    directory = filedialog.askdirectory(
        title="Select Folder containing research papers.",
        initialdir=last_opened_directory
    )
    if directory:
        last_opened_directory=directory
        print(f"{ct()} - All PDF(s) in {directory} to be processed are: \n")
        el_files = [f for f in os.listdir(directory) if f.endswith((".pdf"))]
        index = 1
        for file in el_files:
            print(f"{index}. \n", file)
            index += 1
    else:
        print(f"{ct()} - No folder selected, please choose a folder containing research papers to begin processing!\n")
    return directory

# Main function
def start_analysis_s():
    global API_KEY, llm_selection, directory
    if not API_KEY or not llm_selection or not  directory:
        print(f"{ct()} - Insufficient data provided (Either no PDF found or missing API key or missing LLM), kindly double check your input!\n")
        return
    print(f"{ct()} - Start analyzing PDFs found in: {directory}, LLM: {llm_selection}, API Key: {API_KEY}\n")
    def thread_process():
        main.main(directory,API_KEY,llm_selection)

    thread=threading.Thread(target=thread_process)
    thread.start()
    print(f"{ct()} - Basic Analysis in progress, please wait...\n")

# Choose specific PDF file
def file_selection():
    global API_KEY, llm_selection, specific_pdf, last_opened_directory
    specific_pdf = filedialog.askopenfilename(
        title="Select the target research paper",
        initialdir=last_opened_directory,
        filetypes=(
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        )
    )
    if specific_pdf and API_KEY and llm_selection:
        last_opened_directory=os.path.dirname(specific_pdf)
        print(f'{ct()} - "{specific_pdf}" has been forwarded to Gemini for analysis.\n')
    else:
        print(f'{ct()} - Insufficient data provided (Either no PDF found or missing API key or missing LLM), kindly double check your input!\n')
        return
    def thread_ps():
        main.main_c(specific_pdf, API_KEY, llm_selection) # function to do specific analysis

    thread=threading.Thread(target=thread_ps)
    thread.start()
    return specific_pdf

button_image_1 = PhotoImage(
    file=relative_to_assets("browse.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=file_selection,
    relief="flat"
)
button_1.place(
    x=1148.0,
    y=400.0,
    width=40.0,
    height=40.0
)

def chat():
    global API_KEY, llm_selection
    userinput = entry_1.get()
    if userinput and API_KEY and llm_selection:
        main.main_chat(API_KEY,llm_selection,userinput)
        entry_1.delete(0, tkinter.END)
        print(f'{ct()} - User question: "{userinput}"')
        pass
    else:
        print(f'{ct()} - Either one of the following information is missing, please kindly provide them: message to be sent, API key or LLM selection.\n')
        return

#Send button
button_image_2 = PhotoImage(
    file=relative_to_assets("check.png"))
send_chat = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=chat,
    relief="flat"
)
send_chat.place(
    x=1198.0,
    y=400.0,
    width=40.0,
    height=40.0
)

# Quote Extraction function
def start_qe():
    global API_KEY, llm_selection, directory
    if not API_KEY or not llm_selection or not  directory:
        print(f"{ct()} - Insufficient data provided (Either no PDF found or missing API key or missing LLM), kindly double check your input!\n")
        return
    print(f"{ct()} - Start extracting quotes for PDFs found in: {directory}, LLM: {llm_selection}, API Key: {API_KEY}\n")
    def thread_process():
        main.main_q(directory,API_KEY,llm_selection)

    thread=threading.Thread(target=thread_process)
    thread.start()
    print(f"{ct()} - Quotes extraction in progress, please wait...\n")

button_image_3 = PhotoImage(
    file=relative_to_assets("qe.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=start_qe,
    relief="flat"
)
button_3.place(
    x=293.0,
    y=96.0,
    width=80.0,
    height=35.0
)

# Main function
def start_analysis_d():
    global API_KEY, llm_selection, directory
    if not API_KEY or not llm_selection or not  directory:
        print(f"{ct()} - Insufficient data provided (Either no PDF found or missing API key or missing LLM), kindly double check your input!\n")
        return
    print(f"{ct()} - Start analyzing PDFs found in: {directory}, LLM: {llm_selection}, API Key: {API_KEY}\n")
    def thread_process():
        main.main_d(directory,API_KEY,llm_selection)

    thread=threading.Thread(target=thread_process)
    thread.start()
    print(f"{ct()} - Basic Analysis in progress, please wait...\n")

button_image_4 = PhotoImage(
    file=relative_to_assets("dt.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=start_analysis_d,
    relief="flat"
)
button_4.place(
    x=163.0,
    y=96.0,
    width=80.0,
    height=35.0
)

# Main function
def start_analysis():
    global API_KEY, llm_selection, directory
    if not API_KEY or not llm_selection or not  directory:
        print(f"{ct()} - Insufficient data provided (Either no PDF found or missing API key or missing LLM), kindly double check your input!\n")
        return
    print(f"{ct()} - Start analyzing PDFs found in: {directory}, LLM: {llm_selection}, API Key: {API_KEY}\n")
    def thread_process():
        main.main(directory,API_KEY,llm_selection)

    thread=threading.Thread(target=thread_process)
    thread.start()
    print(f"{ct()} - Basic Analysis in progress, please wait...\n")

button_image_5 = PhotoImage(
    file=relative_to_assets("ba.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=start_analysis,
    relief="flat"
)
button_5.place(
    x=33.0,
    y=96.0,
    width=80.0,
    height=35.0
)
#Save API Key and LLM Selection

def save_input():
    global API_KEY
    global llm_selection
    API_KEY = apikey_input.get()
    llm_selection = llm_combobox.get()
    if not API_KEY:
        messagebox.showwarning("Warning", f"{ct()} - API Key not found!")
        return
    elif not llm_selection:
        messagebox.showwarning("Warning", "No LLM selection detected!")
        return
    print(f"{ct()} - API Key: {API_KEY}, has been provided and saved!\n - LLM: {llm_selection}, selected!\n")
    return API_KEY, llm_selection

button_image_6 = PhotoImage(
    file=relative_to_assets("check.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=save_input,
    relief="flat"
)
button_6.place(
    x=396.0,
    y=39.0,
    width=40.0,
    height=40.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("info.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print(f"{ct()} - Created by Nguyen, Son Hoang & Le, Thi Dieu Ly."
                          "\nKindly refer to all source codes and revisions on:"
                          "\nhttps://github.com/sonhoangn/LitAnalysis/tree/main/programs"
                          "\nUsage: This program leverages different Gemini models from Google using Google-provided API key to help analyzing research papers in PDF form.\n"),
    relief="flat"
)
button_7.place(
    x=396.0,
    y=93.0,
    width=40.0,
    height=40.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("browse.png"))
browse = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=choose_dir,
    relief="flat"
)
browse.place(
    x=8.0,
    y=39.0,
    width=40.0,
    height=40.0
)

# User messages
entry_image_1 = PhotoImage(
    file=relative_to_assets("conv_box.png"))
entry_bg_1 = canvas.create_image(
    795.0,
    423.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=462.0,
    y=411.0,
    width=670.0,
    height=28.0
)
entry_1.bind("<Return>", lambda event: chat())

entry_image_2 = PhotoImage(
    file=relative_to_assets("api_input.png"))
entry_bg_2 = canvas.create_image(
    115.0,
    64.0,
    image=entry_image_2
)
apikey_input = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
apikey_input.place(
    x=67.0,
    y=51.0,
    width=100.0,
    height=20.0
)

# LLM Selection box
llm_options = ["gemini-2.5-flash-preview-05-20", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"]
entry_image_3 = PhotoImage(
    file=relative_to_assets("llm_droplist.png"))
entry_bg_3 = canvas.create_image(
    283,
    64.0,
    image=entry_image_3
)
llm_combobox = ttk.Combobox(
    window,
    values=llm_options,
    state="readonly",
    width=329
)
llm_combobox.place(
    x=193.0,
    y=51.0,
    width=185.0,
    height=20.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("conv_cbox_n.png"))
entry_bg_4 = canvas.create_image(
    844.5,
    219.5,
    image=entry_image_4
)
conv = Text(
    bd=0,
    bg="#ffffff",
    fg="#000000",
    highlightthickness=0
)
conv.place(
    x=479.0,
    y=53.0,
    width=731.0,
    height=331.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("terminal_2.png"))
entry_bg_5 = canvas.create_image(
    221.5,
    298.0,
    image=entry_image_5
)
terminal_display = Text(
    bd=0,
    bg="#000000",
    fg="#000716",
    highlightthickness=0
)
terminal_display.place(
    x=36.0,
    y=164.0,
    width=371.0,
    height=266.0
)

class StdoutRedirector(object):
    def __init__(self, ter_dis, conv_box):
        self.ter_dis = ter_dis
        self.conv_box = conv_box
        self.ter_dis.tag_config("output", foreground="#8cffff")
        # self.conv_box.tag_config("content", foreground="#56ff3c")
        # self.conv_box.tag_config("title", foreground="#ffff78")
        # self.conv_box.tag_config("p_name", foreground="#ff50f3")
        # self.conv_box.tag_config("separator", foreground="#ffcc78")
        # self.conv_box.tag_config("separator_s", foreground="#500068")
        self.conv_box.tag_config("content", foreground="#030c26")
        self.conv_box.tag_config("title", foreground="#1d2ab5")
        self.conv_box.tag_config("p_name", foreground="#411a8a")
        self.conv_box.tag_config("separator", foreground="#914017")
        self.conv_box.tag_config("separator_s", foreground="#567506")
        self.ter_dis.tag_config("user", foreground="#56ff3c")

    def write(self, string):
        match1=re.search(r"Research Paper Analysis: (.*)",string)
        match2=re.search(r"1. Objective: (.*)",string)
        match3=re.search(r"2. Methodology:(.*)",string)
        match4=re.search(r"3. Results: (.*)",string)
        match5=re.search(r"4. Overall Summary: (.*)",string)
        match6=re.search(r"Follow-up Analysis: (.*)",string)
        match7=re.search(r"1. Response: (.*)",string)
        match8=re.search(r"2. Supporting Quote: (.*)",string)
        match9=re.search(r"3. Explanation of Relevance: (.*)",string)
        match10=re.search(r".*?User question:\..*",string)
        if match1:
            aws=match1.group(1).strip()
            self.conv_box.insert(tkinter.END, "="*91, "separator")
            self.conv_box.insert(tkinter.END, "\n\nResearch Paper Analysis: \n", "title")
            self.conv_box.insert(tkinter.END, f'{aws}\n', "p_name")
            self.conv_box.insert(tkinter.END, f'\n', "content")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match2:
            aws=match2.group(1).strip()
            self.conv_box.insert(tkinter.END, "1. Objective: \n", "title")
            self.conv_box.insert(tkinter.END, f'{aws}\n', "content")
            self.conv_box.insert(tkinter.END, f'\n', "content")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match3:
            aws=match3.group(1).strip()
            aws_lines=aws.split('.')
            self.conv_box.insert(tkinter.END, "2. Methodology: \n", "title")
            for line in aws_lines:
                self.conv_box.insert(tkinter.END, f'{line}\n', "content")
            self.conv_box.insert(tkinter.END, f'\n', "content")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match4:
            aws=match4.group(1).strip()
            self.conv_box.insert(tkinter.END, "3. Results: \n", "title")
            self.conv_box.insert(tkinter.END, f'{aws}\n', "content")
            self.conv_box.insert(tkinter.END, f'\n', "content")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match5:
            aws=match5.group(1).strip()
            self.conv_box.insert(tkinter.END, "4. Overall Summary: \n", "title")
            self.conv_box.insert(tkinter.END, f'{aws}\n', "content")
            self.conv_box.insert(tkinter.END, f'\n', "content")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match6:
            aws=match6.group(1).strip()
            self.conv_box.insert(tkinter.END, "-"*91, "separator_s")
            self.conv_box.insert(tkinter.END, "\n\nFollow-up Analysis: \n", "title")
            self.conv_box.insert(tkinter.END, f'{aws}\n', "p_name")
            self.conv_box.insert(tkinter.END, f'\n', "content")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match7:
            aws=match7.group(1).strip()
            self.conv_box.insert(tkinter.END, "1. Response: \n", "title")
            self.conv_box.insert(tkinter.END, f'{aws}\n', "content")
            self.conv_box.insert(tkinter.END, f'\n', "output_1")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match8:
            aws=match8.group(1).strip()
            self.conv_box.insert(tkinter.END, "2. Supporting Quote: \n", "title")
            self.conv_box.insert(tkinter.END, f'{aws}\n', "content")
            self.conv_box.insert(tkinter.END, f'\n', "content")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match9:
            aws=match9.group(1).strip()
            self.conv_box.insert(tkinter.END, "3. Explanation of Relevance: \n", "title")
            self.conv_box.insert(tkinter.END, f'{aws}\n', "content")
            self.conv_box.insert(tkinter.END, f'\n', "content")
            self.conv_box.see(tkinter.END)
            self.conv_box.update_idletasks()
        elif match10:
            aws=match10.group(1)
            self.ter_dis.insert(tkinter.END, f'User Question: \n', "user")
            self.ter_dis.insert(tkinter.END, f'{aws}\n', "user")
            self.ter_dis.insert(tkinter.END, f'\n', "output")
            self.ter_dis.see(tkinter.END)
            self.ter_dis.update_idletasks()
        else:
            self.ter_dis.insert(tkinter.END, string, "output")
            self.ter_dis.see(tkinter.END)
            self.ter_dis.update_idletasks()
    def flush(self):
        pass
sys.stdout = StdoutRedirector(terminal_display,conv)

window.resizable(False, False)
window.mainloop()
