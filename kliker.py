import tkinter as tk
import os
import stat
from tkinter import messagebox
import random
import json
from PIL import Image, ImageTk

button = None
button_text = None
check = 0
coeff = 1
rebirth_count = 0
upgrade_end_count = 0
upgradexx_count = 0
mouses = 0
speed = 10000

upgrade_costs = {
    "upgrade1":  25,
    "upgrade2":  100,
    "upgrade3":  300,
    "upgrade4":  800,
    "upgrade5":  2100,
    "upgrade6":  5500,
    "upgrade7":  15000,
    "upgrade8":  42000,
    "upgrade9":  200000,
    "upgrade10": 550000,
    "upgrade11": 1500000,
    "upgrade12": 4000000,
    "upgrade13": 9500000,
    "upgrade14": 15000000,
    "upgrade15": 21000000,
    "upgrade16": 50000001,
    "upgrade17": 90000001,
    "upgradex2": 50000,
    "upgradex3": 1500000,
    "upgrade_mouse": 1000,
    "upgrade_mouse_speed": 20000
}

upgrade_costs_start = {
    "upgrade1":  25,
    "upgrade2":  100,
    "upgrade3":  300,
    "upgrade4":  800,
    "upgrade5":  2100,
    "upgrade6":  5500,
    "upgrade7":  15000,
    "upgrade8":  42000,
    "upgrade9":  200000,
    "upgrade10": 550000,
    "upgrade11": 1500000,
    "upgrade12": 4000000,
    "upgrade13": 9500000,
    "upgrade14": 15000000,
    "upgrade15": 21000001,
    "upgrade16": 50000001,
    "upgrade17": 90000001,
    "upgradex2": 50000,
    "upgradex3": 1500000,
    "upgrade_mouse": 1000,
    "upgrade_mouse_speed": 20000
}


def format_number(number):
    return "{:,}".format(number).replace(",", " ")


def save():
    global check, coeff, upgrade_costs, rebirth_count, upgrade_end_count, \
        upgrade_costs_start, upgradexx_count, button, button_text, mouses, speed, field_color

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

    if button is not None and button_text is not None:
        if isinstance(button, (str, int)) and isinstance(button_text, (str, int)):
            button_coords = canvas.coords(button)
            button_text_coords = canvas.coords(button_text)
        else:
            messagebox.showinfo("xyita", "Invalid button or button_text!")
    else:
        messagebox.showinfo("xyita", "da, xyita!")

    button_text_content = canvas.itemcget(button_text, "text") if button_text else ""
    button_color = canvas.itemcget(button, "fill") if button else ""
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
        upgrade_costs_start, upgradexx_count, button, button_text, mouses, speed, field_color

    if 'button' in globals():
        canvas.delete(button)
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
            button = canvas.create_oval(*button_coords, fill=button_color)
        elif shape_type == "rectangle":
            button = canvas.create_rectangle(*button_coords, fill=button_color)
        else:
            button = canvas.create_oval(*button_coords, fill=button_color)

        button_text = canvas.create_text(*button_text_coords, text=button_text_content, fill="black")
        canvas.tag_bind(button, "<Button-1>", button_click)
        canvas.tag_bind(button_text, "<Button-1>", button_click)
        canvas.config(bg=field_color)

        update_labels()

        if mouses > 0:
            auto_click()

        return (check, coeff, rebirth_count, upgrade_end_count, upgradexx_count,
                upgrade_costs, upgrade_costs_start, button, button_text, mouses, speed, field_color)

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


def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def change_color():
    global button
    if button is not None and isinstance(button, (str, int)):
        new_color = random_color()
        canvas.itemconfig(button, fill=new_color)
    else:
        messagebox.showinfo("Ошибка", "Кнопка не существует или имеет неверный тип!")


def auto_click():
    global mouses, button, speed
    i = 0
    while i < mouses:
        button_click()
        i += 1

    window.after(speed, auto_click)


