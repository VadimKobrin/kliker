# контроллер, мозг
#from A_model import GameModel
#from A_view import GameView
from tkinter import messagebox
import os
import json
import stat


class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.increment = self.model.increment
        self.field_color = None
        self.upgrade_costs = self.model.upgrade_costs
        self.upgrade_costs_start = None
        self.button_text = None

    def increase_score(self, points):
        self.model.increase_score(points)
        self.view.update_score(self.model.score)

    def rebirth_condition(self):
        self.model.rebirth_condition()
        self.view.update_rebirth_count(self.model.rebirth_count)

    def upgrade(self, upgrade_key, increment_value):
        cost = self.model.get_upgrade_cost(upgrade_key)
        if self.model.check >= cost:
            if (upgrade_key == "upgradex2" or upgrade_key == "upgradex3") and self.model.upgradexx_count <= 5:
                self.model.upgradexx_count += 1
                self.model.coeff *= increment_value
                self.model.set_upgrade_cost(upgrade_key, int(cost * 10))
            elif (upgrade_key == "upgradex2" or upgrade_key == "upgradex3") and self.model.upgradexx_count > 5:
                self.view.show_message("я вредный", "Слишком много умножений уже сделано)))")
                self.model.check += cost
            else:
                self.model.coeff += increment_value
                self.model.set_upgrade_cost(upgrade_key, int(cost * 1.3))
            if upgrade_key == "upgrade16":
                self.model.upgrade_end_count += 1
            self.model.check -= cost
            self.view.update_labels()
        else:
            self.view.show_message("Посмотри на циферки", f"Нужно {self.model.format_number(cost)} кликов")

    def mouse_cliker(self, upgrade_key):
        cost = self.model.get_upgrade_cost(upgrade_key)
        if self.model.check >= cost:
            self.model.check -= cost
            if upgrade_key == "upgrade_mouse":
                self.model.mouses += 1
                self.model.set_upgrade_cost(upgrade_key, int(cost * 3))
            elif upgrade_key == "upgrade_mouse_speed":
                self.model.speed = int(self.model.speed / 2)
                self.model.set_upgrade_cost(upgrade_key, int(cost * 10))
            self.view.update_labels()
            if self.model.mouses == 1:
                self.auto_click()
        else:
            self.view.show_message("Посмотри на циферки", f"Нужно {self.model.format_number(cost)} кликов")

    def format_number(self, number):
        return f"{number:,}"

    def get_upgrade_cost(self, upgrade_name):
        return self.model.upgrade_costs.get(upgrade_name, 0)

    def get_increment_value(self, index):
        return self.model.get_increment_value(index)

    def get_mouses(self):
        return self.model.mouses

    def get_speed(self):
        return self.model.speed

    def auto_click(self):
        n = 0
        while n < self.model.mouses:
            self.button_click()
            n += 1
        self.view.schedule_auto_click(self.model.speed, self.auto_click)

    def button_click(self, event=None):
        self.model.check += self.model.coeff
        self.view.update_labels()
        self.view.change_color()
        return self.model.check

    def save(self):
        shape_type = "oval" if self.rebirth_count < 3 else "rectangle" if self.rebirth_count < 6 else "oval"

        if not os.path.exists("result.txt"):
            with open("result.txt", "w", encoding="utf-8") as file:
                pass

        button_coords = []
        button_text_coords = []

        if self.button_main is not None and self.button_text is not None:
            if isinstance(self.button_main, (str, int)) and isinstance(self.button_text, (str, int)):
                button_coords = self.view.canvas.coords(self.button_main)
                button_text_coords = self.view.canvas.coords(self.button_text)
            else:
                messagebox.showinfo("xyita", "Invalid button_main or button_text!")
        else:
            messagebox.showinfo("xyita", "da, xyita!")

        button_text_content = self.view.canvas.itemcget(self.button_text, "text") if self.button_text else ""
        button_color = self.view.canvas.itemcget(self.button_main, "fill") if self.button_main else ""
        self.field_color = self.view.canvas.cget("bg")

        data = {
            "check": self.check,
            "coeff": self.coeff,
            "rebirth_count": self.rebirth_count,
            "upgrade_end_count": self.upgrade_end_count,
            "upgradexx_count": self.upgradexx_count,
            "upgrade_costs": self.upgrade_costs,
            "upgrade_costs_start": self.upgrade_costs_start,
            "button_coords": button_coords,
            "button_color": button_color,
            "button_text_coords": button_text_coords,
            "button_text_content": button_text_content,
            "field_color": self.field_color,
            "shape_type": shape_type,
            "mouses": self.mouses,
            "speed": self.speed
        }

        try:
            os.chmod("result.txt", stat.S_IWRITE)

            with open("result.txt", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            os.chmod("result.txt", stat.S_IREAD)
            messagebox.showinfo("Сохранение", "Данные сохранены!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    pass

    def take_data(self):
        if self.button_main is not None:
            self.view.canvas.delete(self.button_main)
        if self.button_text is not None:
            self.view.canvas.delete(self.button_text)

        try:
            with open("result.txt", 'r', encoding="utf-8") as file:
                data = json.load(file)

            self.check = data["check"]
            self.coeff = data["coeff"]
            self.rebirth_count = data["rebirth_count"]
            self.upgrade_end_count = data["upgrade_end_count"]
            self.upgradexx_count = data["upgradexx_count"]
            self.upgrade_costs = data["upgrade_costs"]
            self.upgrade_costs_start = data["upgrade_costs_start"]
            button_coords = data["button_coords"]
            button_color = data["button_color"]
            button_text_coords = data["button_text_coords"]
            button_text_content = data["button_text_content"]
            self.field_color = data["field_color"]
            shape_type = data["shape_type"]
            self.mouses = data["mouses"]
            self.speed = data["speed"]

            # Восстанавливаем кнопку, текст, фон
            if shape_type == "oval":
                self.button_main = self.view.canvas.create_oval(*button_coords, fill=button_color)
            elif shape_type == "rectangle":
                self.button_main = self.view.canvas.create_rectangle(*button_coords, fill=button_color)
            else:
                self.button_main = self.view.canvas.create_oval(*button_coords, fill=button_color)

            self.button_text = self.view.canvas.create_text(*button_text_coords, text=button_text_content, fill="black")
            self.view.canvas.tag_bind(self.button_main, "<Button-1>", self.view.button_click)
            self.view.canvas.tag_bind(self.button_text, "<Button-1>", self.view.button_click)
            self.view.canvas.config(bg=self.field_color)

            self.view.update_labels()

            if self.mouses > 0:
                self.view.auto_click()

            return (self.check, self.coeff, self.rebirth_count, self.upgrade_end_count, self.upgradexx_count,
                    self.upgrade_costs, self.upgrade_costs_start, self.button_main, self.button_text, self.mouses, self.speed, self.field_color)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            return None


    @property
    def check(self):
        return self.model.check

    @property
    def coeff(self):
        return self.model.coeff

    @property
    def upgrade_end_count(self):
        return self.model.upgrade_end_count

    @property
    def upgradexx_count(self):
        return self.model.upgradexx_count

    @property
    def mouses(self):
        return self.model.mouses

    @property
    def speed(self):
        return self.model.speed

    @property
    def score(self):
        return self.model.self

    @property
    def rebirth_count(self):
        return self.model.rebirth_count

    pass
