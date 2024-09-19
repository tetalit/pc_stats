import psutil
import time
def monitor_resources(interval=1):
    try:
        while True:
            cpu_percent = psutil.cpu_percent(interval=interval)

            memory_info = psutil.virtual_memory()

            disk_info = psutil.disk_usage("/")

            print(f"CPU: {cpu_percent}%")
            print(f"Память: {memory_info.percent}% используется")
            print(f"Диск: {disk_info.percent}% занято")
            print("-" * 30)

            time.sleep(interval)

    except KeyboardInterrupt:
        print("Мониторинг завершен.")


monitor_resources()