def mouse_cliker(upgrade_key):
    global check, coeff, upgrade_end_count, mouses, speed
    cost = upgrade_costs[upgrade_key]
    if check >= cost:
        check -= cost
        if upgrade_key == "upgrade_mouse":
            mouses += 1
            upgrade_costs[upgrade_key] = int(cost * 3)
        elif upgrade_key == "upgrade_mouse_speed":
            speed = int(speed/2)
            upgrade_costs[upgrade_key] = int(cost * 10)
        update_labels()
        if mouses == 1:
            auto_click()
    else:
        messagebox.showinfo("Посмотри на циферки", f"Нужно {format_number(cost)} кликов")


def upgrade(upgrade_key, increment):
    global check, coeff, upgrade_end_count, upgradexx_count
    cost = upgrade_costs[upgrade_key]
    if check >= cost:
        if (upgrade_key == "upgradex2" or upgrade_key == "upgradex3") and upgradexx_count <= 5:
            upgradexx_count += 1
            coeff *= increment
            upgrade_costs[upgrade_key] = int(cost * 10)
        elif (upgrade_key == "upgradex2" or upgrade_key == "upgradex3") and upgradexx_count > 5:
            messagebox.showinfo("я вредный", "Слишком много умножений уже сделано)))")
            check += cost
        else:
            coeff += increment
            upgrade_costs[upgrade_key] = int(cost * 1.3)
        if upgrade_key == "upgrade17":
            upgrade_end_count += 1
        check -= cost
        update_labels()
    else:
        messagebox.showinfo("Посмотри на циферки", f"Нужно {format_number(cost)} кликов")


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
        if field_color == "purple":
            canvas.config(bg=random_color())
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
        button0.config(state=tk.NORMAL)


def rebirth_condition():
    global upgrade_end_count
    if upgrade_end_count >= 5:
        button0.config(state=tk.DISABLED)
        rebirth()
    else:
        messagebox.showinfo("Ребитх", "Необходимо улучшить последнее улучшение пять раз!")


def slider(value):
    value = int(value)
    koef_slider = 1
    button1.place(x=950, y=5 - value * koef_slider)
    button2.place(x=950, y=50 - value * koef_slider)
    button3.place(x=950, y=100 - value * koef_slider)
    button4.place(x=950, y=150 - value * koef_slider)
    button5.place(x=950, y=200 - value * koef_slider)
    button6.place(x=950, y=250 - value * koef_slider)
    button7.place(x=950, y=300 - value * koef_slider)
    button8.place(x=950, y=350 - value * koef_slider)
    button9.place(x=950, y=400 - value * koef_slider)
    button10.place(x=950, y=450 - value * koef_slider)
    button11.place(x=950, y=500 - value * koef_slider)
    button12.place(x=950, y=550 - value * koef_slider)
    button13.place(x=950, y=600 - value * koef_slider)
    button14.place(x=950, y=650 - value * koef_slider)
    button15.place(x=950, y=700 - value * koef_slider)
    button16.place(x=950, y=750 - value * koef_slider)
    button17.place(x=950, y=800 - value * koef_slider)

    buttonx2.place(x=950, y=950 - value * koef_slider)
    buttonx3.place(x=950, y=1000 - value * koef_slider)

    label_upgrade1.place(x=1250, y=5 - value * koef_slider)
    label_upgrade2.place(x=1250, y=50 - value * koef_slider)
    label_upgrade3.place(x=1250, y=100 - value * koef_slider)
    label_upgrade4.place(x=1250, y=150 - value * koef_slider)
    label_upgrade5.place(x=1250, y=200 - value * koef_slider)
    label_upgrade6.place(x=1250, y=250 - value * koef_slider)
    label_upgrade7.place(x=1250, y=300 - value * koef_slider)
    label_upgrade8.place(x=1250, y=350 - value * koef_slider)
    label_upgrade9.place(x=1250, y=400 - value * koef_slider)
    label_upgrade10.place(x=1250, y=450 - value * koef_slider)
    label_upgrade11.place(x=1250, y=500 - value * koef_slider)
    label_upgrade12.place(x=1250, y=550 - value * koef_slider)
    label_upgrade13.place(x=1250, y=600 - value * koef_slider)
    label_upgrade14.place(x=1250, y=650 - value * koef_slider)
    label_upgrade15.place(x=1250, y=700 - value * koef_slider)
    label_upgrade16.place(x=1250, y=750 - value * koef_slider)
    label_upgrade17.place(x=1250, y=800 - value * koef_slider)

    label_upgradex2.place(x=1250, y=950 - value * koef_slider)
    label_upgradex3.place(x=1250, y=1000 - value * koef_slider)


