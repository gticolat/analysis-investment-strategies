from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np


class Utils:

    def reformat_date(self, date, preformat, postformat):
        date = datetime.strptime(date, preformat)
        return date.strftime(postformat)

    def valid_date(self, date):
        result = True
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            result = False
        return result

    def diff_date(self, date1, date2):
        result = True
        date1 = datetime.strptime(date1, "%d-%m-%Y")
        date2 = datetime.strptime(date2, "%d-%m-%Y")
        date0 = timedelta()

        if (date2 - date1) <= date0:
            result = False

        return result

    def valid_date_for_analysis(self, start_date, end_date, coin_begin_date, error_start_date, error_end_date):
        result = False

        valid_date = 0
        error_start_date.set("")
        error_end_date.set("")

        if self.valid_date(start_date) is False:
            error_start_date.set("Le format de la date est incorrect.")
        else:
            if self.diff_date(coin_begin_date, start_date) is False:
                error_start_date.set("La date de début doit être ultérieur à la date " + coin_begin_date + ".")
            else:
                valid_date = valid_date + 1

        if self.valid_date(end_date) is False:
            error_end_date.set("Le format de la date est incorrect.")
        else:
            now = date.today()
            if self.diff_date(end_date, now.strftime("%d-%m-%Y")) is False:
                error_end_date.set("La date de fin doit être antérieur à la date d'aujourd'hui.")
            else:
                valid_date = valid_date + 1

        if valid_date == 2:
            if self.diff_date(start_date, end_date) is False:
                error_end_date.set("La date de fin doit être ultérieur à la date de début.")
            else:
                result = True

        return result

    def genDateEndFixed(self, start_date, end_date):

        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

        # On génère un ndarray qui va de la date de départ à la date de fin incrémenté d'un jour
        invest_start_date =  np.arange(start_date,
                                       (end_date - relativedelta(months=1)),
                                       relativedelta(days=1)).astype(datetime)

        size_invest_start_date = invest_start_date.size
        invest_start_date = invest_start_date.reshape(size_invest_start_date, 1)

        invest_end_date = np.full((size_invest_start_date, 1), end_date)

        return np.concatenate((invest_start_date, invest_end_date), axis=1)

    def genDateWithInterval(self, start_date, end_date, intervalle):

        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

        # On génère un ndarray qui va de la date de départ à la date de fin moins l'intervale incrémenté d'un jour
        invest_start_date = np.arange(start_date,
                                      (end_date - relativedelta(months=intervalle)),
                                      relativedelta(days=1)).astype(datetime)

        # On récupère le nombre d'entrée du tableau
        size_invest_start_date = invest_start_date.size

        # On transforme le tableau en tableau à deux dimensions pour pouvoir le concaténer par la suite
        invest_start_date = invest_start_date.reshape(size_invest_start_date, 1)

        invest_end_date = np.arange((start_date + relativedelta(months=intervalle)),
                                    end_date,
                                    relativedelta(days=1)).astype(datetime)
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



