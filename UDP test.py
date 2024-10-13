import socket

# Создание UDP сокета
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Определение адреса и порта сервера
server_address = ('127.0.0.1', 12345)

# Данные для отправки
message = b'Привет, сервер!'

try:
    # Отправка данных
    udp_socket.sendto(message, server_address)
    print(f'Сообщение отправлено: {message.decode()}')
finally:
    # Закрытие сокета
    udp_socket.close()
