import sqlite3


class OrdreVenteModel:

    def __init__(self):
        self.con = sqlite3.connect('Database/strategy_analysis.db')
        self.cur = self.con.cursor()
        self.table = "SA_OrdreVente"

    def commit(self):
        # Save (commit) the changes
        self.con.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    def select(self, id_portfolio):
        query = """SELECT date_donnees_historique, montant
        FROM """ + self.table + """
        WHERE id_portfolio = ?
        """

        self.cur.execute(query, [id_portfolio])
        rows = self.cur.fetchall()

        return rows

    def insert(self, ordre_vente):
        query = """INSERT INTO """ + self.table + """(id_portfolio, date_donnees_historique, id_cryptomonnaie, montant)
        VALUES(?, ?, ?, ?)
        """

        self.cur.executemany(query, ordre_vente)

        self.commit()