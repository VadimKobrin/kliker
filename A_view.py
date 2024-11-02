# внешний выгляд
import tkinter as tk
from functools import partial
from PIL import Image, ImageTk
from tkinter import messagebox


class GameView:
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        self.create_menu()
        self.labels_upgrades = []
        self.buttons_upgrades = []
        # Основная часть
        window.title("Мое приложение")
        window.geometry("1600x1000")
        self.canvas = tk.Canvas(window, width=1600, height=1000)
        self.canvas.place(x=1, y=1)
        self.canvas.config(bg="white")
        self.field_color = self.canvas.cget("bg")
        self.boss_button()
        self.slider = tk.Scale(window, from_=0, to=1000, orient="vertical", length=750, command=self.slider_command,
                               showvalue=False)
        self.slider.place(x=1500, y=0)
        window.bind("<MouseWheel>", self.on_mouse_wheel)

        # Открываем иконку курсора
        mouse_icon = Image.open("kursor.ico")
        mouse_icon = mouse_icon.resize((16, 16), Image.LANCZOS)
        self.mouse_icon = ImageTk.PhotoImage(mouse_icon)

        # Создаем метку с иконкой мышки
        self.label_mouse_icon = tk.Label(window, image=self.mouse_icon)
        self.label_mouse_icon.image = self.mouse_icon
        self.label_mouse_icon.place(x=36, y=405)
        window.update()

        # Вывод данных
        self.label_check = tk.Label(window, text="Счёт: 0", font=("Comic Sans MS", 16, "bold"), fg="purple")
        self.label_check.place(x=400, y=70)
        self.label_coeff = tk.Label(window, text="Сила клика: ×1", font=("Times New Roman", 16, "italic"), fg="orange")
        self.label_coeff.place(x=400, y=100)
        self.label_rebirth = tk.Label(window, text="Ребитхи: 0", font=("Arial", 16, "bold"), fg="green")
        self.label_rebirth.place(x=400, y=130)
        self.label_upgradeX = tk.Label(window, text="Последних улучшений: 0/5", font=("Arial", 16, "bold"), fg="blue")
        self.label_upgradeX.place(x=400, y=170)

        # Кнопки и цена улучшений
        self.buttonRebirth = tk.Button(window, text=" РЕБИТХ! ", font=("Comic Sans MS", 16, "bold"), fg="green",
                                       command=self.controller.rebirth_condition, width=30, height=1)
        self.buttonRebirth.place(x=400, y=1)

        self.labels_upgrades = []
        self.buttons_upgrades = []

        # Кнопки умножения
        self.buttonx2 = tk.Button(window, text="умножение на 2",
                                  command=lambda: self.controller.upgrade("upgradex2", 2), width=30, height=2)
        self.buttonx2.place(x=950, y=950)

        self.label_upgradex2 = tk.Label(window,
                                        text=f"Цена: {self.controller.format_number(self.controller.model.get_upgrade_cost('upgradex2'))}",
                                        font=("Comic Sans MS", 14, "bold"), fg="purple")
        self.label_upgradex2.place(x=1250, y=950)

        self.buttonx3 = tk.Button(window, text="умножение на 3",
                                  command=lambda: self.controller.upgrade("upgradex3", 3), width=30, height=2)
        self.buttonx3.place(x=950, y=1000)

        self.label_upgradex3 = tk.Label(window,
                                        text=f"Цена: {self.controller.format_number(self.controller.model.get_upgrade_cost('upgradex3'))}",
                                        font=("Comic Sans MS", 14, "bold"), fg="purple")
        self.label_upgradex3.place(x=1250, y=1000)

        # Доп мышки
        self.button_mouse = tk.Button(window, text=" автомышкааа!!!",
                                      command=lambda: self.controller.mouse_cliker("upgrade_mouse"), width=20,
                                      height=2)
        self.button_mouse.place(x=50, y=350)
        self.label_upgrade_mouse = tk.Label(window,
                                            text=f"Цена: {self.controller.format_number(self.controller.get_upgrade_cost('upgrade_mouse'))}",
                                            font=("Comic Sans MS", 12, "bold"), fg="purple")
        self.label_upgrade_mouse.place(x=210, y=355)
        self.button_mouse_speed = tk.Button(window, text=" улучшение скорости мыши",
                                            command=lambda: self.controller.mouse_cliker("upgrade_mouse_speed"),
                                            width=23, height=2)
        self.button_mouse_speed.place(x=350, y=350)
        self.label_upgrade_mouse_speed = tk.Label(window,
                                                  text=f"Цена: {self.controller.format_number(self.controller.get_upgrade_cost('upgrade_mouse_speed'))}",
                                                  font=("Comic Sans MS", 12, "bold"), fg="purple")
        self.label_upgrade_mouse_speed.place(x=530, y=355)
        self.label_mouse = tk.Label(window,
                                    text=f": {self.controller.mouses}    Скорость раз в: {self.controller.speed} мс",
                                    font=("Comic Sans MS", 12, "bold"), fg="purple")
        self.label_mouse.place(x=50, y=400)

        for i in range(0, 17):
            upgrade_name = f'upgrade{i}'
            cost = self.controller.get_upgrade_cost(upgrade_name)
            label = tk.Label(self.window, text=f"Цена: {self.controller.format_number(cost)}",
                             font=("Comic Sans MS", 16, "bold"), fg="purple")
            label.place(x=1250, y=5 + i * 45)
            self.labels_upgrades.append(label)

            increment_value = self.controller.increment[i]
            upgrade_button = tk.Button(window, text=f"улучшение на {increment_value}",
                                       command=partial(self.controller.upgrade, f"upgrade{i}", increment_value), width=30, height=2)
            upgrade_button.place(x=950, y=5 + i * 45)
            self.buttons_upgrades.append(upgrade_button)

    def slider_command(self, value):
        value = int(value)
        koef_slider = 1
        buttons = [f"button{q}" for q in range(0, 17)]
        labels = [f"label_upgrade{q}" for q in range(0, 17)]

        for q, button in enumerate(buttons):
            globals()[button].place(x=950, y=5 + q * 45 - value * koef_slider)

        for q, label in enumerate(labels):
            globals()[label].place(x=1250, y=5 + q * 45 - value * koef_slider)

        self.buttonx2.place(x=950, y=950 - value * koef_slider)
        self.buttonx3.place(x=950, y=1000 - value * koef_slider)
        self.label_upgradex2.place(x=1250, y=950 - value * koef_slider)
        self.label_upgradex3.place(x=1250, y=1000 - value * koef_slider)

    def on_mouse_wheel(self, event):
        self.slider.set(self.slider.get() - int(event.delta / 5))

    def create_menu(self):
        menu_bar = tk.Menu(self.window)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Сохранить", command=self.controller.save)
        file_menu.add_command(label="Старое сохранение", command=self.controller.take_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.window.quit)
        menu_bar.add_cascade(label="Меню", menu=file_menu)
        self.window.config(menu=menu_bar)
        pass

    def update_labels(self):
        labels = [
            ("label_check", f"Счёт: {self.controller.format_number(self.controller.check)}"),
            ("label_coeff", f"Сила клика: ×{self.controller.format_number(self.controller.coeff)}"),
            ("label_rebirth", f"Ребитхи: {self.controller.rebirth_count}"),
            ("label_upgradeX", f"Последних улучшений: {self.controller.upgrade_end_count}/5"),
            ("label_upgradex2",
             f"Цена: {self.controller.format_number(self.controller.upgrade_costs['upgradex2'])}"),
            ("label_upgradex3",
             f"Цена: {self.controller.format_number(self.controller.upgrade_costs['upgradex3'])}"),
            ("label_upgrade_mouse",
             f"Цена: {self.controller.format_number(self.controller.upgrade_costs['upgrade_mouse'])}"),
            ("label_upgrade_mouse_speed",
             f"Цена: {self.controller.format_number(self.controller.upgrade_costs['upgrade_mouse_speed'])}"),
            ("label_mouse", f": {self.controller.mouses}    Скорость раз в: {self.controller.speed} мс")
        ]

        for i, label in enumerate(self.labels_upgrades):
            upgrade_name = f'upgrade{i}'
            cost = self.controller.get_upgrade_cost(upgrade_name)
            text = f"Цена: {self.controller.format_number(cost)}"
            label.config(text=text, bg=self.field_color)



    def change_color(self):
        if self.controller.button_main is not None and isinstance(self.controller.button_main, (str, int)):
            new_color = self.controller.random_color()
            self.canvas.itemconfig(self.controller.button_main, fill=new_color)
        else:
            messagebox.showinfo("Ошибка", "Кнопка не существует или имеет неверный тип!")

    def format_number(self, number):
        return "{:,}".format(number).replace(",", " ")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def figure(self):
        if 'button_main' in globals():
            self.canvas.delete(self.model.button_main)
        if 'button_text' in globals():
            self.canvas.delete(self.model.button_text)

        if self.rebirth_count < 3:
            # Создаем круг с текстом
            button_main = self.canvas.create_oval(50, 20, 350, 320, fill="yellow")
            button_text = self.canvas.create_text(200, 170, text="Нажми меня!", fill="black")
        elif (self.rebirth_count >= 3) and (self.rebirth_count < 6):
            # Создаем прямоугольник с текстом
            button_main = self.canvas.create_rectangle(50, 450, 350, 750, fill="yellow")
            button_text = self.canvas.create_text(200, 600, text="Нажми меня!", fill="black")
        else:
            # Создаем круг 2 с текстом
            button_main = self.canvas.create_oval(50, 20, 350, 320, fill="green")
            button_text = self.canvas.create_text(200, 170, text="Нажми меня!", fill="black")
        self.canvas.tag_bind(button_main, "<Button-1>", self.model.button_click)
        self.canvas.tag_bind(button_text, "<Button-1>", self.model.button_click)


    def boss_button(self):
        self.button_main = self.canvas.create_oval(50, 20, 350, 320, fill="yellow")
        self.button_text = self.canvas.create_text(200, 170, text="Нажми меня!", fill="black")
        self.canvas.tag_bind(self.button_main, '<ButtonPress-1>', self.controller.button_click)
        self.canvas.tag_bind(self.button_text, '<ButtonPress-1>', self.controller.button_click)
