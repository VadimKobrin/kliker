import tkinter as tk
import os
import stat
import numpy as np
from tkinter import messagebox
import random
import json
import pygame
from PIL import Image, ImageTk
from functools import partial

button_main = None
button_text = None
check = 0
coeff = 10000000000000000
rebirth_count = 0
upgrade_end_count = 0
upgradexx_count = 0
dino_count = 0
speed = 40000
current_page = 0
hard = False
is_stopping = False
images_dino = []
pygame.init()
pygame.mixer.init()
song_index = 0
playlist = []

upgrade_costs = {
    "upgrade0":  10,    "upgrade1":  40,    "upgrade2":  120,    "upgrade3":  300,    "upgrade4":  800,
    "upgrade5":  1400,   "upgrade6":  2700,    "upgrade7":  5000,    "upgrade8":  8500,    "upgrade9":  15000,
    "upgrade10": 23000,    "upgrade11": 35000,    "upgrade12": 65000,    "upgrade13": 100000,    "upgrade14": 180000,
    "upgrade15": 300000,    "upgrade16": 470000,    "upgrade17": 700000,    "upgrade18": 1000000,
    "upgrade19": 1700000,    "upgrade20": 3100000,    "upgrade21": 5000000,    "upgrade22": 8000000,
    "upgrade23": 15000000,    "upgrade24": 35000000,    "upgrade25": 60000000,    "upgrade26": 100000000,
    "upgrade27": 140000000,    "upgrade28": 230000000,    "upgrade29": 350000000,    "upgrade30": 500000000,
    "upgradex2": 50000,    "upgradex3": 1500000,    "upgrade_dino": 3000,    "upgrade_dino_speed": 10000
}

upgrade_costs_start = {
    "upgrade0":  10,    "upgrade1":  40,    "upgrade2":  120,    "upgrade3":  300,    "upgrade4":  800,
    "upgrade5":  1400,   "upgrade6":  2700,    "upgrade7":  5000,    "upgrade8":  8500,    "upgrade9":  15000,
    "upgrade10": 23000,    "upgrade11": 35000,    "upgrade12": 65000,    "upgrade13": 100000,    "upgrade14": 180000,
    "upgrade15": 300000,    "upgrade16": 470000,    "upgrade17": 700000,    "upgrade18": 1000000,
    "upgrade19": 1700000,    "upgrade20": 3100000,    "upgrade21": 5000000,    "upgrade22": 8000000,
    "upgrade23": 15000000,    "upgrade24": 35000000,    "upgrade25": 60000000,    "upgrade26": 100000000,
    "upgrade27": 140000000,    "upgrade28": 230000000,    "upgrade29": 350000000,    "upgrade30": 500000000,
    "upgradex2": 50000,    "upgradex3": 1500000,    "upgrade_dino": 3000,    "upgrade_dino_speed": 10000
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
        upgrade_costs_start, upgradexx_count, button_main, button_text, dino_count, speed, field_color

    if rebirth_count < 3:
        shape_type = "oval"
    elif (rebirth_count >= 3) and (rebirth_count < 6):
        shape_type = "rectangle"
    else:
        shape_type = "oval"

    if not os.path.exists("data cache/result.txt"):
        with open("data cache/result.txt", "w", encoding="utf-8") as file:
            pass

    button_coords = []
    button_text_coords = []

    if button_main is not None and button_text is not None:
        if isinstance(button_main, (str, int)) and isinstance(button_text, (str, int)):
            button_coords = canvas.coords(button_main)
            button_text_coords = canvas.coords(button_text)
        else:
            messagebox.showinfo("Invalid", "Invalid button_main or button_text!")
    else:
        messagebox.showinfo("Invalid", "da, invalid!")

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
        "dino_count": dino_count,
        "speed": speed,
    }

    try:
        os.chmod("data cache/result.txt", stat.S_IWRITE)

        with open("data cache/result.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        os.chmod("data cache/result.txt", stat.S_IREAD)
        messagebox.showinfo("Сохранение", "Данные сохранены!")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")


def take_data():
    global check, coeff, upgrade_costs, rebirth_count, upgrade_end_count, \
        upgrade_costs_start, upgradexx_count, button_main, button_text, dino_count, speed, field_color

    if 'button_main' in globals():
        canvas.delete(button_main)
    if 'button_text' in globals():
        canvas.delete(button_text)

    try:
        with open("data cache/result.txt", 'r', encoding="utf-8") as file:
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
        dino_count = data["dino_count"]
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

        if rebirth_count < 3:
            canvas.coords(button_main, 50, 20, 350, 320)
        elif (rebirth_count >= 3) and (rebirth_count < 6):
            canvas.coords(button_main, 50, 450, 350, 750)
        else:
            canvas.coords(button_main, 200, 20, 50, 270, 350, 270)

        if dino_count > 0:
            auto_click()

        return (check, coeff, rebirth_count, upgrade_end_count, upgradexx_count,
                upgrade_costs, upgrade_costs_start, button_main, button_text, dino_count, speed, field_color)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
        return None


def create_menu():
    global window
    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Меню", menu=file_menu)
    file_menu.add_command(label="Сохранить", command=save)
    file_menu.add_command(label="Старое сохранение", command=take_data)
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=window.quit)
    window.config(menu=menu_bar)

    file_order = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Режим игры", menu=file_order)
    file_order.add_command(label="Обычный", command=end_hard)
    file_order.add_command(label="Сложный", command=start_hard)

    file_music = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Музыка", menu=file_music)
    file_music.add_command(label="Включить", command=play_music)
    file_music.add_command(label="Остановить", command=stop_music)
    file_music.add_command(label="Переключение", command=switch_music)
    file_music.add_command(label="Громкость", command=show_volume_slider)


