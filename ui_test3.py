import tkinter as tk
from tkinter import ttk
import psutil
import platform
import GPUtil
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# Загружаем настройки из файла settings.txt (если файла нет, используются значения по умолчанию)
def load_settings():
    settings = {
        "bg": "black",
        "fg": "white",
        "font_size": "12",
        "graph_bg": "black",
        "graph_line": "lime"
    }
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
def save_settings(bg, fg, font_size, graph_bg, graph_line):
    with open("settings.txt", "w") as f:
        f.write(f"bg={bg}\n")
        f.write(f"fg={fg}\n")
        f.write(f"font_size={font_size}\n")
        f.write(f"graph_bg={graph_bg}\n")
        f.write(f"graph_line={graph_line}\n")

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
    settings_win.geometry("300x350")
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

    tk.Label(settings_win, text="Graph BG (hex):", bg="gray20", fg="white", font=("Helvetica", 10)).pack(pady=5)
    graph_bg_entry = tk.Entry(settings_win, font=("Helvetica", 10))
    graph_bg_entry.pack(pady=5)
    graph_bg_entry.insert(0, current_graph_bg)

    tk.Label(settings_win, text="Graph Line Color (hex):", bg="gray20", fg="white", font=("Helvetica", 10)).pack(pady=5)
    graph_line_entry = tk.Entry(settings_win, font=("Helvetica", 10))
    graph_line_entry.pack(pady=5)
    graph_line_entry.insert(0, current_graph_line)

    def apply_settings():
        new_bg = bg_entry.get()
        new_fg = fg_entry.get()
        try:
            new_font_size = int(font_size_entry.get())
        except ValueError:
            new_font_size = 12
        new_font = ("Helvetica", new_font_size)
        new_graph_bg = graph_bg_entry.get()
        new_graph_line = graph_line_entry.get()

        root.configure(bg=new_bg)
        update_theme(main_frame, new_bg, new_fg, new_font)
        # Обновляем графики:
        cpu_ax.set_facecolor(new_graph_bg)
        cpu_line.set_color(new_graph_line)
        cpu_ax.set_title("CPU Usage", color=new_fg, fontsize=new_font_size)
        cpu_ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
        cpu_canvas.draw()

        ram_ax.set_facecolor(new_graph_bg)
        ram_line.set_color(new_graph_line)
        ram_ax.set_title("RAM Usage", color=new_fg, fontsize=new_font_size)
        ram_ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
        ram_canvas.draw()

        if gpu_list_global:
            gpu_ax.set_facecolor(new_graph_bg)
            gpu_line.set_color(new_graph_line)
            gpu_ax.set_title("GPU Load", color=new_fg, fontsize=new_font_size)
            gpu_ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
            gpu_canvas.draw()

        global current_fg, current_font_size, current_graph_bg, current_graph_line
        current_fg = new_fg
        current_font_size = new_font_size
        current_graph_bg = new_graph_bg
        current_graph_line = new_graph_line

        save_settings(new_bg, new_fg, new_font_size, new_graph_bg, new_graph_line)
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
current_graph_bg = settings.get("graph_bg", "black")
current_graph_line = settings.get("graph_line", "lime")

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
os_frame = tk.LabelFrame(main_frame, text="OS Information", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))
cpu_frame = tk.LabelFrame(main_frame, text="CPU Information", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))
gpu_frame = tk.LabelFrame(main_frame, text="GPU Information", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))
ram_frame = tk.LabelFrame(main_frame, text="RAM Information", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))
disk_frame = tk.LabelFrame(main_frame, text="Disk Information", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))

os_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
cpu_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
gpu_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
ram_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
disk_frame.grid(row=2, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)

# --- OS Information ---
uname = platform.uname()
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
tk.Label(os_frame, text=f"System: {uname.system}", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)
tk.Label(os_frame, text=f"Node name: {uname.node}", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)
tk.Label(os_frame, text=f"Release: {uname.release}", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)
tk.Label(os_frame, text=f"Version: {uname.version}", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)
tk.Label(os_frame, text=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}",
         bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)

