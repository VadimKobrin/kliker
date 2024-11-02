import tkinter as tk
import os
import stat
from tkinter import messagebox
import random
import numpy as np
import json
from PIL import Image, ImageTk
from functools import partial

button_main = None
button_text = None
check = 0
coeff = 1
rebirth_count = 0
upgrade_end_count = 0
upgradexx_count = 0
mouses = 0
speed = 40000

upgrade_costs = {
    "upgrade0":  10,    "upgrade1":  40,    "upgrade2":  120,    "upgrade3":  300,    "upgrade4":  800,
    "upgrade5":  1400,   "upgrade6":  2700,    "upgrade7":  5000,    "upgrade8":  8500,    "upgrade9":  15000,
    "upgrade10": 23000,    "upgrade11": 35000,    "upgrade12": 65000,    "upgrade13": 100000,    "upgrade14": 180000,
    "upgrade15": 300000,    "upgrade16": 470000,    "upgrade17": 700000,    "upgrade18": 1000000,
    "upgrade19": 1700000,    "upgrade20": 3100000,    "upgrade21": 5000000,    "upgrade22": 8000000,
    "upgrade23": 15000000,    "upgrade24": 35000000,    "upgrade25": 60000000,    "upgrade26": 100000000,
    "upgrade27": 140000000,    "upgrade28": 230000000,    "upgrade29": 350000000,    "upgrade30": 500000000,
    "upgradex2": 50000,    "upgradex3": 1500000,    "upgrade_mouse": 3000,    "upgrade_mouse_speed": 10000
}

upgrade_costs_start = {
    "upgrade0":  10,    "upgrade1":  40,    "upgrade2":  120,    "upgrade3":  300,    "upgrade4":  800,
    "upgrade5":  1400,   "upgrade6":  2700,    "upgrade7":  5000,    "upgrade8":  8500,    "upgrade9":  15000,
    "upgrade10": 23000,    "upgrade11": 35000,    "upgrade12": 65000,    "upgrade13": 100000,    "upgrade14": 180000,
    "upgrade15": 300000,    "upgrade16": 470000,    "upgrade17": 700000,    "upgrade18": 1000000,
    "upgrade19": 1700000,    "upgrade20": 3100000,    "upgrade21": 5000000,    "upgrade22": 8000000,
    "upgrade23": 15000000,    "upgrade24": 35000000,    "upgrade25": 60000000,    "upgrade26": 100000000,
    "upgrade27": 140000000,    "upgrade28": 230000000,    "upgrade29": 350000000,    "upgrade30": 500000000,
    "upgradex2": 50000,    "upgradex3": 1500000,    "upgrade_mouse": 3000,    "upgrade_mouse_speed": 10000
}

increment = [
    1, 2, 4, 7, 10,
    14, 17, 30, 50, 75,
    110, 200, 350, 500, 700,
    1000, 1250, 1700, 2400,
    3500, 5000, 6750, 9000,
    12000, 15000, 18500, 21000,
    25000, 30000, 50000, -25000
]


def format_number(number):
    return "{:,}".format(number).replace(",", " ")


