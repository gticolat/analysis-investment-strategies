import sqlite3


class CryptocurrencyModel:

    def __init__(self):
        self.con = sqlite3.connect('Database/strategy_analysis.db')
        self.cur = self.con.cursor()
        self.table = "SA_CryptoMonnaie"

    def commit(self):
        # Save (commit) the changes
        self.con.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    def select_all(self):
        query = "SELECT id_cryptomonnaie, symbole, name, rank FROM " + self.table

        self.cur.execute(query)
        rows = self.cur.fetchall()

        return rows

    def select_uses(self):
        query = """SELECT """ + self.table + """.id_cryptomonnaie, symbole, name, rank
                FROM """ + self.table + """
                INNER JOIN SA_DonneesHistorique ON """ + self.table + """.id_cryptomonnaie =  SA_DonneesHistorique.id_cryptomonnaie
                GROUP BY """ + self.table + """.id_cryptomonnaie"""

        self.cur.execute(query)
        rows = self.cur.fetchall()

        return rows

    def select_id_from_symbol(self, symbole):
        query = "SELECT id_cryptomonnaie FROM "+ self.table +" WHERE symbole = ?"

        self.cur.execute(query, [symbole])
        row = self.cur.fetchone()

        if row is None:
            id_crypto = -1
        else:
            id_crypto = row[0]

        return id_crypto

    def select_id_from_name(self, name):
        query = "SELECT id_cryptomonnaie FROM " + self.table + " WHERE name = ?"

        self.cur.execute(query, [name])
        row = self.cur.fetchone()

        return row[0]



    def insert(self, value):
        query = "INSERT INTO " + self.table + " (id_cryptomonnaie, symbole, name, rank)  VALUES (?, ?, ?, ?)"

        self.cur.executemany(query, value)
        self.commit()
