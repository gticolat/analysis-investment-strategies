from tkinter import ttk
import tkinter as tk


class AnalysisView:

    def __init__(self, controller: 'ProfitechController'):

        self.controller = controller
        self.frame = ""

        self.strat = tk.StringVar(value="dca")
        self.freq = tk.StringVar(value="monthly")
        self.intervalle = tk.IntVar(value=0)

    def afficher(self):

        coins = self.controller.get_cryptocurrencies_uses()
        coin_name = []
        for coin in coins:
            coin_name.append(coin[2])

        self.frame = ttk.Frame(self.controller.window, padding=10)
        self.frame.grid()

        ttk.Label(self.frame, text="Séléctionnez les paramètres de l'analyse : ").grid(row=0, column=0)

        ttk.Label(self.frame, text="Séléctionnez la cryptomonnaie à tester : ").grid(row=1, column=0)

        crypto_choose = ttk.Combobox(self.frame, state="readonly", values=coin_name)
        crypto_choose.grid(row=2, column=0)
        crypto_choose.current(0)

        ttk.Label(self.frame, text="Séléctionnez la stratégie à tester : ").grid(row=3, column=0)

        frame_strat = ttk.Frame(self.frame, padding=10)
        frame_strat.grid(row=4, column=0)

        dca_radiobutton = ttk.Radiobutton(frame_strat, text="Dollar Cost Averaging", variable=self.strat, value="dca", width=20)
        va_radiobutton = ttk.Radiobutton(frame_strat, text="Value Averaging", variable=self.strat, value="va", width=20)
        lump_sum_radiobutton = ttk.Radiobutton(frame_strat, text="Lump Sum", variable=self.strat, value="ls", width=20)

        dca_radiobutton.grid(row=0, column=0)
        va_radiobutton.grid(row=0, column=1)
        lump_sum_radiobutton.grid(row=0, column=2)

        ttk.Label(self.frame, text="Séléctionnez la fréquence d'achat : ").grid(row=6, column=0)

        frame_freq = ttk.Frame(self.frame, padding=10)
        frame_freq.grid(row=7, column=0)

        monthly_radiobutton = ttk.Radiobutton(frame_freq, text="Mensuelle", variable=self.freq, value="monthly", width=15)
        weekly_radiobutton = ttk.Radiobutton(frame_freq, text="Hebdomadaire", variable=self.freq, value="weekly", width=15)

        monthly_radiobutton.grid(row=0, column=0)
        weekly_radiobutton.grid(row=0, column=1)

        ttk.Label(self.frame, text="Séléctionnez l'intervalle entre l'ordre d'achat et de vente : ").grid(row=8, column=0)

        frame_intervalle = ttk.Frame(self.frame, padding=10)
        frame_intervalle.grid(row=9, column=0)

        no_intervalle_radiobutton = ttk.Radiobutton(frame_intervalle, text="Sans intervalle", variable=self.intervalle, value="0",
                                                    width=15)
        months3_radiobutton = ttk.Radiobutton(frame_intervalle, text="3 mois", variable=self.intervalle, value="3",
                                              width=10)
        months6_radiobutton = ttk.Radiobutton(frame_intervalle, text="6 mois", variable=self.intervalle, value="6",
                                             width=10)
        months12_radiobutton = ttk.Radiobutton(frame_intervalle, text="12 mois", variable=self.intervalle, value="12",
                                             width=10)
        months24_radiobutton = ttk.Radiobutton(frame_intervalle, text="24 mois", variable=self.intervalle, value="24",
                                             width=10)

        no_intervalle_radiobutton.grid(row=0, column=0)
        months3_radiobutton.grid(row=0, column=1)
        months6_radiobutton.grid(row=0, column=2)
        months12_radiobutton.grid(row=0, column=3)
        months24_radiobutton.grid(row=0, column=4)

        ttk.Label(self.frame, text="Séléctionnez la date de début d'achat (jj-mm-aaaa) : ").grid(row=10, column=0)
        error_start_date = tk.StringVar()

        start_date = ttk.Entry(self.frame)
        start_date.grid(row=11, column=0)

        ttk.Label(self.frame, textvariable=error_start_date).grid(row=12, column=0)

        ttk.Label(self.frame, text="Séléctionnez la date de fin d'achat (jj-mm-aaaa) : ").grid(row=13, column=0)
        error_end_date = tk.StringVar()

        end_date = ttk.Entry(self.frame)
        end_date.grid(row=14, column=0)

        ttk.Label(self.frame, textvariable=error_end_date).grid(row=15, column=0)

        ttk.Label(self.frame, text="Séléctionnez le prix à investir (100 par défaut) : ").grid(row=16, column=0)

        price = ttk.Entry(self.frame)
        price.grid(row=17, column=0)

        progress_bar = ttk.Progressbar(self.frame, orient="horizontal", mode="determinate", length=280)

        ttk.Button(self.frame, text="Lancer l'analyse", command=lambda: self.controller.analysis(
            crypto_choose.get(),
            self.strat.get(),
            self.freq.get(),
            self.intervalle.get(),
            start_date.get(),
            end_date.get(),
            price.get(),
            error_start_date,
            error_end_date,
            progress_bar)).grid(row=18, column=0)

        progress_bar.grid(row=20, column=0)

    def close(self):
        self.frame.destroy()