def save():
    global check, coeff, upgrade_costs, rebirth_count, upgrade_end_count, \
        upgrade_costs_start, upgradexx_count, button_main, button_text, mouses, speed, field_color

    if rebirth_count < 3:
        shape_type = "oval"
    elif (rebirth_count >= 3) and (rebirth_count < 6):
        shape_type = "rectangle"
    else:
        shape_type = "oval"

    if not os.path.exists("result.txt"):
        with open("result.txt", "w", encoding="utf-8") as file:
            pass

    button_coords = []
    button_text_coords = []

    if button_main is not None and button_text is not None:
        if isinstance(button_main, (str, int)) and isinstance(button_text, (str, int)):
            button_coords = canvas.coords(button_main)
            button_text_coords = canvas.coords(button_text)
        else:
            messagebox.showinfo("xyita", "Invalid button_main or button_text!")
    else:
        messagebox.showinfo("xyita", "da, xyita!")

    button_text_content = canvas.itemcget(button_text, "text") if button_text else ""
    button_color = canvas.itemcget(button_main, "fill") if button_main else ""
    field_color = canvas.cget("bg")

    data = {
        "check": check,
        "coeff": coeff,
        "rebirth_count": rebirth_count,
        "upgrade_end_count": upgrade_end_count,
        "upgradexx_count": upgradexx_count,
        "upgrade_costs": upgrade_costs,
        "upgrade_costs_start": upgrade_costs_start,
        "button_coords": button_coords,
        "button_color": button_color,
        "button_text_coords": button_text_coords,
        "button_text_content": button_text_content,
        "field_color": field_color,
        "shape_type": shape_type,
        "mouses": mouses,
        "speed": speed
    }

    try:
        os.chmod("result.txt", stat.S_IWRITE)

        with open("result.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        os.chmod("result.txt", stat.S_IREAD)
        messagebox.showinfo("Сохранение", "Данные сохранены!")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")


def take_data():
    global check, coeff, upgrade_costs, rebirth_count, upgrade_end_count, \
        upgrade_costs_start, upgradexx_count, button_main, button_text, mouses, speed, field_color

    if 'button_main' in globals():
        canvas.delete(button_main)
    if 'button_text' in globals():
        canvas.delete(button_text)

    try:
        with open("result.txt", 'r', encoding="utf-8") as file:
            data = json.load(file)

        check = data["check"]
        coeff = data["coeff"]
        rebirth_count = data["rebirth_count"]
        upgrade_end_count = data["upgrade_end_count"]
        upgradexx_count = data["upgradexx_count"]
        upgrade_costs = data["upgrade_costs"]
        upgrade_costs_start = data["upgrade_costs_start"]
        button_coords = data["button_coords"]
        button_color = data["button_color"]
        button_text_coords = data["button_text_coords"]
        button_text_content = data["button_text_content"]
        field_color = data["field_color"]
        shape_type = data["shape_type"]
        mouses = data["mouses"]
        speed = data["speed"]

        # Восстанавливаем кнопку, текст, фон
        if shape_type == "oval":
            button_main = canvas.create_oval(*button_coords, fill=button_color)
        elif shape_type == "rectangle":
            button_main = canvas.create_rectangle(*button_coords, fill=button_color)
        else:
            button_main = canvas.create_oval(*button_coords, fill=button_color)

        button_text = canvas.create_text(*button_text_coords, text=button_text_content, fill="black")
        canvas.tag_bind(button_main, "<Button-1>", button_click)
        canvas.tag_bind(button_text, "<Button-1>", button_click)
        canvas.config(bg=field_color)

        update_labels()

        if mouses > 0:
            auto_click()

        return (check, coeff, rebirth_count, upgrade_end_count, upgradexx_count,
                upgrade_costs, upgrade_costs_start, button_main, button_text, mouses, speed, field_color)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
        return None


def create_menu():
    global window
    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Сохранить", command=save)
    file_menu.add_command(label="Старое сохранение", command=take_data)
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=window.quit)
    menu_bar.add_cascade(label="Меню", menu=file_menu)
    window.config(menu=menu_bar)


def auto_click():
    global mouses, speed
    n = 0
    while n < mouses:
        button_click()
        n += 1

    window.after(speed, auto_click)


def mouse_cliker(upgrade_key):
    global check, coeff, upgrade_end_count, mouses, speed
    cost = upgrade_costs[upgrade_key]
    if check >= cost:
        check -= cost
        if upgrade_key == "upgrade_mouse":
            mouses += 1
            upgrade_costs[upgrade_key] = int(cost * 5)
        elif upgrade_key == "upgrade_mouse_speed":
            speed = int(speed/np.sqrt(2))
            upgrade_costs[upgrade_key] = int(cost * 12)
        update_labels()
        if mouses == 1:
            auto_click()
    else:
        messagebox.showinfo("Посмотри на циферки", f"Нужно {format_number(cost)} кликов")


def upgrade(upgrade_key, increment_value):
    global check, coeff, upgrade_end_count, upgradexx_count
    cost = upgrade_costs[upgrade_key]
    if check >= cost:
        if (upgrade_key == "upgradex2" or upgrade_key == "upgradex3") and upgradexx_count <= 5:
            upgradexx_count += 1
            coeff *= increment_value
            upgrade_costs[upgrade_key] = int(cost * 10)
        elif (upgrade_key == "upgradex2" or upgrade_key == "upgradex3") and upgradexx_count > 5:
            messagebox.showinfo("я вредный", "Слишком много умножений уже сделано)))")
            check += cost
        else:
            coeff += increment_value
            upgrade_costs[upgrade_key] = int(cost * 1.3)
        if upgrade_key == "upgrade30":
            upgrade_end_count += 1
        check -= cost
        update_labels()
    else:
        messagebox.showinfo("Посмотри на циферки", f"Нужно {format_number(cost)} кликов")
    if coeff < 1:
        messagebox.showinfo("Точно всё хорошо", "ЖИВИ!!! Не бей бедного разраба!!!")
        coeff = 1


