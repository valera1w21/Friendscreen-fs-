import socket
import pyautogui
import io
import time
import struct
from PIL import Image

# Создаем сокет для сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 25565))  # Порт 25565
server_socket.listen(1)

print("Сервер ожидает подключение...")
client_socket, addr = server_socket.accept()
print(f"Подключен клиент: {addr}")

# Передаем изображение экрана
try:
    while True:
        # Захватываем экран
        screenshot = pyautogui.screenshot(region=(0, 0, 800, 600))

        # Сохраняем изображение в буфер
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')  # Сохраняем изображение в буфер
        img_byte_arr = img_byte_arr.getvalue()  # Получаем байтовое представление изображения

        # Отправляем размер данных перед изображением
        data_size = len(img_byte_arr)
        print(f"Размер данных для отправки: {data_size} байт")  # Отладочная информация

        # Отправляем размер данных в 4 байтах (используем struct для упаковки)
        client_socket.sendall(struct.pack('!I', data_size))  # !I — формат для целого числа в сети

        # Отправляем само изображение
        client_socket.sendall(img_byte_arr)

        # Задержка для предотвращения перегрузки
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Отключение...")
finally:
    client_socket.close()
    server_socket.close()
