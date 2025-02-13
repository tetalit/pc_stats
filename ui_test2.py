import tkinter as tk
from tkinter import ttk
import time
import psutil
import platform
import GPUtil
from datetime import datetime
from GPUtil import GPU
from tabulate import tabulate

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

root = tk.Tk()
root.title('PC info')
root.geometry('600x500')
root.configure(bg='black')

# Изменение стиля для текста
style = ttk.Style()
style.configure("TLabel", foreground="white", background="black", font=("Helvetica", 12))  # увеличиваем размер шрифта
style.configure("TNotebook", background="black", font=("Helvetica", 12))  # увеличиваем шрифт для вкладок
style.configure("TNotebook.Tab", background="black", foreground="black", padding=[10, 5], font=("Helvetica", 12))  # текст вкладок больше

book = ttk.Notebook(root, style="TNotebook")
book.pack(fill=tk.BOTH, expand=1)

OS_info = tk.Frame(book, bg='black')
cpu_info = tk.Frame(book, bg='black')
gpu_info = tk.Frame(book, bg='black')
ram_info = tk.Frame(book, bg='black')
disks_info = tk.Frame(book, bg='black')

book.add(OS_info, text='OS')
book.add(cpu_info, text='CPU')
book.add(gpu_info, text="GPU")
book.add(ram_info, text="RAM")
book.add(disks_info, text="DISK")

