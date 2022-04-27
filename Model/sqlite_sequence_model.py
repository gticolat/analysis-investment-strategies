import sqlite3


class SqliteSequenceModel:

    def __init__(self):
        self.con = sqlite3.connect('Database/strategy_analysis.db')
        self.cur = self.con.cursor()
        self.table = "sqlite_sequence"

    def commit(self):
        # Save (commit) the changes
        self.con.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    def select_seq(self, table_name):
        query = """SELECT seq
        FROM """ + self.table + """
        WHERE name = ?
        """

        self.cur.execute(query, [table_name])
        row = self.cur.fetchone()

        return row[0]