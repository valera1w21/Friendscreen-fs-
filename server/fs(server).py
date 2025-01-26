import socket
import pyautogui
import io
import time
import struct
from PIL import Image
import sys
from pathlib import Path
import importlib

# Создаем сокет для сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Повторное использование порта
server_socket.bind(('10.100.102.23', 25565))  # Порт 25565
server_socket.listen(1)

print("Сервер ожидает подключение...")

try:
    # Принимаем подключение клиента
    client_socket, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")

    # Получаем первое сообщение от клиента
    data = client_socket.recv(1024)  # Ждем данных от клиента
    if data:
        print(f"Получено: {data.decode()}")
    else:
        print("Клиент отключился без отправки данных.")
except Exception as e:
    print(f"Ошибка на сервере: {e}")
finally:
    # Закрываем соединения
    client_socket.close()
    server_socket.close()
    print("Сервер завершил работу.")
# Начинаем передавать изображение
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

# Настройка пути
try:
    # Определяем домашний каталог пользователя
    user_home = Path.home()

    # Создаем путь к директории boots
    boots_path = user_home / "Desktop" / "Friendscreen (fs)" / "fundserver" / "boots"

    # Проверяем существование пути
    if not boots_path.exists():
        raise FileNotFoundError(f"Путь не существует: {boots_path}")

    # Добавляем путь в sys.path
    sys.path.append(str(boots_path))
    print(f"Путь добавлен: {boots_path}")

except Exception as e:
    print(f"Ошибка при настройке пути: {e}")
    input("Нажмите Enter для завершения...")
    sys.exit(1)

# Импортируем и запускаем Screen Viewer App
try:
    # Имя файла для импорта (без расширения .py)
    module_name = "dys"  # Замените "svg" на точное имя вашего файла в папке boots

    # Импортируем модуль
    screen_viewer_module = importlib.import_module(module_name)
    print(f"Модуль {module_name} успешно импортирован.")

    # Проверяем наличие функции main()
    if hasattr(screen_viewer_module, 'main'):
        # Запускаем функцию main()
        screen_viewer_module.main()
    else:
        print(f"Функция main() не найдена в модуле {module_name}.")
        input("Нажмите Enter для завершения...")
        sys.exit(1)

except Exception as e:
    print(f"Ошибка при запуске Screen Viewer App: {e}")
    input("Нажмите Enter для завершения...")
    sys.exit(1)

finally:
    # Закрываем сокеты
    client_socket.close()
    server_socket.close()
