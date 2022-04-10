import sqlite3


class DatabaseInit:

    def __init__(self):
        # self.con = sqlite3.connect('../Database/strategy_analysis.db')
        self.con = sqlite3.connect('Database/strategy_analysis.db')
        self.cur = self.con.cursor()
        self.createInit()

    def commit(self):
        # Save (commit) the changes
        self.con.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    def createInit(self):
        # Create table at program first launch
        self.cur.execute("CREATE TABLE IF NOT EXISTS SA_CryptoMonnaie (id_cryptomonnaie int PRIMARY KEY, symbole varchar(10), libelle varchar(50))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS SA_DonneesHistorique (date_donnees_historique date, prix real, id_cryptomonnaie int, PRIMARY KEY(date_donnees_historique, id_cryptomonnaie), FOREIGN KEY (id_cryptomonnaie) REFERENCES SA_CryptoMonnaie (id_cryptomonnaie))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS SA_Utilisateur (id_utilisateur int PRIMARY KEY, pseudo varchar(100), mdp varchar(100))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS SA_StrategieFonction (id_fonction int PRIMARY KEY , libelle varchar(100), fonction varchar(250))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS SA_Analyse (id_analyse int PRIMARY KEY)")

    def insert(self):
        # Insert a row of data
        self.cur.execute("INSERT INTO stocks VALUES ('2006-04-05', 'BUY', 'MSFT', 1000, 72.0)")

    def select(self):
        for row in self.cur.execute('SELECT * FROM stocks ORDER BY price'):
            print(row)