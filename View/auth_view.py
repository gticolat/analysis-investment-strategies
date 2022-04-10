from tkinter import *
import tkinter as tk
from tkinter import ttk


class AuthView:

    def __init__(self, controller: 'ProfitechController'):
        # self.controller.window = Tk()

        # self.controller.window.title("Profitech Analysis")
        # self.controller.window.geometry("720x480")
        # self.controller.window.minsize(480, 360)

        self.controller = controller
        self.frame = ""

    def afficher(self):
        self.frame = ttk.Frame(self.controller.window, padding=10)
        self.frame.grid()

        label_username = ttk.Label(self.frame, text="Nom d'utilisateur")
        input_username = ttk.Entry(self.frame)
        label_password = ttk.Label(self.frame, text="Mot de passe")
        input_password = ttk.Entry(self.frame, show='•')

        var_error_message = tk.StringVar()
        label_error_message = ttk.Label(self.frame, textvariable=var_error_message)

        label_username.grid(column=0, row=0)
        input_username.grid(column=0, row=1)
        label_password.grid(column=0, row=2)
        input_password.grid(column=0, row=3)
        label_error_message.grid(column=0, row=5)

        ttk.Button(self.frame, text="Connexion",
                   command=lambda: self.controller.auth_user(input_username.get(), input_password.get(),
                                                        var_error_message)).grid(column=0, row=4)

    def close(self):
        self.frame.destroy()


