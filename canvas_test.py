import tkinter as tk
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

root = tk.Tk()
root.title('PC info')
root.geometry('300x300')

# Create NoteBook
book = ttk.Notebook(root)
book.pack(fill=tk.BOTH, expand=1)
root.iconbitmap(default="pc.ico")
# Create Main Frame
OS_info = tk.Frame(book)
cpu_info = tk.Frame(book)
gpu_info = tk.Frame(book)
ram_info = tk.Frame(book)
disks_info = tk.Frame(book)

# put the main frame into notebook
book.add(OS_info, text='OS')
book.add(cpu_info, text='CPU')
book.add(gpu_info, text="GPU")
book.add(ram_info, text="RAM")
book.add(disks_info, text="DISK")

# Create canvas inside main frame
canvas_os = tk.Canvas(OS_info)
canvas_os.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create ScrollBar inside main frame
my_scrollbar = ttk.Scrollbar(OS_info, orient=tk.VERTICAL, command=canvas_os.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_os.configure(yscrollcommand=my_scrollbar.set)

uname = platform.uname()
canvas_os.create_text(50,10,text=f"System: {uname.system}")
canvas_os.create_text(87,30,text=f"Node name: {uname.node}")
canvas_os.create_text(32,50,text=f"Release: {uname.release}")
canvas_os.create_text(53,70,text=f"Version: {uname.version}")
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
canvas_os.create_text(80,90,text=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

canvas_cpu = tk.Canvas(cpu_info)
canvas_cpu.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(cpu_info, orient=tk.VERTICAL, command=canvas_cpu.yview)
canvas_cpu.pack(side=tk.RIGHT, fill=tk.Y)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_cpu.configure(yscrollcommand=my_scrollbar.set)

cpufreq = psutil.cpu_freq()
canvas_cpu.create_text(50, 10,text=f"Physical cores: {psutil.cpu_count(logical=False)}")
canvas_cpu.create_text(40,30,text=f"Total cores: {psutil.cpu_count(logical=True)}")
canvas_cpu.create_text(54,50,text=f"Max Frequency: {cpufreq.max:.2f}Mhz")
# canvas_cpu.create_text(50,70,text=f"Total CPU Usage: {psutil.cpu_percent()}%")

canvas_gpu = tk.Canvas(gpu_info)
canvas_gpu.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(gpu_info, orient=tk.VERTICAL, command=canvas_gpu.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_gpu.configure(yscrollcommand=my_scrollbar.set)

gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    # get the GPU id
    gpu_id = gpu.id
    # name of GPU
    gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
    gpu_load = f"{gpu.load*100}%"
    # get free memory in MB format
    gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
    gpu_temperature = f"{gpu.temperature} °C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
        gpu_total_memory, gpu_temperature, gpu_uuid
    ))
canvas_gpu.create_text(70,10, text=f"GPU name: {gpu.name}")
canvas_gpu.create_text(70,30, text=f"Total memory: {gpu.memoryTotal}MB")
canvas_gpu.create_text(142,50,text=f"UUID: {gpu.uuid}")

canvas_ram = tk.Canvas(ram_info)
canvas_ram.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create ScrollBar inside main frame
my_scrollbar = ttk.Scrollbar(ram_info, orient=tk.VERTICAL, command=canvas_ram.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_ram.configure(yscrollcommand=my_scrollbar.set)

svmem = psutil.virtual_memory()

canvas_ram.create_text(40,10,text=f"Total: {get_size(svmem.total)}")
canvas_ram.create_text(50,30,text=f"Available: {get_size(svmem.available)}")
canvas_ram.create_text(40,50,text=f"Used: {get_size(svmem.used)}")

canvas_disk = tk.Canvas(disks_info)
canvas_disk.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create ScrollBar inside main frame
my_scrollbar = ttk.Scrollbar(disks_info, orient=tk.VERTICAL, command=canvas_disk.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_disk.configure(yscrollcommand=my_scrollbar.set)

partitions = psutil.disk_partitions()

# canvas_disk.create_text(50,10,text=f"=== Device: {partitions.device} ===")
# canvas_disk.create_text(50, 30, text=f"  Mountpoint: {partitions.mountpoint}")

root.mainloop()