# основной файл
import tkinter as tk
from A_controller import GameController
from A_model import GameModel
from A_view import GameView

# основная часть
window = tk.Tk()
model = GameModel()
controller = GameController(model, None)
view = GameView(window, controller)
controller.view = view

window.mainloop()