# ОС информация
canvas_os = tk.Canvas(OS_info, bg='black', highlightthickness=0)
canvas_os.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(OS_info, orient=tk.VERTICAL, command=canvas_os.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_os.configure(yscrollcommand=my_scrollbar.set)

uname = platform.uname()
canvas_os.create_text(50, 10, text=f"System: {uname.system}", fill="white", font=("Helvetica", 12))  # увеличиваем шрифт
canvas_os.create_text(87, 30, text=f"Node name: {uname.node}", fill="white", font=("Helvetica", 12))
canvas_os.create_text(32, 50, text=f"Release: {uname.release}", fill="white", font=("Helvetica", 12))
canvas_os.create_text(53, 70, text=f"Version: {uname.version}", fill="white", font=("Helvetica", 12))
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
canvas_os.create_text(80, 90, text=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}", fill="white", font=("Helvetica", 12))

# CPU информация
canvas_cpu = tk.Canvas(cpu_info, bg='black', highlightthickness=0)
canvas_cpu.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(cpu_info, orient=tk.VERTICAL, command=canvas_cpu.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_cpu.configure(yscrollcommand=my_scrollbar.set)

cpufreq = psutil.cpu_freq()
canvas_cpu.create_text(50, 10, text=f"Physical cores: {psutil.cpu_count(logical=False)}", fill="white", font=("Helvetica", 12))
canvas_cpu.create_text(40, 30, text=f"Total cores: {psutil.cpu_count(logical=True)}", fill="white", font=("Helvetica", 12))
canvas_cpu.create_text(50, 50, text=f"Max Frequency: {cpufreq.max:.2f}Mhz", fill="white", font=("Helvetica", 12))
cpu_usage_id = canvas_cpu.create_text(60, 70, text=f"Total CPU Usage: {psutil.cpu_percent()}%", fill="white", font=("Helvetica", 12))

# Попытка получить температуру CPU
try:
    temps = psutil.sensors_temperatures()
    if 'coretemp' in temps:
        cpu_temp = temps['coretemp'][0].current
        canvas_cpu.create_text(50, 90, text=f"CPU Temperature: {cpu_temp} °C", fill="white", font=("Helvetica", 12))
    else:
        canvas_cpu.create_text(50, 90, text="CPU Temperature: N/A", fill="white", font=("Helvetica", 12))
except AttributeError:
    canvas_cpu.create_text(50, 90, text="CPU Temperature: Not supported", fill="white", font=("Helvetica", 12))

# GPU информация
canvas_gpu = tk.Canvas(gpu_info, bg='black', highlightthickness=0)
canvas_gpu.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(gpu_info, orient=tk.VERTICAL, command=canvas_gpu.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_gpu.configure(yscrollcommand=my_scrollbar.set)

gpus = GPUtil.getGPUs()
gpu_text_ids = []
y_gpu = 10
for gpu in gpus:
    canvas_gpu.create_text(110, y_gpu, text=f"GPU name: {gpu.name}", fill="white", font=("Helvetica", 12))
    y_gpu += 20
    canvas_gpu.create_text(70, y_gpu, text=f"Total memory: {gpu.memoryTotal}MB", fill="white", font=("Helvetica", 12))
    y_gpu += 20
    load_id = canvas_gpu.create_text(110, y_gpu, text=f"Load: {gpu.load*100:.1f}%", fill="white", font=("Helvetica", 12))
    y_gpu += 20
    temp_id = canvas_gpu.create_text(110, y_gpu, text=f"Temperature: {gpu.temperature} °C", fill="white", font=("Helvetica", 12))
    y_gpu += 20
    canvas_gpu.create_text(142, y_gpu, text=f"UUID: {gpu.uuid}", fill="white", font=("Helvetica", 12))
    y_gpu += 40
    gpu_text_ids.append((load_id, temp_id))

# RAM информация
canvas_ram = tk.Canvas(ram_info, bg='black', highlightthickness=0)
canvas_ram.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(ram_info, orient=tk.VERTICAL, command=canvas_ram.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_ram.configure(yscrollcommand=my_scrollbar.set)

svmem = psutil.virtual_memory()
canvas_ram.create_text(40, 10, text=f"Total: {get_size(svmem.total)}", fill="white", font=("Helvetica", 12))
canvas_ram.create_text(50, 30, text=f"Available: {get_size(svmem.available)}", fill="white", font=("Helvetica", 12))
canvas_ram.create_text(40, 50, text=f"Used: {get_size(svmem.used)}", fill="white", font=("Helvetica", 12))

# Диски информация
canvas_disk = tk.Canvas(disks_info, bg='black', highlightthickness=0)
canvas_disk.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(disks_info, orient=tk.VERTICAL, command=canvas_disk.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_disk.configure(yscrollcommand=my_scrollbar.set)

height_disk_canvas = 10
partitions = psutil.disk_partitions()
for partition in partitions:
    canvas_disk.create_text(50, height_disk_canvas, text=f"=== Device: {partition.device} ===", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20
    canvas_disk.create_text(50, height_disk_canvas, text=f"  Mountpoint: {partition.mountpoint}", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20
    canvas_disk.create_text(60, height_disk_canvas, text=f"  File system type: {partition.fstype}", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20
    partition_usage = psutil.disk_usage(partition.mountpoint)
    canvas_disk.create_text(50, height_disk_canvas, text=f"  Total Size: {get_size(partition_usage.total)}", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20
    canvas_disk.create_text(50, height_disk_canvas, text=f"  Used: {get_size(partition_usage.used)}", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20
    canvas_disk.create_text(50, height_disk_canvas, text=f"  Free: {get_size(partition_usage.free)}", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20
    canvas_disk.create_text(50, height_disk_canvas, text=f"  Percentage: {partition_usage.percent}%", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20
    disk_io = psutil.disk_io_counters()
    canvas_disk.create_text(60, height_disk_canvas, text=f"Total read: {get_size(disk_io.read_bytes)}", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20
    canvas_disk.create_text(60, height_disk_canvas, text=f"Total write: {get_size(disk_io.write_bytes)}", fill="white", font=("Helvetica", 12))
    height_disk_canvas += 20

# Функции обновления
def update_cpu():
    usage = psutil.cpu_percent()
    canvas_cpu.itemconfig(cpu_usage_id, text=f"Total CPU Usage: {usage}%", fill="white")
    root.after(1000, update_cpu)

def update_gpu():
    gpus = GPUtil.getGPUs()
    for i, gpu in enumerate(gpus):
        if i < len(gpu_text_ids):
            load_id, temp_id = gpu_text_ids[i]
            canvas_gpu.itemconfig(load_id, text=f"Load: {gpu.load*100:.1f}%", fill="white")
            canvas_gpu.itemconfig(temp_id, text=f"Temperature: {gpu.temperature} °C", fill="white")
    root.after(1000, update_gpu)

update_cpu()
update_gpu()

root.mainloop()
