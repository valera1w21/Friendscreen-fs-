import socket
import sys
import tkinter as tk
import sys

print("Программа запущена.")
# Настройка пути
sys.path.append(r"C:\Users\вал\Desktop\Friendscreen (fs)\fundserver\boots")
print("Путь добавлен.")
try:
    from svg import ScreenViewerApp
    print("Класс импортирован.")
    
    # Создаем и запускаем приложение
    root = tk.Tk()
    print("Создано окно tkinter.")
    app = ScreenViewerApp(root)
    print("Запуск mainloop...")
    root.mainloop()
except Exception as e:
    print(f"Произошла ошибка: {e}")
    input("Нажмите Enter для завершения...")

# Настройка клиентского сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(5)  # Установим тайм-аут для операций с сокетом
client_socket.connect(('localhost', 25565))  # IP и порт сервера

# Создание Tkinter окна
root = tk.Tk()
root.mainloop()