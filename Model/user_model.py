import sqlite3


class UserModel:

    def __init__(self):
        self.con = sqlite3.connect('Database/strategy_analysis.db')
        self.cur = self.con.cursor()
        self.table = "SA_Utilisateur"

    def commit(self):
        # Save (commit) the changes
        self.con.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    def select_user(self, pseudo):
        query = "SELECT * FROM " + self.table + " WHERE pseudo = ?"

        self.cur.execute(query, [pseudo])
        row = self.cur.fetchone()

        return row

    # def select_password(self, pseudo):
    #     query = "SELECT mdp FROM " + self.table + " WHERE pseudo = ?"

    #     self.cur.execute(query, [pseudo])
    #     row = self.cur.fetchone()[0]

    #     return row
