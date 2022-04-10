import numpy as np
from dateutil.relativedelta import relativedelta
import datetime


class DateInterval:

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def getStartDate(self):
        return self.start_date

    def getEndDate(self):
        return self.end_date

    def genDateEndFixed(self):

        # On génère un ndarray qui va de la date de départ à la date de fin incrémenté d'un jour
        invest_start_date =  np.arange(self.getStartDate(),
                                       (self.getEndDate() - relativedelta(months=1)),
                                       relativedelta(days=1)).astype(datetime.datetime)

        size_invest_start_date = invest_start_date.size
        invest_start_date = invest_start_date.reshape(size_invest_start_date, 1)

        invest_end_date = np.full((size_invest_start_date, 1), self.getEndDate())

        return np.concatenate((invest_start_date, invest_end_date), axis=1)

    def genDateWithInterval(self, interval):

        # On génère un ndarray qui va de la date de départ à la date de fin moins l'intervale incrémenté d'un jour
        invest_start_date = np.arange(self.getStartDate(),
                                      (self.getEndDate() - relativedelta(months=interval)),
                                      relativedelta(days=1)).astype(datetime.datetime)

        # On récupère le nombre d'entrée du tableau
        size_invest_start_date = invest_start_date.size

        # On transforme le tableau en tableau à deux dimensions pour pouvoir le concaténer par la suite
        invest_start_date = invest_start_date.reshape(size_invest_start_date, 1)

        invest_end_date = np.arange((self.getStartDate() + relativedelta(months=interval)),
                                    self.getEndDate(),
                                    relativedelta(days=1)).astype(datetime.datetime)
        size_invest_end_date = invest_end_date.size
        invest_end_date = invest_end_date.reshape(size_invest_end_date, 1)

        # On doit s'assurer que les deux tableaux fassent la même taille pour pouvoir les concaténer
        if size_invest_start_date > size_invest_end_date:
            invest_start_date = invest_start_date[:size_invest_end_date]

        elif size_invest_start_date < size_invest_end_date:
            invest_end_date = invest_end_date[:size_invest_start_date]

        # On concatène les deux tableaux, ils sont sous la forme :
        # [[date_debut, date_fin], [date_debut, date_fin]]
        return np.concatenate((invest_start_date, invest_end_date), axis=1)

