from tkinter import *
from tkinter import ttk

import time

import psutil
import platform
import GPUtil
from datetime import datetime
from tabulate import tabulate

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

uname = platform.uname()
window = Tk()
window.title("aboba")
window.geometry('800x600')
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text='cpu')
tab_control.add(tab2, text='gpu')
tab_control.add(tab3, text='ram')
lbl1 = Label(tab1, text=f"System: {uname.system}  Release: {uname.release}  Version: {uname.version}")
lbl1.grid(column=0, row=0)
lbl2 = Label(tab2, text='')
lbl2.grid(column=0, row=0)
lbl3 = Label(tab3, text='')
lbl3.grid(column=0, row=0)
tab_control.pack(expand=1, fill='both')
window.mainloop()
