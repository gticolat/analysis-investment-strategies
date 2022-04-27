import sqlite3


class PortfolioModel:

    def __init__(self):
        self.con = sqlite3.connect('Database/strategy_analysis.db')
        self.cur = self.con.cursor()
        self.table = "SA_Portfolio"

    def commit(self):
        # Save (commit) the changes
        self.con.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    def select(self, id_analyse):
        query = """SELECT id_portfolio, frequence, intervalle, strat, montant_total_crypto, montant_total_investi, id_analyse
        FROM """ + self.table + """
        WHERE id_analyse = ?
        """

        self.cur.execute(query, [id_analyse])
        rows = self.cur.fetchall()

        return rows

    def select_last_id(self):
        query = """SELECT MAX(id_portfolio)
                FROM """ + self.table + """
                """

        self.cur.execute(query)
        row = self.cur.fetchall()

        return row[0][0]

    def insert(self, portfolios):
        query = """INSERT INTO """ + self.table + """(frequence, intervalle, strat, montant_total_crypto, montant_total_investi, id_analyse)
        VALUES(?, ?, ?, ?, ?, ?)
        """

        self.cur.executemany(query, portfolios)

        self.commit()