def play_music():
    global song_index, playlist, is_stopping
    is_stopping = False
    for file_name in os.listdir("sounds"):
        if file_name.endswith(".mp3"):
            playlist.append(os.path.join("sounds", file_name))
    if playlist:
        pygame.mixer.music.load(playlist[song_index])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)


def stop_music():
    global is_stopping
    is_stopping = True
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    else:
        print("Музыка не играет.")


def switch_music():
    global song_index, playlist
    song_index = (song_index + 1) % len(playlist)
    play_music()


def show_volume_slider():
    volume_slider.place(x=260, y=1)
    volume_slider.lift()
    window.bind("<Button-1>", hide_volume_slider, add="+")


def hide_volume_slider(event):
    if event.widget != volume_slider:
        volume_slider.place_forget()
        window.unbind("<Button-1>")


def adjust_volume(volume):
    pygame.mixer.music.set_volume(float(volume))


def check_event():
    global is_stopping
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if not is_stopping:
                switch_music()
    window.after(100, check_event)


def auto_click():
    global dino_count, speed
    if not hard:
        n = 0
        while n < dino_count:
            button_click()
            n += 1
        window.after(speed, auto_click)


def dino_cliker(upgrade_key):
    global check, coeff, upgrade_end_count, dino_count, speed
    cost = upgrade_costs[upgrade_key]
    if check >= cost:
        check -= cost
        if upgrade_key == "upgrade_dino":
            dino_count += 1
            upgrade_costs[upgrade_key] = int(cost * 3)
        elif upgrade_key == "upgrade_dino_speed":
            speed = int(speed/np.sqrt(2))
            upgrade_costs[upgrade_key] = int(cost * 12)
        update_labels()
        if dino_count == 1:
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
            messagebox.showinfo("вредный разработчик", "Слишком много умножений уже сделано)")
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
        messagebox.showinfo("Точно всё хорошо", "ЖИВИ! Не бей разраба!")
        coeff = 1


def change_color():     # на главную кнопку
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
                brightness > 90):
            # Форматирование цвета в шестнадцатеричном формате
            return "#{:06x}".format(color)


def rebirth(step=0):
    global check, coeff, rebirth_count, upgrade_end_count, upgradexx_count, dino_count, speed, field_color
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
        dino_count = 0
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


