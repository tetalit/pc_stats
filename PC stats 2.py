import time
import psutil
import platform
import GPUtil
from datetime import datetime
from tabulate import tabulate
from tkinter import *
from tkinter import ttk

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def finish():
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Закрытие приложения")

root = Tk()  # создаем корневой объект - окно
root.title("PC info")  # устанавливаем заголовок окна
root.iconbitmap(default="pc.ico")
root.geometry("600x600")  # устанавливаем размеры окна, то что с плюсом, это позиция в которой появится окно при запуске
#root.resizable(False, False) # запрет на изменение размера окна
root.protocol("WM_DELETE_WINDOW", finish)
root.minsize(250,150) # ограничение размеров окна
root.maxsize(2560,1440)

root.config(cursor="dot")
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab1, text='os')
tab_control.add(tab2, text='cpu')
tab_control.add(tab3, text='gpu')

# root.attributes("-toolwindow", True)
# root.attributes("-alpha", 0.5) #прозрачность
# root.attributes("-fullscreen", True) #полный экран

# label = Label(text="Hello METANIT.COM")  # создаем текстовую метку
# label.pack(anchor="n")  # размещаем метку в окне

# value_var = IntVar()
# progressbar = ttk.Progressbar(orient="horizontal", variable=value_var)
# progressbar.pack(fill=X, padx=6, pady=6)
# label = ttk.Label(textvariable=value_var)
# label.pack(anchor=NW, padx=6, pady=6)
# def start(): progressbar.start(1000)  # запускаем progressbar
# def stop(): progressbar.stop()  # останавливаем progressbar
# start_btn = ttk.Button(text="Start", command=start)
# start_btn.pack(anchor=SW, side=LEFT, padx=6, pady=6)
# stop_btn = ttk.Button(text="Stop", command=stop)
# stop_btn.pack(anchor=SE, side=RIGHT, padx=6, pady=6)

canvas = Canvas(bg="white", width=400, height=400)
canvas.pack(anchor=CENTER, expand=1)

uname = platform.uname()
canvas.create_text(50,10,text=f"System: {uname.system}")
canvas.create_text(87,30,text=f"Node name: {uname.node}")
canvas.create_text(32,50,text=f"Release: {uname.release}")
canvas.create_text(53,70,text=f"Version: {uname.version}")
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
canvas.create_text(80,90,text=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

root.mainloop()