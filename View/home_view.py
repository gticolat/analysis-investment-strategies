from tkinter import ttk


class HomeView:

    def __init__(self, controller: 'ProfitechController'):

        self.controller = controller
        self.frame = ""

    def afficher(self):

        self.frame = ttk.Frame(self.controller.window, padding=10)
        self.frame.grid()

        ttk.Button(self.frame, text="Analyser", command=lambda: self.controller.switch_frame(self, self.controller.analysis_view)).grid(column=0, row=1)
        ttk.Button(self.frame, text="Historique des analyses").grid(column=0, row=2)
        ttk.Button(self.frame, text="Liste des cryptomonnaies", command=lambda: self.controller.switch_frame(self, self.controller.cryptocurrency_list_view)).grid(column=0, row=3)

    def close(self):
        self.frame.destroy()