# --- CPU Information ---
cpufreq = psutil.cpu_freq()
cpu_cores = psutil.cpu_count(logical=False)
total_cores = psutil.cpu_count(logical=True)
cpu_usage_value = psutil.cpu_percent(interval=1)
cpu_name = platform.processor()  # Получаем имя процессора

# Создаем два внутренних фрейма: данные слева, график справа
cpu_data_frame = tk.Frame(cpu_frame, bg=current_bg)
cpu_graph_frame = tk.Frame(cpu_frame, bg=current_bg)
cpu_data_frame.pack(side="left", fill="both", expand=True)
cpu_graph_frame.pack(side="right", fill="both", expand=True)

# Добавляем имя процессора
tk.Label(cpu_data_frame, text=f"CPU Name: {cpu_name}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)

tk.Label(cpu_data_frame, text=f"Physical cores: {cpu_cores}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)
tk.Label(cpu_data_frame, text=f"Total cores: {total_cores}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)
tk.Label(cpu_data_frame, text=f"Max Frequency: {cpufreq.max:.2f} Mhz", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)
cpu_usage_label = tk.Label(cpu_data_frame, text=f"Total CPU Usage: {cpu_usage_value}%", bg=current_bg, fg=current_fg,
                           font=("Helvetica", current_font_size))
cpu_usage_label.pack(anchor="w", padx=5, pady=3)
try:
    temps = psutil.sensors_temperatures()
    if 'coretemp' in temps:
        cpu_temp = temps['coretemp'][0].current
        cpu_temp_label = tk.Label(cpu_data_frame, text=f"CPU Temperature: {cpu_temp} °C", bg=current_bg, fg=current_fg,
                                  font=("Helvetica", current_font_size))
    else:
        cpu_temp_label = tk.Label(cpu_data_frame, text="CPU Temperature: N/A", bg=current_bg, fg=current_fg,
                                  font=("Helvetica", current_font_size))
except AttributeError:
    cpu_temp_label = tk.Label(cpu_data_frame, text="CPU Temperature: Not supported", bg=current_bg, fg=current_fg,
                              font=("Helvetica", current_font_size))
cpu_temp_label.pack(anchor="w", padx=5, pady=3)

# График CPU (в cpu_graph_frame)
cpu_history = []
cpu_fig = plt.Figure(figsize=(3,2), dpi=100)
cpu_ax = cpu_fig.add_subplot(111)
cpu_ax.set_ylim(0, 100)
cpu_line, = cpu_ax.plot([], [], color=current_graph_line)
cpu_ax.set_facecolor(current_graph_bg)
cpu_ax.set_title("CPU Usage", color=current_fg, fontsize=current_font_size)
# Убираем нижнюю разметку оси X:
cpu_ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
cpu_canvas = FigureCanvasTkAgg(cpu_fig, master=cpu_graph_frame)
cpu_canvas.get_tk_widget().pack(anchor="w", padx=5, pady=5)

# --- GPU Information ---
gpu_list_global = GPUtil.getGPUs()
gpu_load_labels = []  # для динамического обновления загрузки GPU
gpu_temp_labels = []  # для динамического обновления температуры GPU

# Создаем два внутренних фрейма: данные слева, график справа
gpu_data_frame = tk.Frame(gpu_frame, bg=current_bg)
gpu_graph_frame = tk.Frame(gpu_frame, bg=current_bg)
gpu_data_frame.pack(side="left", fill="both", expand=True)
gpu_graph_frame.pack(side="right", fill="both", expand=True)

if gpu_list_global:
    for gpu in gpu_list_global:
        tk.Label(gpu_data_frame, text=f"GPU name: {gpu.name}", bg=current_bg, fg=current_fg,
                 font=("Helvetica", current_font_size))\
            .pack(anchor="w", padx=5, pady=3)
        tk.Label(gpu_data_frame, text=f"Total memory: {gpu.memoryTotal} MB", bg=current_bg, fg=current_fg,
                 font=("Helvetica", current_font_size))\
            .pack(anchor="w", padx=5, pady=3)
        load_label = tk.Label(gpu_data_frame, text=f"Load: {gpu.load * 100:.1f}%", bg=current_bg, fg=current_fg,
                              font=("Helvetica", current_font_size))
        load_label.pack(anchor="w", padx=5, pady=3)
        gpu_load_labels.append(load_label)
        temp_label = tk.Label(gpu_data_frame, text=f"Temperature: {gpu.temperature} °C", bg=current_bg, fg=current_fg,
                              font=("Helvetica", current_font_size))
        temp_label.pack(anchor="w", padx=5, pady=3)
        gpu_temp_labels.append(temp_label)
        # tk.Label(gpu_data_frame, text=f"UUID: {gpu.uuid}", bg=current_bg, fg=current_fg,
        #          font=("Helvetica", current_font_size))\
        #     .pack(anchor="w", padx=5, pady=3)
        tk.Label(gpu_data_frame, text="----------------------", bg=current_bg, fg=current_fg,
                 font=("Helvetica", current_font_size))\
            .pack(anchor="w", padx=5, pady=3)
else:
    tk.Label(gpu_data_frame, text="No GPU found", bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size))\
        .pack(anchor="w", padx=5, pady=3)

# График GPU (в gpu_graph_frame, используется первая GPU)
if gpu_list_global:
    gpu_history = []
    gpu_fig = plt.Figure(figsize=(3,2), dpi=100)
    gpu_ax = gpu_fig.add_subplot(111)
    gpu_ax.set_ylim(0, 100)
    gpu_line, = gpu_ax.plot([], [], color=current_graph_line)
    gpu_ax.set_facecolor(current_graph_bg)
    gpu_ax.set_title("GPU Load", color=current_fg, fontsize=current_font_size)
    gpu_ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
    gpu_canvas = FigureCanvasTkAgg(gpu_fig, master=gpu_graph_frame)
    gpu_canvas.get_tk_widget().pack(anchor="w", padx=5, pady=5)

# --- RAM Information ---
svmem = psutil.virtual_memory()

# Создаем два внутренних фреймов: данные слева, график справа
ram_data_frame = tk.Frame(ram_frame, bg=current_bg)
ram_graph_frame = tk.Frame(ram_frame, bg=current_bg)
ram_data_frame.pack(side="left", fill="both", expand=True)
ram_graph_frame.pack(side="right", fill="both", expand=True)

tk.Label(ram_data_frame, text=f"Total RAM: {get_size(svmem.total)}", bg=current_bg, fg=current_fg,
         font=("Helvetica", current_font_size))\
    .pack(anchor="w", padx=5, pady=3)
ram_available_label = tk.Label(ram_data_frame, text=f"Available RAM: {get_size(svmem.available)}", bg=current_bg,
                               fg=current_fg, font=("Helvetica", current_font_size))
ram_available_label.pack(anchor="w", padx=5, pady=3)
ram_used_label = tk.Label(ram_data_frame, text=f"Used RAM: {get_size(svmem.used)}", bg=current_bg, fg=current_fg,
                          font=("Helvetica", current_font_size))
ram_used_label.pack(anchor="w", padx=5, pady=3)
ram_usage_label = tk.Label(ram_data_frame, text=f"RAM Usage: {svmem.percent}%", bg=current_bg, fg=current_fg,
                           font=("Helvetica", current_font_size))
ram_usage_label.pack(anchor="w", padx=5, pady=3)

# График RAM (в ram_graph_frame)
ram_history = []
ram_fig = plt.Figure(figsize=(3,2), dpi=100)
ram_ax = ram_fig.add_subplot(111)
ram_ax.set_ylim(0, 100)
ram_line, = ram_ax.plot([], [], color=current_graph_line)
ram_ax.set_facecolor(current_graph_bg)
ram_ax.set_title("RAM Usage", color=current_fg, fontsize=current_font_size)
ram_ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
ram_canvas = FigureCanvasTkAgg(ram_fig, master=ram_graph_frame)
ram_canvas.get_tk_widget().pack(anchor="w", padx=5, pady=5)

# --- Disk Information ---
partitions = psutil.disk_partitions()
# Очищаем диск-фрейм, если требуется (если обновляем динамически)
for idx, partition in enumerate(partitions):
    # Создаем отдельный фрейм для каждого диска (столбец)
    disk_subframe = tk.Frame(disk_frame, bg=current_bg)
    # Размещаем фрейм в строке 0, в столбце idx
    disk_subframe.grid(row=0, column=idx, sticky="nsew", padx=5, pady=5)
    # Задаем равномерное распределение столбцов в disk_frame
    disk_frame.columnconfigure(idx, weight=1)

    tk.Label(disk_subframe, text=f"=== Device: {partition.device} ===",
             bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_subframe, text=f"Mountpoint: {partition.mountpoint}",
             bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_subframe, text=f"File system type: {partition.fstype}",
             bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)

    partition_usage = psutil.disk_usage(partition.mountpoint)
    tk.Label(disk_subframe, text=f"Total Size: {get_size(partition_usage.total)}",
             bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_subframe, text=f"Used: {get_size(partition_usage.used)}",
             bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_subframe, text=f"Free: {get_size(partition_usage.free)}",
             bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)
    tk.Label(disk_subframe, text=f"Percentage: {partition_usage.percent}%",
             bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
        .pack(anchor="w", padx=5, pady=3)

    # Получаем информацию по I/O для каждого диска (используя параметр perdisk=True)
    io_counters = psutil.disk_io_counters(perdisk=True)
    if partition.device in io_counters:
        d_io = io_counters[partition.device]
        tk.Label(disk_subframe, text=f"Total read: {get_size(d_io.read_bytes)}",
                 bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
            .pack(anchor="w", padx=5, pady=3)
        tk.Label(disk_subframe, text=f"Total write: {get_size(d_io.write_bytes)}",
                 bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
            .pack(anchor="w", padx=5, pady=3)
    # tk.Label(disk_subframe, text="----------------------",
    #          bg=current_bg, fg=current_fg, font=("Helvetica", current_font_size)) \
    #     .pack(anchor="w", padx=5, pady=3)


# Функция динамического обновления статистики и графиков
def update_stats():
    # CPU
    cpu_usage_val = psutil.cpu_percent(interval=0)
    cpu_usage_label.config(text=f"Total CPU Usage: {cpu_usage_val}%")
    cpu_history.append(cpu_usage_val)
    if len(cpu_history) > 60:
        cpu_history.pop(0)
    cpu_line.set_data(range(len(cpu_history)), cpu_history)
    cpu_ax.set_xlim(0, max(60, len(cpu_history)))
    cpu_canvas.draw()

    # RAM
    svmem = psutil.virtual_memory()
    ram_available_label.config(text=f"Available RAM: {get_size(svmem.available)}")
    ram_used_label.config(text=f"Used RAM: {get_size(svmem.used)}")
    ram_usage_label.config(text=f"RAM Usage: {svmem.percent}%")
    ram_val = svmem.percent
    ram_history.append(ram_val)
    if len(ram_history) > 60:
        ram_history.pop(0)
    ram_line.set_data(range(len(ram_history)), ram_history)
    ram_ax.set_xlim(0, max(60, len(ram_history)))
    ram_canvas.draw()

    # GPU
    gpus = GPUtil.getGPUs()
    for i, gpu in enumerate(gpus):
        if i < len(gpu_load_labels):
            gpu_load_labels[i].config(text=f"Load: {gpu.load * 100:.1f}%")
        if i < len(gpu_temp_labels):
            gpu_temp_labels[i].config(text=f"Temperature: {gpu.temperature} °C")
    if gpu_list_global:
        gpu_val = gpus[0].load * 100 if gpus else 0
        global gpu_history
        if 'gpu_history' not in globals():
            gpu_history = []
        gpu_history.append(gpu_val)
        if len(gpu_history) > 60:
            gpu_history.pop(0)
        gpu_line.set_data(range(len(gpu_history)), gpu_history)
        gpu_ax.set_xlim(0, max(60, len(gpu_history)))
        gpu_canvas.draw()

    root.after(1000, update_stats)

update_stats()
root.mainloop()

# чтобы скомпилить файл
# pyinstaller --onefile --add-data "settings.txt;." pc_info.py