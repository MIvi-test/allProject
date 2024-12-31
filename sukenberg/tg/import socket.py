import socket

# Создаем объект сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключение к серверу
server_address = ('192.168.0.100', 12333)  # Используйте реальный IP вашего ноутбука
client_socket.connect(server_address)

try:
    # Отправляем сообщение серверу
    message = input("Введите сообщение для отправки: ")
    client_socket.sendall(message.encode('utf-8'))
    
    # Получаем ответ от сервера
    response = client_socket.recv(1024).decode('utf-8')
    print(f'Ответ от сервера: {response}')

finally:
    # Закрываем соединение
    client_socket.close()

