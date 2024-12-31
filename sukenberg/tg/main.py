# import os

# # Укажите путь к папке с файлами
# folder_path = 'data/photos'

# # Получаем список файлов в папке
# files = os.listdir(folder_path)
# # Переименовываем файлы
# for index, file in enumerate(files, start=1):
#     # Получаем расширение файла
#     file_extension = os.path.splitext(file)[1]
    
#     # Формируем новое имя файла
#     new_name = f"{index}{file_extension}"
    
#     # Полные пути к старому и новому именам
#     old_file_path = os.path.join(folder_path, file)
#     new_file_path = os.path.join(folder_path, new_name)
    
#     # Переименовываем файл
#     os.rename(old_file_path, new_file_path)

# print("Файлы успешно переименованы.")

import pyautogui as gui
import socket


def  restart():
    gui.hotkey('ctrl', 'shift','f5')


# Создаем объект сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_address = (socket.gethostbyname(socket.gethostname()), 12333)  # Используйте реальный IP вашего ноутбука
print(socket.gethostbyname(socket.gethostname()))
server_socket.bind(server_address)

# Переходим в режим прослушивания
server_socket.listen()

print('Сервер запущен и ожидает подключения...')

try:
    while True:
        # Ожидаем подключение клиента
        connection, client_address = server_socket.accept()
        
        try:
            print(f'Подключен клиент: {client_address}')
            
            # Получаем данные от клиента
            data = connection.recv(1024).decode('utf-8')
            if not data:
                break
                
            print(f'Получено сообщение: {data}')
            if data == 'перезапуск':
                restart()

            # Отправляем ответ клиенту
            response = f'Вы отправили: {data}'
            connection.sendall(response.encode('utf-8'))

        finally:
            # Закрываем соединение
            connection.close()

except KeyboardInterrupt:
    pass

finally:
    # Закрываем сокет сервера
    server_socket.close()