def change_color():     #на главную кнопку
    global button_main
    if button_main is not None and isinstance(button_main, (str, int)):
        new_color = random_color()
        canvas.itemconfig(button_main, fill=new_color)
    else:
        messagebox.showinfo("Ошибка", "Кнопка не существует или имеет неверный тип!")


def random_color():
    def color_distance(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5
    purple = (128, 0, 128)
    black = (0, 0, 0)
    green = (0, 128, 0)
    while True:
        color = random.randint(0, 0xFFFFFF)
        # Разделение цвета на компоненты RGB
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        brightness = (r * 0.299 + g * 0.587 + b * 0.114)
        # Проверка, что цвет достаточно далёк от запрещённых цветов и не слишком тёмный
        if (color_distance((r, g, b), purple) > 100 and
                color_distance((r, g, b), black) > 100 and
                color_distance((r, g, b), green) > 100 and
                brightness > 70):
            # Форматирование цвета в шестнадцатеричном формате
            return "#{:06x}".format(color)


def rebirth(step=0):
    global check, coeff, rebirth_count, upgrade_end_count, upgradexx_count, mouses, speed, field_color
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFFFFF", "#000000"]
    colors *= 7
    if step < len(colors):
        canvas.config(bg=colors[step])
        window.after(30, rebirth, step + 1)
    else:
        canvas.config(bg=random_color())
        field_color = canvas.cget("bg")
        rebirth_count += 1
        check = 0
        coeff = 1
        upgrade_end_count = 0
        upgradexx_count = 0
        mouses = 0
        speed = 10000
        for key in upgrade_costs:
            upgrade_costs_start[key] = int(upgrade_costs_start[key] * 2)
            upgrade_costs[key] = int(upgrade_costs_start[key])
        update_labels()
        figure()
        buttonRebirth.config(state=tk.NORMAL)


def rebirth_condition():
    global upgrade_end_count
    if upgrade_end_count >= 5:
        buttonRebirth.config(state=tk.DISABLED)
        rebirth()
    else:
        messagebox.showinfo("Не ребитх!", "Необходимо сделать последнее улучшение ПЯТЬ раз!")


def slider(value_slider):
    value_slider = int(value_slider)
    koef_slider = 1
    buttons = [f"button{q}" for q in range(0, 31)]
    labels = [f"label_upgrade{q}" for q in range(0, 31)]

    for q, button in enumerate(buttons):
        globals()[button].place(x=950, y=5 + q * 45 - value_slider * koef_slider)

    for q, label in enumerate(labels):
        globals()[label].place(x=1250, y=5 + q * 45 - value_slider * koef_slider)

    buttonx2.place(x=950, y=1500 - value_slider * koef_slider)
    buttonx3.place(x=950, y=1550 - value_slider * koef_slider)
    label_upgradex2.place(x=1250, y=1500 - value_slider * koef_slider)
    label_upgradex3.place(x=1250, y=1550 - value_slider * koef_slider)


def update_labels():
    labels = [
        ("label_check", f"Счёт: {format_number(check)}"),
        ("label_coeff", f"Сила клика: ×{format_number(coeff)}"),
        ("label_rebirth", f"Ребитхи: {rebirth_count}"),
        ("label_upgradeX", f"Последних улучшений: {upgrade_end_count}/5"),
        ("label_upgrade0", f"Цена: {format_number(upgrade_costs['upgrade0'])}"),
        ("label_upgrade1", f"Цена: {format_number(upgrade_costs['upgrade1'])}"),
        ("label_upgrade2", f"Цена: {format_number(upgrade_costs['upgrade2'])}"),
        ("label_upgrade3", f"Цена: {format_number(upgrade_costs['upgrade3'])}"),
        ("label_upgrade4", f"Цена: {format_number(upgrade_costs['upgrade4'])}"),
        ("label_upgrade5", f"Цена: {format_number(upgrade_costs['upgrade5'])}"),
        ("label_upgrade6", f"Цена: {format_number(upgrade_costs['upgrade6'])}"),
        ("label_upgrade7", f"Цена: {format_number(upgrade_costs['upgrade7'])}"),
        ("label_upgrade8", f"Цена: {format_number(upgrade_costs['upgrade8'])}"),
        ("label_upgrade9", f"Цена: {format_number(upgrade_costs['upgrade9'])}"),
        ("label_upgrade10", f"Цена: {format_number(upgrade_costs['upgrade10'])}"),
        ("label_upgrade11", f"Цена: {format_number(upgrade_costs['upgrade11'])}"),
        ("label_upgrade12", f"Цена: {format_number(upgrade_costs['upgrade12'])}"),
        ("label_upgrade13", f"Цена: {format_number(upgrade_costs['upgrade13'])}"),
        ("label_upgrade14", f"Цена: {format_number(upgrade_costs['upgrade14'])}"),
        ("label_upgrade15", f"Цена: {format_number(upgrade_costs['upgrade15'])}"),
        ("label_upgrade16", f"Цена: {format_number(upgrade_costs['upgrade16'])}"),
        ("label_upgrade17", f"Цена: {format_number(upgrade_costs['upgrade17'])}"),
        ("label_upgrade18", f"Цена: {format_number(upgrade_costs['upgrade18'])}"),
        ("label_upgrade19", f"Цена: {format_number(upgrade_costs['upgrade19'])}"),
        ("label_upgrade20", f"Цена: {format_number(upgrade_costs['upgrade20'])}"),
        ("label_upgrade21", f"Цена: {format_number(upgrade_costs['upgrade21'])}"),
        ("label_upgrade22", f"Цена: {format_number(upgrade_costs['upgrade22'])}"),
        ("label_upgrade23", f"Цена: {format_number(upgrade_costs['upgrade23'])}"),
        ("label_upgrade24", f"Цена: {format_number(upgrade_costs['upgrade24'])}"),
        ("label_upgrade25", f"Цена: {format_number(upgrade_costs['upgrade25'])}"),
        ("label_upgrade26", f"Цена: {format_number(upgrade_costs['upgrade26'])}"),
        ("label_upgrade27", f"Цена: {format_number(upgrade_costs['upgrade27'])}"),
        ("label_upgrade28", f"Цена: {format_number(upgrade_costs['upgrade28'])}"),
        ("label_upgrade29", f"Цена: {format_number(upgrade_costs['upgrade29'])}"),
        ("label_upgrade30", f"Цена: {format_number(upgrade_costs['upgrade30'])}"),
        ("label_upgradex2", f"Цена: {format_number(upgrade_costs['upgradex2'])}"),
        ("label_upgradex3", f"Цена: {format_number(upgrade_costs['upgradex3'])}"),
        ("label_upgrade_mouse", f"Цена: {format_number(upgrade_costs['upgrade_mouse'])}"),
        ("label_upgrade_mouse_speed", f"Цена: {format_number(upgrade_costs['upgrade_mouse_speed'])}"),
        ("label_mouse", f": {mouses}    Скорость раз в: {speed} мс")
    ]
    for label, text in labels:
        globals()[label].config(text=text, bg=field_color)


def figure():
    global button_main, button_text, rebirth_count
    if 'button_main' in globals():
        canvas.delete(button_main)
    if 'button_text' in globals():
        canvas.delete(button_text)

    if rebirth_count < 3:
        # Создаем круг с текстом
        button_main = canvas.create_oval(50, 20, 350, 320, fill="yellow")
        button_text = canvas.create_text(200, 170, text="Нажми меня!", fill="black")
    elif (rebirth_count >= 3) and (rebirth_count < 6):
        # Создаем прямоугольник с текстом
        button_main = canvas.create_rectangle(50, 450, 350, 750, fill="yellow")
        button_text = canvas.create_text(200, 600, text="Нажми меня!", fill="black")
    else:
        # Создаем круг 2 с текстом
        button_main = canvas.create_oval(50, 20, 350, 320, fill="green")
        button_text = canvas.create_text(200, 170, text="Нажми меня!", fill="black")
    canvas.tag_bind(button_main, "<Button-1>", button_click)
    canvas.tag_bind(button_text, "<Button-1>", button_click)
    return button_main, button_text


def button_click(event=None):
    global check, coeff
    check += coeff
    update_labels()
    change_color()
    return check


# основная часть
window = tk.Tk()
window.title("Мое приложение")
window.geometry("1600x1000")
canvas = tk.Canvas(window, width=1600, height=1000)
canvas.place(x=1, y=1)
canvas.config(bg="white")
field_color = canvas.cget("bg")
slider = tk.Scale(window, from_=0, to=1000, orient="vertical", length=750, command=slider, showvalue=False)
slider.place(x=1500, y=0)
window.bind("<MouseWheel>", lambda event: slider.set(slider.get() - int(event.delta / 5)))

figure()
# Открываем иконку курсора
mouse_icon = Image.open("kursor.ico")
mouse_icon = mouse_icon.resize((16, 16), Image.Resampling.LANCZOS)
mouse_icon = ImageTk.PhotoImage(mouse_icon)
# Создаем метку с иконкой мышки
label_mouse_icon = tk.Label(window, image=mouse_icon)
label_mouse_icon.image = mouse_icon
label_mouse_icon.place(x=36, y=405)
window.update()


# вывод данных
label_check = tk.Label(window, text="Счёт: 0", font=("Times New Roman", 16, "italic bold"), fg="green")
label_check.place(x=400, y=70)
label_coeff = tk.Label(window, text="Сила клика: ×1", font=("Times New Roman", 16, "italic bold"), fg="green")
label_coeff.place(x=400, y=100)
label_rebirth = tk.Label(window, text="Ребитхи: 0", font=("Times New Roman", 16, "italic bold"), fg="green")
label_rebirth.place(x=400, y=130)
label_upgradeX = tk.Label(window, text="Последних улучшений: 0/5", font=("Times New Roman", 16, "italic bold"), fg="green")
label_upgradeX.place(x=400, y=170)

# кнопки и цена улучшений
buttonRebirth = tk.Button(window, text=" РЕБИТХ! ", font=("Comic Sans MS", 16, "italic bold"), fg="green",
                          command=lambda: rebirth_condition(), width=30)
buttonRebirth.place(x=400, y=1)

for i in range(0, 31):
    label = tk.Label(window, text=f"Цена: {format_number(upgrade_costs[f'upgrade{i}'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
    label.place(x=1250, y=5 + i * 45)
    globals()[f'label_upgrade{i}'] = label

for i in range(0, 31):
    value = increment[i]
    upgrade_button = tk.Button(window, text=f"улучшение на {value}", font=("Comic Sans MS", 12, "italic bold"),
                               command=partial(upgrade, f"upgrade{i}", value))
    upgrade_button.config(width=20)
    upgrade_button.place(x=950, y=5 + i * 45)
    globals()[f'button{i}'] = upgrade_button

# кнопки умножения
buttonx2 = tk.Button(window, text="умножение на 2", font=("Comic Sans MS", 12, "italic bold"),
                     command=lambda: upgrade("upgradex2", 2), width=20)
buttonx2.place(x=950, y=1500)
label_upgradex2 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgradex2'])}", font=("Comic Sans MS", 14, "bold"), fg="purple")
label_upgradex2.place(x=1250, y=1500)
buttonx3 = tk.Button(window, text="умножение на 3", font=("Comic Sans MS", 12, "italic bold"),
                     command=lambda: upgrade("upgradex3", 3), width=20)
buttonx3.place(x=950, y=1550)
label_upgradex3 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgradex3'])}", font=("Comic Sans MS", 14, "bold"), fg="purple")
label_upgradex3.place(x=1250, y=1550)

# доп мышки
button_mouse = tk.Button(window, text=" автоклики!",
                         command=lambda: mouse_cliker("upgrade_mouse"), width=20, height=2)
button_mouse.place(x=50, y=350)
label_upgrade_mouse = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade_mouse'])}", font=("Comic Sans MS", 12, "bold"), fg="purple")
label_upgrade_mouse.place(x=210, y=355)
button_mouse_speed = tk.Button(window, text=" улучшение скорости мыши",
                               command=lambda: mouse_cliker("upgrade_mouse_speed"), width=23, height=2)
button_mouse_speed.place(x=350, y=350)
label_upgrade_mouse_speed = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade_mouse_speed'])}", font=("Comic Sans MS", 12, "bold"), fg="purple")
label_upgrade_mouse_speed.place(x=530, y=355)
label_mouse = tk.Label(window, text=f": {mouses}    Скорость раз в: {speed} мс", font=("Comic Sans MS", 12, "bold"), fg="purple")
label_mouse.place(x=50, y=400)

update_labels()
create_menu()

window.mainloop()
