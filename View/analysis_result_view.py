from tkinter import ttk
import tkinter as tk


class AnalysisResultView:

    def __init__(self, controller: 'ProfitechController'):

        self.controller = controller
        self.frame = ""

    def afficher(self, id_analyse):
        plt = self.controller.histogram(self.controller.get_portfolios(id_analyse))
        plt.grid(row=0, column=1)

    def close(self):
        self.frame.destroy()