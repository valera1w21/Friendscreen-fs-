import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import io
import os

class ScreenViewerApp:
    def __init__(self, master, root, socket):
        self.master = master  # Главное окно приложения
        self.root = root      # Корневое окно Tkinter
        self.socket = socket  # Сокет (можно использовать для расширения функционала)

        # Настройка главного окна
        self.root.title("fs")
        self.root.geometry("800x600")

         # Путь к иконке
        icon_path = os.path.join(os.path.dirname(__file__), "fs", "fs.ico")

        # Проверка наличия файла и установка иконки
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print("Файл иконки не найден:", icon_path)

        # Фрейм для изображения, центрируемый в окне
        self.frame = tk.Frame(self.root, bg="black")  # Рамка с фоновым цветом
        self.frame.pack(fill=tk.BOTH, expand=True) 

        # Панель с кнопками
        self.button_frame = tk.Frame(self.root, bg="gray")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Кнопка выхода
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_program)
        self.exit_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Кнопка увеличения окна
        self.maximize_button = tk.Button(self.button_frame, text="Maximize", command=self.maximize_window)
        self.maximize_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Кнопка возврата к стандартному размеру
        self.unzoom_button = tk.Button(self.button_frame, text="Unzoom", command=self.unzoom_window)
        self.unzoom_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Добавляем метку для изображения
        self.label = tk.Label(self.frame, bg="black")
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Центрируем изображение
       
        # Запуск обновления изображения
        self.root.after(100, self.update_image)

    def capture_screen(self):
        """Функция для захвата экрана и преобразования его в формат Tkinter."""
        try:
            screenshot = pyautogui.screenshot()
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            image = Image.open(io.BytesIO(img_byte_arr))

            # Получаем размеры фрейма для масштабирования изображения
            frame_width = self.frame.winfo_width()
            frame_height = self.frame.winfo_height()

            if frame_width < 10 or frame_height < 10:
                return None  # Если окно слишком маленькое

            # Масштабируем изображение под размеры фрейма
            image = image.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Ошибка при захвате экрана: {e}")
            return None

    def update_image(self):
        """Метод для обновления изображения в окне."""
        if self.root.winfo_exists():
            photo = self.capture_screen()
            if photo:
                self.label.config(image=photo)
                self.label.image = photo  # Сохраняем ссылку на изображение
            else:
                print("Ошибка: не удалось обновить изображение.")
            self.root.after(100, self.update_image)

    def exit_program(self):
        """Метод для выхода из программы."""
        self.root.after_cancel(self.update_image)  # Останавливаем обновление
        self.root.destroy()  # Уничтожаем окно

        
    def maximize_window(self):
       """Увеличение окна до максимального размера."""
       self.root.state('zoomed')

    def unzoom_window(self):
        """Возвращение окна к стандартному размеру."""
        self.root.state('normal')
        self.root.geometry(f"{self.original_width}x{self.original_height}")

# Создаем объект Tkinter
root = tk.Tk()
socket_placeholder = None  # Здесь можно подключить реальный сокет

# Создаем и запускаем приложение
app = ScreenViewerApp(master=None, root=root, socket=socket_placeholder)
root.mainloop()
