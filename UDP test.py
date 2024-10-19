import socket

# Создание UDP сокета
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Определение адреса и порта сервера
server_address = ('192.168.0.150', 12345)

# Данные для отправки
message = 'Привет, сервер!'.encode('utf-8')  # Кодируем строку в байты

try:
    # Отправка данных
    udp_socket.sendto(message, server_address)
    print(f'Сообщение отправлено: {message.decode("utf-8")}')  # Декодируем для вывода
finally:
    # Закрытие сокета
    udp_socket.close()
