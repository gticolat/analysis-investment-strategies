import sqlite3


class HistoricalDataModel:

    def __init__(self):
        self.con = sqlite3.connect('Database/strategy_analysis.db')
        self.cur = self.con.cursor()
        self.table = "SA_DonneesHistorique"

    def commit(self):
        # Save (commit) the changes
        self.con.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    def select(self, coin_name):
        query = """ SELECT date_donnees_historique, prix
                    FROM """ + self.table + """ DH
                    INNER JOIN SA_CryptoMonnaie CM ON DH.id_cryptomonnaie = CM.id_cryptomonnaie
                    WHERE CM.name = ?
        """

        self.cur.execute(query, [coin_name])
        rows = self.cur.fetchall()

        return rows

    def select_first_date(self, coin_name):
        query = """SELECT MIN(date_donnees_historique)
                    FROM """ + self.table + """ DH
                    INNER JOIN SA_CryptoMonnaie CM ON DH.id_cryptomonnaie = CM.id_cryptomonnaie
                    WHERE CM.name = ?
        """

        self.cur.execute(query, [coin_name])
        row = self.cur.fetchall()

        return row[0][0]

    def insert(self, value):
        query = "INSERT INTO " + self.table + " (date_donnees_historique, prix, id_cryptomonnaie)  VALUES (?, ?, ?)"

        self.cur.executemany(query, value)

        self.commit()

    def delete(self, id_cryptomonnaie):
        query = """DELETE FROM """ + self.table + """
                WHERE id_cryptomonnaie = ?"""

        self.cur.execute(query, [id_cryptomonnaie])

        self.commit()
