# всякие значения
import tkinter as tk
from tkinter import messagebox


class GameModel:
    def __init__(self):
        self.check = 0
        self.rebirth_count = 0
        self.upgrade_costs = {
            "upgrade0": 25,
            "upgrade1": 100,
            "upgrade2": 300,
            "upgrade3": 800,
            "upgrade4": 2100,
            "upgrade5": 5500,
            "upgrade6": 15000,
            "upgrade7": 42000,
            "upgrade8": 200000,
            "upgrade9": 550000,
            "upgrade10": 1500000,
            "upgrade11": 4000000,
            "upgrade12": 9500000,
            "upgrade13": 15000000,
            "upgrade14": 21000000,
            "upgrade15": 50000001,
            "upgrade16": 90000001,
            "upgradex2": 50000,
            "upgradex3": 1500000,
            "upgrade_mouse": 1000,
            "upgrade_mouse_speed": 20000
        }

        self.upgrade_costs_start = {
            "upgrade0": 25,
            "upgrade1": 100,
            "upgrade2": 300,
            "upgrade3": 800,
            "upgrade4": 2100,
            "upgrade5": 5500,
            "upgrade6": 15000,
            "upgrade7": 42000,
            "upgrade8": 200000,
            "upgrade9": 550000,
            "upgrade10": 1500000,
            "upgrade11": 4000000,
            "upgrade12": 9500000,
            "upgrade13": 15000000,
            "upgrade14": 21000000,
            "upgrade15": 50000001,
            "upgrade16": 90000001,
            "upgradex2": 50000,
            "upgradex3": 1500000,
            "upgrade_mouse": 1000,
            "upgrade_mouse_speed": 20000
        }

        self.increment = [
            1, 2, 5, 8, 11, 17, 30, 50, 70, 130, 200, 300, 450, 750, 1000, 1500, 123
        ]

        self.check = 0
        self.coeff = 1
        self.upgrade_end_count = 0
        self.upgradexx_count = 0
        self.mouses = 0
        self.speed = 10000
        pass

    def get_upgrade_cost(self, upgrade_name):
        return self.upgrade_costs.get(upgrade_name, 0)

    def rebirth(self, step=0):
        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFFFFF", "#000000"]
        colors *= 7
        if step < len(colors):
            self.view.canvas.config(bg=colors[step])
            self.view.window.after(30, self.rebirth, step + 1)
        else:
            self.view.canvas.config(bg=self.random_color())
            field_color = self.view.canvas.cget("bg")
            if field_color == "purple":
                self.view.canvas.config(bg=self.random_color())
            self.rebirth_count += 1
            self.check = 0
            self.coeff = 1
            self.upgrade_end_count = 0
            self.upgradexx_count = 0
            self.mouses = 0
            self.speed = 10000
            for key in self.upgrade_costs:
                self.upgrade_costs_start[key] = int(self.upgrade_costs_start[key] * 2)
                self.upgrade_costs[key] = int(self.upgrade_costs_start[key])
            self.view.update_labels()
            self.view.figure()
            self.view.buttonRebirth.config(state=tk.NORMAL)



    def rebirth_condition(self):
        if self.upgrade_end_count >= 5:
            self.view.buttonRebirth.config(state=tk.DISABLED)
            self.rebirth()
        else:
            messagebox.showinfo("Ребитх", "Необходимо улучшить последнее улучшение пять раз!")

    def format_number(self, number):
        return "{:,}".format(number).replace(",", " ")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def button_click(self, event=None):
        self.check += self.coeff
        self.view.update_labels()
        self.view.change_color()
        return self.model.check
