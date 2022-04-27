import sqlite3


class AnalysisModel:

    def __init__(self):
        self.con = sqlite3.connect('Database/strategy_analysis.db')
        self.cur = self.con.cursor()
        self.table = "SA_Analyse"

    def commit(self):
        # Save (commit) the changes
        self.con.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    def select_last_id(self):
        query = """SELECT MAX(id_analyse)
        FROM """ + self.table + """
        """

        self.cur.execute(query)
        row = self.cur.fetchall()

        return row[0][0]

    def insert(self, datetime):
        query = """INSERT INTO """ + self.table + """(date_heure)
        VALUES (?)
        """

        self.cur.execute(query, [datetime])

        self.commit()