def show_page(page_index):
    global current_page
    current_page = page_index
    for i in range(31):
        globals()[f'button{i}'].place_forget()
        globals()[f'label_upgrade{i}'].place_forget()
    offset = page_index * 10
    for i in range(10):
        if offset + i >= 31:
            break
        globals()[f'button{offset + i}'].place(x=950, y=5 + i * 45)
        globals()[f"label_upgrade{offset + i}"].place(x=1250, y=5 + i * 45)
def previous_page():
    show_page((current_page - 1) % 4)
def next_page():
    show_page((current_page + 1) % 4)


def dino_labels(count):
    global images_dino
    images_dino.clear()
    dino1 = Image.open("images/dino 1.jpeg").resize((40, 40), Image.Resampling.LANCZOS)
    dino2 = Image.open("images/dino 2.jpg").resize((40, 40), Image.Resampling.LANCZOS)

    # не забываем, i начальное = 0
    for i in range(count):
        if i < 10:
            images_dino.append(ImageTk.PhotoImage(dino1))
            canvas.create_image(410 + (i * 40), 225, image=images_dino[i])
        elif (i >= 10) and (i < 20):
            images_dino.append(ImageTk.PhotoImage(dino2))
            canvas.create_image(410 + ((i - 10) * 40), 265, image=images_dino[i])
        i += 1


def update_labels():
    global dino_count
    labels = {f"label_upgrade{i}": f"Цена: {format_number(upgrade_costs[f'upgrade{i}'])}" for i in range(31)}
    labels.update({
        "label_check": f"Счёт: {format_number(check)}",
        "label_coeff": f"Сила клика: ×{format_number(coeff)}",
        "label_rebirth": f"Ребитхи: {rebirth_count}",
        "label_upgradeX": f"Последних улучшений: {upgrade_end_count}/5",
        "label_upgradex2": f"Цена: {format_number(upgrade_costs['upgradex2'])}",
        "label_upgradex3": f"Цена: {format_number(upgrade_costs['upgradex3'])}",
        "label_upgrade_dino": f"Цена: {format_number(upgrade_costs['upgrade_dino'])}",
        "label_upgrade_dino_speed": f"Цена: {format_number(upgrade_costs['upgrade_dino_speed'])}",
        "label_dino": f": {dino_count}    Скорость раз в: {speed} мс"
    })

    for label, text in labels.items():
        globals()[label].config(text=text, bg=field_color)

    dino_labels(dino_count)


def start_hard():
    global hard, button_text2
    hard = True
    button_text2 = canvas.create_text(200, 220, text="Правда я куда-то убегаю)", fill="black")


def move_button():
    global button_main
    window.update_idletasks()
    x = random.randint(50, 1200)
    y = random.randint(50, 700)
    if rebirth_count < 3:
        canvas.coords(button_main, x, y, x + 300, y + 300)
    elif (rebirth_count >= 3) and (rebirth_count < 6):
        canvas.coords(button_main, x, y, x + 300, y + 300)
    else:
        canvas.coords(button_main, x, y, x + 150, y + 300, x + 300, y + 300)


def end_hard():
    global hard, button_main, button_text2
    canvas.delete(button_text2)
    hard = False
    if rebirth_count < 3:
        canvas.coords(button_main, 50, 20, 350, 320)
    elif (rebirth_count >= 3) and (rebirth_count < 6):
        canvas.coords(button_main, 50, 450, 350, 750)
    else:
        canvas.coords(button_main, 200, 20, 50, 270, 350, 270)


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
        # Создаем треугольник с текстом
        button_main = canvas.create_polygon(200, 20, 50, 270, 350, 270, fill="green")
        button_text = canvas.create_text(200, 170, text="Нажми меня!", fill="black")
    canvas.tag_bind(button_main, "<Button-1>", button_click)
    canvas.tag_bind(button_text, "<Button-1>", button_click)
    return button_main, button_text


def button_click(event=None):
    global check, coeff
    check += coeff
    update_labels()
    change_color()
    if hard:
        move_button()
        check += coeff*(5 - 1)
    return check