def update_labels():
    label_check.config(text=f"Счёт: {format_number(check)}", bg=field_color)
    label_coeff.config(text=f"Сила клика: ×{format_number(coeff)}", bg=field_color)
    label_rebirth.config(text=f"Ребитхи: {rebirth_count}", bg=field_color)
    label_upgradeX.config(text=f"Последних улучшений: {upgrade_end_count}/5", bg=field_color)
    label_upgrade1.config(text=f"Цена: {format_number(upgrade_costs['upgrade1'])}", bg=field_color)
    label_upgrade2.config(text=f"Цена: {format_number(upgrade_costs['upgrade2'])}", bg=field_color)
    label_upgrade3.config(text=f"Цена: {format_number(upgrade_costs['upgrade3'])}", bg=field_color)
    label_upgrade4.config(text=f"Цена: {format_number(upgrade_costs['upgrade4'])}", bg=field_color)
    label_upgrade5.config(text=f"Цена: {format_number(upgrade_costs['upgrade5'])}", bg=field_color)
    label_upgrade6.config(text=f"Цена: {format_number(upgrade_costs['upgrade6'])}", bg=field_color)
    label_upgrade7.config(text=f"Цена: {format_number(upgrade_costs['upgrade7'])}", bg=field_color)
    label_upgrade8.config(text=f"Цена: {format_number(upgrade_costs['upgrade8'])}", bg=field_color)
    label_upgrade9.config(text=f"Цена: {format_number(upgrade_costs['upgrade9'])}", bg=field_color)
    label_upgrade10.config(text=f"Цена: {format_number(upgrade_costs['upgrade10'])}", bg=field_color)
    label_upgrade11.config(text=f"Цена: {format_number(upgrade_costs['upgrade11'])}", bg=field_color)
    label_upgrade12.config(text=f"Цена: {format_number(upgrade_costs['upgrade12'])}", bg=field_color)
    label_upgrade13.config(text=f"Цена: {format_number(upgrade_costs['upgrade13'])}", bg=field_color)
    label_upgrade14.config(text=f"Цена: {format_number(upgrade_costs['upgrade14'])}", bg=field_color)
    label_upgrade15.config(text=f"Цена: {format_number(upgrade_costs['upgrade15'])}", bg=field_color)
    label_upgrade16.config(text=f"Цена: {format_number(upgrade_costs['upgrade16'])}", bg=field_color)
    label_upgrade17.config(text=f"Цена: {format_number(upgrade_costs['upgrade17'])}", bg=field_color)

    label_upgradex2.config(text=f"Цена: {format_number(upgrade_costs['upgradex2'])}", bg=field_color)
    label_upgradex3.config(text=f"Цена: {format_number(upgrade_costs['upgradex3'])}", bg=field_color)
    label_upgrade_mouse.config(text=f"Цена: {format_number(upgrade_costs['upgrade_mouse'])}", bg=field_color)
    label_upgrade_mouse_speed.config(text=f"Цена: {format_number(upgrade_costs['upgrade_mouse_speed'])}", bg=field_color)
    label_mouse.config(text=f": {mouses}    Скорость раз в: {speed} мс", bg=field_color)


def figure():
    global button, button_text, rebirth_count
    if 'button' in globals():
        canvas.delete(button)
    if 'button_text' in globals():
        canvas.delete(button_text)

    if rebirth_count < 3:
        # Создаем круг с текстом
        button = canvas.create_oval(50, 20, 350, 320, fill="yellow")
        button_text = canvas.create_text(200, 170, text="Нажми меня!", fill="black")
    elif (rebirth_count >= 3) and (rebirth_count < 6):
        # Создаем прямоугольник с текстом
        button = canvas.create_rectangle(50, 450, 350, 750, fill="yellow")
        button_text = canvas.create_text(200, 600, text="Нажми меня!", fill="black")
    else:
        # Создаем круг 2 с текстом
        button = canvas.create_oval(50, 20, 350, 320, fill="green")
        button_text = canvas.create_text(200, 170, text="Нажми меня!", fill="black")
    canvas.tag_bind(button, "<Button-1>", button_click)
    canvas.tag_bind(button_text, "<Button-1>", button_click)
    return button, button_text


