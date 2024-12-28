import socket
import tkinter as tk
from PIL import Image, ImageTk
import io
import struct

class ScreenViewerApp:
    def __init__(self, root, client_socket):
        self.root = root
        self.client_socket = client_socket

        # Начальные размеры окна (будут динамически изменяться)
        self.width = 800
        self.height = 600

        # Флаг для полного экрана
        self.is_fullscreen = False

        # Устанавливаем иконку и имя программы
        #self.root.iconbitmap("your_icon.ico")  # Укажите путь к вашему файлу .ico
        self.root.title("Screen Viewer App")  # Имя программы

        # Устанавливаем фон для окна
        self.root.config(bg="lightgray")

        # Создаем холст для отображения изображения
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Создаем панель для кнопок
        self.control_frame = tk.Frame(root, bg="lightgray")
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Кнопка для выхода
        self.quit_button = tk.Button(self.control_frame, text="Выход", command=self.quit, bg="red", fg="white")
        self.quit_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопки для увеличения и уменьшения экрана
        self.zoom_in_button = tk.Button(self.control_frame, text="Увеличить", command=self.zoom_in, bg="blue", fg="white")
        self.zoom_in_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.zoom_out_button = tk.Button(self.control_frame, text="Уменьшить", command=self.zoom_out, bg="blue", fg="white")
        self.zoom_out_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для перехода в/выхода из полного экрана
        self.toggle_fullscreen_button = tk.Button(self.control_frame, text="Полный экран", command=self.toggle_fullscreen, bg="green", fg="white")
        self.toggle_fullscreen_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Поля ввода для изменения размера
        self.width_label = tk.Label(self.control_frame, text="Ширина:", bg="lightgray")
        self.width_label.pack(side=tk.LEFT, padx=5)
        self.width_entry = tk.Entry(self.control_frame)
        self.width_entry.insert(0, str(self.width))  # Вставляем текущее значение
        self.width_entry.pack(side=tk.LEFT, padx=5)

        self.height_label = tk.Label(self.control_frame, text="Высота:", bg="lightgray")
        self.height_label.pack(side=tk.LEFT, padx=5)
        self.height_entry = tk.Entry(self.control_frame)
        self.height_entry.insert(0, str(self.height))  # Вставляем текущее значение
        self.height_entry.pack(side=tk.LEFT, padx=5)

        self.set_size_button = tk.Button(self.control_frame, text="Изменить размер", command=self.change_size, bg="purple", fg="white")
        self.set_size_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Разрешаем изменение размера окна
        self.root.resizable(True, True)

        # Устанавливаем начальный размер окна
        self.root.geometry(f"{self.width}x{self.height}")

        # Начинаем обновление изображения
        self.update_image()

    def update_image(self):
        try:
            # Получаем размер данных изображения (4 байта)
            data_size_bytes = self.client_socket.recv(4)
            if len(data_size_bytes) < 4:
                print("Ошибка: не получен полный размер данных.")
                return

            # Преобразуем размер данных в целое число
            data_size = struct.unpack('!I', data_size_bytes)[0]

            # Получаем само изображение
            data = b""
            while len(data) < data_size:
                packet = self.client_socket.recv(min(4096, data_size - len(data)))
                if not packet:
                    print("Ошибка: не получены все данные изображения.")
                    return
                data += packet

            # Преобразуем байты в изображение
            image = Image.open(io.BytesIO(data))

            # Масштабируем изображение под размер окна
            image = image.resize((self.width, self.height - 50), Image.Resampling.LANCZOS)  # Уменьшаем на размер панели

            # Преобразуем изображение в формат, который может быть использован в Tkinter
            img_tk = ImageTk.PhotoImage(image)

            # Обновляем изображение на холсте
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

            # Сохраняем изображение в атрибуте, чтобы оно не было удалено сборщиком мусора
            self.canvas.image = img_tk

            # Повторить обновление через 100 мс
            self.root.after(100, self.update_image)

        except Exception as e:
            print(f"Ошибка при получении данных: {e}")

    def zoom_in(self):
        """Увеличение экрана"""
        # Увеличиваем размеры окна, но не панели управления
        self.width = int(self.width * 1.2)
        self.height = int(self.height * 1.2)

        # Обновляем размер окна
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Обновляем изображение
        self.update_image()

    def zoom_out(self):
        """Уменьшение экрана"""
        # Уменьшаем размеры окна, но не панели управления
        self.width = int(self.width * 0.8)
        self.height = int(self.height * 0.8)

        # Обновляем размер окна
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Обновляем изображение
        self.update_image()

    def change_size(self):
        """Изменение размера окна по введенным данным"""
        try:
            # Получаем новые размеры из полей ввода
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())

            # Устанавливаем новые размеры окна
            self.width = new_width
            self.height = new_height

            # Обновляем размер окна
            self.root.geometry(f"{self.width}x{self.height}")

            # Обновляем изображение
            self.update_image()

        except ValueError:
            print("Ошибка: введите правильные числовые значения для ширины и высоты.")

    def toggle_fullscreen(self):
        """Переключение между полным экраном и обычным режимом"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.root.attributes('-fullscreen', True)  # Переключаем в полноэкранный режим
            self.toggle_fullscreen_button.config(text="Выход из полного экрана")  # Изменяем текст кнопки
        else:
            self.root.attributes('-fullscreen', False)  # Выход из полного экрана
            self.toggle_fullscreen_button.config(text="Полный экран")  # Возвращаем текст кнопки

    def quit(self):
        """Завершение программы"""
        self.client_socket.close()
        self.root.quit()


# Настройка сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('79.178.86.141', 25565))

# Создание Tkinter окна
root = tk.Tk()
app = ScreenViewerApp(root, client_socket)
root.mainloop()