# основная часть
window = tk.Tk()
window.title("Дино кликер")
window.geometry("1600x1000")
canvas = tk.Canvas(window, width=1600, height=1000)
window.iconbitmap('images/kursor.ico')
canvas.place(x=1, y=1)
canvas.config(bg="white")
field_color = canvas.cget("bg")
button_prev = tk.Button(window, text="Предыдущая страница", command=previous_page)
button_prev.place(x=980, y=460)
button_next = tk.Button(window, text="Следующая страница", command=next_page)
button_next.place(x=1255, y=460)

# красоту наводим
canvas.create_rectangle(900, 1, 1500, 450, outline="black", width=5)
canvas.create_rectangle(900, 450, 1500, 489, outline="black", width=5)
canvas.create_line(1200, 450, 1200, 490, fill="black", width=5)
canvas.create_rectangle(900, 492, 1500, 600, outline="gray", width=5)

# Открываем иконку курсора
dino = Image.open("images/dino 1.jpeg").resize((30, 30), Image.Resampling.LANCZOS)
dino = ImageTk.PhotoImage(dino)
canvas.create_image(35, 415, image=dino)

button_text2 = canvas.create_text(200, 220, text="Правда я куда-то убегаю)", fill="black")
volume_slider = tk.Scale(window, from_=1, to=0, resolution=0.1, orient=tk.VERTICAL, showvalue=False,
                         command=lambda v: adjust_volume(float(v)))
volume_slider.place_forget()


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
buttonRebirth = tk.Button(window, text=" МЕТЕОРИТ! ", font=("Comic Sans MS", 16, "italic bold"), fg="green",
                          command=lambda: rebirth_condition(), width=30)
buttonRebirth.place(x=400, y=1)

for i in range(0, 31):
    value = increment[i]
    upgrade_button = tk.Button(window, text=f"улучшение на {value}", font=("Comic Sans MS", 12, "italic bold"),
                               command=partial(upgrade, f"upgrade{i}", value))
    upgrade_button.config(width=20)
    globals()[f'button{i}'] = upgrade_button
    label = tk.Label(window, text=f"Цена: {format_number(upgrade_costs[f'upgrade{i}'])}",
                     font=("Comic Sans MS", 16, "bold"), fg="purple")
    globals()[f'label_upgrade{i}'] = label

# кнопки умножения
buttonx2 = tk.Button(window, text="умножение на 2", font=("Comic Sans MS", 12, "italic bold"),
                     command=lambda: upgrade("upgradex2", 2), width=20)
buttonx2.place(x=950, y=500)
label_upgradex2 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgradex2'])}",
                           font=("Comic Sans MS", 14, "bold"), fg="purple")
label_upgradex2.place(x=1250, y=500)
buttonx3 = tk.Button(window, text="умножение на 3", font=("Comic Sans MS", 12, "italic bold"),
                     command=lambda: upgrade("upgradex3", 3), width=20)
buttonx3.place(x=950, y=550)
label_upgradex3 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgradex3'])}",
                           font=("Comic Sans MS", 14, "bold"), fg="purple")
label_upgradex3.place(x=1250, y=550)

# доп помощники кликать
button_dino = tk.Button(window, text=" Дино помогут!",
                        command=lambda: dino_cliker("upgrade_dino"), width=20, height=2)
button_dino.place(x=50, y=350)
label_upgrade_dino = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade_dino'])}",
                              font=("Comic Sans MS", 12, "bold"), fg="purple")
label_upgrade_dino.place(x=210, y=355)
button_dino_speed = tk.Button(window, text=" +К скорости Дино",
                              command=lambda: dino_cliker("upgrade_dino_speed"), width=23, height=2)
button_dino_speed.place(x=450, y=350)
label_upgrade_dino_speed = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade_dino_speed'])}",
                                    font=("Comic Sans MS", 12, "bold"), fg="purple")
label_upgrade_dino_speed.place(x=630, y=355)
label_dino = tk.Label(window, text=f": {dino_count}    Скорость раз в: {speed} мс",
                      font=("Comic Sans MS", 12, "bold"), fg="purple")
label_dino.place(x=50, y=400)


play_music()
figure()
check_event()
window.update()
show_page(current_page)
update_labels()
create_menu()

window.mainloop()