def button_click(event=None):
    global check, coeff
    check += coeff
    update_labels()
    change_color()
    return check


#основная часть
window = tk.Tk()
window.title("Мое приложение")
window.geometry("1600x1000")
canvas = tk.Canvas(window, width=1600, height=1000)
canvas.place(x=1, y=1)
canvas.config(bg="white")
field_color = canvas.cget("bg")
slider = tk.Scale(window, from_=0, to=1000, orient="vertical", length=750, command=slider, showvalue=False)
slider.place(x=1500, y=0)

figure()
# Открываем иконку курсора
mouse_icon = Image.open("kursor.ico")
mouse_icon = mouse_icon.resize((15, 15), Image.LANCZOS)
mouse_icon = ImageTk.PhotoImage(mouse_icon)
# Создаем метку с иконкой мышки
label_mouse_icon = tk.Label(window, image=mouse_icon)
label_mouse_icon.image = mouse_icon
label_mouse_icon.place(x=17, y=405)
window.update()


#вывод данных
label_check = tk.Label(window, text="Счёт: 0", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_check.place(x=400, y=70)
label_coeff = tk.Label(window, text="Сила клика: ×1", font=("Times New Roman", 16, "italic"), fg="orange")
label_coeff.place(x=400, y=100)
label_rebirth = tk.Label(window, text="Ребитхи: 0", font=("Arial", 16, "bold"), fg="green")
label_rebirth.place(x=400, y=130)
label_upgradeX = tk.Label(window, text="Последних улучшений: 0/5", font=("Arial", 16, "bold"), fg="blue")
label_upgradeX.place(x=400, y=170)


#цена и апгрейд улучшений
label_upgrade1 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade1'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade1.place(x=1250, y=5)
label_upgrade2 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade2'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade2.place(x=1250, y=50)
label_upgrade3 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade3'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade3.place(x=1250, y=100)
label_upgrade4 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade4'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade4.place(x=1250, y=150)
label_upgrade5 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade5'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade5.place(x=1250, y=200)
label_upgrade6 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade6'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade6.place(x=1250, y=250)
label_upgrade7 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade7'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade7.place(x=1250, y=300)
label_upgrade8 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade8'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade8.place(x=1250, y=350)
label_upgrade9 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade9'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade9.place(x=1250, y=400)
label_upgrade10 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade10'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade10.place(x=1250, y=450)
label_upgrade11 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade11'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade11.place(x=1250, y=500)
label_upgrade12 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade12'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade12.place(x=1250, y=550)
label_upgrade13 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade13'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade13.place(x=1250, y=600)
label_upgrade14 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade14'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade14.place(x=1250, y=650)
label_upgrade15 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade15'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade15.place(x=1250, y=700)
label_upgrade16 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade16'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade16.place(x=1250, y=750)
label_upgrade17 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade17'])}", font=("Comic Sans MS", 16, "bold"), fg="purple")
label_upgrade17.place(x=1250, y=800)

#кнопки прибавления
button0 = tk.Button(window, text=" РЕБИТХ! ", font=("Comic Sans MS", 16, "bold"), fg="green",
                    command=lambda: rebirth_condition(), width=30, height=1)
button0.place(x=400, y=1)
button1 = tk.Button(window, text="улучшение на 1", command=lambda: upgrade("upgrade1", 1), width=30, height=2)
button1.place(x=950, y=5)
button2 = tk.Button(window, text="улучшение на 2", command=lambda: upgrade("upgrade2", 2), width=30, height=2)
button2.place(x=950, y=50)
button3 = tk.Button(window, text="улучшение на 5", command=lambda: upgrade("upgrade3", 5), width=30, height=2)
button3.place(x=950, y=100)
button4 = tk.Button(window, text="улучшение на 8", command=lambda: upgrade("upgrade4", 8), width=30, height=2)
button4.place(x=950, y=150)
button5 = tk.Button(window, text="улучшение на 11", command=lambda: upgrade("upgrade5", 11), width=30, height=2)
button5.place(x=950, y=200)
button6 = tk.Button(window, text="улучшение на 17", command=lambda: upgrade("upgrade6", 17), width=30, height=2)
button6.place(x=950, y=250)
button7 = tk.Button(window, text="улучшение на 30", command=lambda: upgrade("upgrade7", 30), width=30, height=2)
button7.place(x=950, y=300)
button8 = tk.Button(window, text="улучшение на 50", command=lambda: upgrade("upgrade8", 50), width=30, height=2)
button8.place(x=950, y=350)
button9 = tk.Button(window, text="улучшение на 70", command=lambda: upgrade("upgrade9", 70), width=30, height=2)
button9.place(x=950, y=400)
button10 = tk.Button(window, text="улучшение на 130", command=lambda: upgrade("upgrade10", 130), width=30, height=2)
button10.place(x=950, y=450)
button11 = tk.Button(window, text="улучшение на 200", command=lambda: upgrade("upgrade11", 200), width=30, height=2)
button11.place(x=950, y=500)
button12 = tk.Button(window, text="улучшение на 300", command=lambda: upgrade("upgrade12", 300), width=30, height=2)
button12.place(x=950, y=550)
button13 = tk.Button(window, text="улучшение на 450", command=lambda: upgrade("upgrade13", 450), width=30, height=2)
button13.place(x=950, y=600)
button14 = tk.Button(window, text="улучшение на 750", command=lambda: upgrade("upgrade14", 750), width=30, height=2)
button14.place(x=950, y=650)
button15 = tk.Button(window, text="улучшение на 1000", command=lambda: upgrade("upgrade15", 1000), width=30, height=2)
button15.place(x=950, y=700)
button16 = tk.Button(window, text="улучшение на 1500", command=lambda: upgrade("upgrade16", 1500), width=30, height=2)
button16.place(x=950, y=750)
button17 = tk.Button(window, text="улучшение на 123", command=lambda: upgrade("upgrade17", 123), width=30, height=2)
button17.place(x=950, y=800)

#кнопки умножения
buttonx2 = tk.Button(window, text="умножение на 2", command=lambda: upgrade("upgradex2", 2), width=30, height=2)
buttonx2.place(x=950, y=950)
label_upgradex2 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgradex2'])}", font=("Comic Sans MS", 14, "bold"), fg="purple")
label_upgradex2.place(x=1250, y=950)
buttonx3 = tk.Button(window, text="умножение на 3", command=lambda: upgrade("upgradex3", 3), width=30, height=2)
buttonx3.place(x=950, y=1000)
label_upgradex3 = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgradex3'])}", font=("Comic Sans MS", 14, "bold"), fg="purple")
label_upgradex3.place(x=1250, y=1000)

#доп мышки
button_mouse = tk.Button(window, text=" автомышкааа!!!", command=lambda: mouse_cliker("upgrade_mouse"), width=20, height=2)
button_mouse.place(x=50, y=350)
label_upgrade_mouse = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade_mouse'])}", font=("Comic Sans MS", 12, "bold"), fg="purple")
label_upgrade_mouse.place(x=210, y=355)
button_mouse_speed = tk.Button(window, text=" улучшение скорости мыши", command=lambda: mouse_cliker("upgrade_mouse_speed"), width=23, height=2)
button_mouse_speed.place(x=350, y=350)
label_upgrade_mouse_speed = tk.Label(window, text=f"Цена: {format_number(upgrade_costs['upgrade_mouse_speed'])}", font=("Comic Sans MS", 12, "bold"), fg="purple")
label_upgrade_mouse_speed.place(x=530, y=355)
label_mouse = tk.Label(window, text=f": {mouses}    Скорость раз в: {speed} мс", font=("Comic Sans MS", 12, "bold"), fg="purple")
label_mouse.place(x=30, y=400)


create_menu()

window.mainloop()
