import socket
import tkinter as tk
import sys
from pathlib import Path
import importlib

print("Программа запущена.")
     
try:
    # Создаем клиентский сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)  # Устанавливаем тайм-аут
    client_socket.connect(('85.250.190.197', 25565))  # Подключаемся к серверу
    print("Сокет успешно подключен.")

    # Отправляем сообщение серверу
    message = "Привет, сервер!"
    client_socket.sendall(message.encode())
    print("Сообщение отправлено серверу.")
except Exception as e:
    print(f"Ошибка при подключении сокета: {e}")
    input("Нажмите Enter для завершения...")
    sys.exit(1)
finally:
    # Закрываем сокет
    client_socket.close()
    print("Клиент завершил работу.")   

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
    module_name = "svg"  # Замените "svg" на точное имя вашего файла в папке boots

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