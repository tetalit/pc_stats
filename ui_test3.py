import tkinter as tk
from tkinter import ttk
import psutil
import platform
import GPUtil
from datetime import datetime


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# Загружаем настройки из файла settings.txt (если файла нет, используются значения по умолчанию)
def load_settings():
    settings = {"bg": "black", "fg": "white", "font_size": "12"}
    try:
        with open("settings.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if '=' in line:
                    key, value = line.split("=", 1)
                    settings[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return settings


# Сохраняем настройки в файл settings.txt
def save_settings(bg, fg, font_size):
    with open("settings.txt", "w") as f:
        f.write(f"bg={bg}\n")
        f.write(f"fg={fg}\n")
        f.write(f"font_size={font_size}\n")


# Рекурсивное обновление темы для виджетов
def update_theme(widget, bg, fg, font):
    try:
        widget.configure(bg=bg)
    except:
        pass
    if isinstance(widget, (tk.Label, tk.LabelFrame, tk.Button)):
        widget.configure(bg=bg, fg=fg, font=font)
    for child in widget.winfo_children():
        update_theme(child, bg, fg, font)


# Окно настроек
def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("300x300")
    settings_win.configure(bg="gray20")

    tk.Label(settings_win, text="Background (hex):", bg="gray20", fg="white", font=("Helvetica", 10)).pack(pady=5)
    bg_entry = tk.Entry(settings_win, font=("Helvetica", 10))
    bg_entry.pack(pady=5)
    bg_entry.insert(0, root.cget("bg"))

    tk.Label(settings_win, text="Font Color (hex):", bg="gray20", fg="white", font=("Helvetica", 10)).pack(pady=5)
    fg_entry = tk.Entry(settings_win, font=("Helvetica", 10))
    fg_entry.pack(pady=5)
    fg_entry.insert(0, current_fg)

    tk.Label(settings_win, text="Font Size:", bg="gray20", fg="white", font=("Helvetica", 10)).pack(pady=5)
    font_size_entry = tk.Entry(settings_win, font=("Helvetica", 10))
    font_size_entry.pack(pady=5)
    font_size_entry.insert(0, current_font_size)

    def apply_settings():
        new_bg = bg_entry.get()
        new_fg = fg_entry.get()
        try:
            new_font_size = int(font_size_entry.get())
        except ValueError:
            new_font_size = 12
        new_font = ("Helvetica", new_font_size)
        root.configure(bg=new_bg)
        update_theme(main_frame, new_bg, new_fg, new_font)
        # Обновляем глобальные переменные для использования в окне настроек
        global current_fg, current_font_size
        current_fg = new_fg
        current_font_size = new_font_size
        save_settings(new_bg, new_fg, new_font_size)
        settings_win.destroy()

    tk.Button(settings_win, text="Apply", command=apply_settings, font=("Helvetica", 10)).pack(pady=10)
    settings_win.grab_set()  # делаем окно модальным


# Загружаем настройки при запуске
settings = load_settings()
current_bg = settings.get("bg", "black")
current_fg = settings.get("fg", "white")
try:
    current_font_size = int(settings.get("font_size", "12"))
except ValueError:
    current_font_size = 12
current_font = ("Helvetica", current_font_size)

# Основное окно приложения
root = tk.Tk()
root.title("PC Info")
root.geometry("1200x800")
root.configure(bg=current_bg)

# Кнопка настроек в левом верхнем углу
settings_button = tk.Button(root, text="Settings", command=open_settings, font=("Helvetica", current_font_size))
settings_button.pack(anchor="nw", padx=10, pady=10)

# Главный фрейм с адаптивной сеткой для разделов
main_frame = tk.Frame(root, bg=current_bg)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
main_frame.columnconfigure(0, weight=1, uniform="col")
main_frame.columnconfigure(1, weight=1, uniform="col")
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)

# Создаем LabelFrame для каждого раздела
os_frame = tk.LabelFrame(main_frame, text="OS Information", bg=current_bg, fg=current_fg,
                         font=("Helvetica", current_font_size))
cpu_frame = tk.LabelFrame(main_frame, text="CPU Information", bg=current_bg, fg=current_fg,
                          font=("Helvetica", current_font_size))
gpu_frame = tk.LabelFrame(main_frame, text="GPU Information", bg=current_bg, fg=current_fg,
                          font=("Helvetica", current_font_size))
ram_frame = tk.LabelFrame(main_frame, text="RAM Information", bg=current_bg, fg=current_fg,
                          font=("Helvetica", current_font_size))
disk_frame = tk.LabelFrame(main_frame, text="Disk Information", bg=current_bg, fg=current_fg,
                           font=("Helvetica", current_font_size))

os_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
cpu_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
gpu_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
ram_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
disk_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

# --- OS Information ---
uname = platform.uname()
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
tk.Label(os_frame, text=f"System: {uname.system}", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)
tk.Label(os_frame, text=f"Node name: {uname.node}", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)
tk.Label(os_frame, text=f"Release: {uname.release}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)
tk.Label(os_frame, text=f"Version: {uname.version}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)
tk.Label(os_frame, text=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}",
         bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)

# --- CPU Information ---
cpufreq = psutil.cpu_freq()
cpu_cores = psutil.cpu_count(logical=False)
total_cores = psutil.cpu_count(logical=True)
cpu_usage_value = psutil.cpu_percent(interval=1)
tk.Label(cpu_frame, text=f"Physical cores: {cpu_cores}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)
tk.Label(cpu_frame, text=f"Total cores: {total_cores}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)
tk.Label(cpu_frame, text=f"Max Frequency: {cpufreq.max:.2f} Mhz", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)
cpu_usage_label = tk.Label(cpu_frame, text=f"Total CPU Usage: {cpu_usage_value}%", bg=current_bg, fg=current_fg,
                           font=("Helvetica", current_font_size))
cpu_usage_label.pack(anchor="w", padx=5, pady=3)
try:
    temps = psutil.sensors_temperatures()
    if 'coretemp' in temps:
        cpu_temp = temps['coretemp'][0].current
        cpu_temp_label = tk.Label(cpu_frame, text=f"CPU Temperature: {cpu_temp} °C", bg=current_bg, fg=current_fg,
                                  font=("Helvetica", current_font_size))
    else:
        cpu_temp_label = tk.Label(cpu_frame, text="CPU Temperature: N/A", bg=current_bg, fg=current_fg,
                                  font=("Helvetica", current_font_size))
except AttributeError:
    cpu_temp_label = tk.Label(cpu_frame, text="CPU Temperature: Not supported", bg=current_bg, fg=current_fg,
                              font=("Helvetica", current_font_size))
cpu_temp_label.pack(anchor="w", padx=5, pady=3)

# --- GPU Information ---
gpu_list = GPUtil.getGPUs()
gpu_load_labels = []  # для динамического обновления загрузки GPU
gpu_temp_labels = []  # для динамического обновления температуры GPU
if gpu_list:
    for gpu in gpu_list:
        tk.Label(gpu_frame, text=f"GPU name: {gpu.name}", bg=current_bg, fg=current_fg,
                 font=("Helvetica", current_font_size)) \
            .pack(anchor="w", padx=5, pady=3)
        tk.Label(gpu_frame, text=f"Total memory: {gpu.memoryTotal} MB", bg=current_bg, fg=current_fg,
                 font=("Helvetica", current_font_size)) \
            .pack(anchor="w", padx=5, pady=3)
        load_label = tk.Label(gpu_frame, text=f"Load: {gpu.load * 100:.1f}%", bg=current_bg, fg=current_fg,
                              font=("Helvetica", current_font_size))
        load_label.pack(anchor="w", padx=5, pady=3)
        gpu_load_labels.append(load_label)
        temp_label = tk.Label(gpu_frame, text=f"Temperature: {gpu.temperature} °C", bg=current_bg, fg=current_fg,
                              font=("Helvetica", current_font_size))
        temp_label.pack(anchor="w", padx=5, pady=3)
        gpu_temp_labels.append(temp_label)
        tk.Label(gpu_frame, text=f"UUID: {gpu.uuid}", bg=current_bg, fg=current_fg,
                 font=("Helvetica", current_font_size)) \
            .pack(anchor="w", padx=5, pady=3)
        tk.Label(gpu_frame, text="----------------------", bg=current_bg, fg=current_fg,
                 font=("Helvetica", current_font_size)) \
            .pack(anchor="w", padx=5, pady=3)
else:
    tk.Label(gpu_frame, text="No GPU found", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)

# --- RAM Information ---
svmem = psutil.virtual_memory()
tk.Label(ram_frame, text=f"Total RAM: {get_size(svmem.total)}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size)) \
    .pack(anchor="w", padx=5, pady=3)
ram_available_label = tk.Label(ram_frame, text=f"Available RAM: {get_size(svmem.available)}", bg=current_bg,
                               fg=current_fg, font=("Helvetica", current_font_size))
ram_available_label.pack(anchor="w", padx=5, pady=3)
ram_used_label = tk.Label(ram_frame, text=f"Used RAM: {get_size(svmem.used)}", bg=current_bg, fg=current_fg,
                          font=("Helvetica", current_font_size))
ram_used_label.pack(anchor="w", padx=5, pady=3)
ram_usage_label = tk.Label(ram_frame, text=f"RAM Usage: {svmem.percent}%", bg=current_bg, fg=current_fg,
                           font=("Helvetica", current_font_size))
ram_usage_label.pack(anchor="w", padx=5, pady=3)

# --- Disk Information ---
partitions = psutil.disk_partitions()
for partition in partitions:
    tk.Label(disk_frame, text=f"=== Device: {partition.device} ===", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_frame, text=f"Mountpoint: {partition.mountpoint}", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_frame, text=f"File system type: {partition.fstype}", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    partition_usage = psutil.disk_usage(partition.mountpoint)
    tk.Label(disk_frame, text=f"Total Size: {get_size(partition_usage.total)}", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_frame, text=f"Used: {get_size(partition_usage.used)}", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_frame, text=f"Free: {get_size(partition_usage.free)}", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_frame, text=f"Percentage: {partition_usage.percent}%", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    disk_io = psutil.disk_io_counters()
    tk.Label(disk_frame, text=f"Total read: {get_size(disk_io.read_bytes)}", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_frame, text=f"Total write: {get_size(disk_io.write_bytes)}", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_frame, text="----------------------", bg=current_bg, fg=current_fg,
             font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)


# Функция динамического обновления статистики
def update_stats():
    cpu_usage_val = psutil.cpu_percent(interval=0)
    cpu_usage_label.config(text=f"Total CPU Usage: {cpu_usage_val}%")

    gpus = GPUtil.getGPUs()
    for i, gpu in enumerate(gpus):
        if i < len(gpu_load_labels):
            gpu_load_labels[i].config(text=f"Load: {gpu.load * 100:.1f}%")
        if i < len(gpu_temp_labels):
            gpu_temp_labels[i].config(text=f"Temperature: {gpu.temperature} °C")

    svmem = psutil.virtual_memory()
    ram_available_label.config(text=f"Available RAM: {get_size(svmem.available)}")
    ram_used_label.config(text=f"Used RAM: {get_size(svmem.used)}")
    ram_usage_label.config(text=f"RAM Usage: {svmem.percent}%")

    root.after(1000, update_stats)


update_stats()
root.mainloop()
