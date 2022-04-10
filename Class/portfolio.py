class Portfolio:

    def __init__(self, date, btc_amount, money_invested, sell_date, sell_earn):
        self.date_buy = date
        self.btc_amount = btc_amount
        self.money_invested = money_invested
        self.sell_date = sell_date
        self.sell_earn = sell_earn

    def get_date_buy(self):
        return self.date_buy

    def get_btc_amount(self):
        return self.btc_amount

    def get_money_invested(self):
        return self.money_invested

    def get_sell_date(self):
        return self.sell_date

    def get_sell_earn(self):
        return self.sell_earn

    def set_date(self, date):
        self.date = date

    def set_btc_amount(self, btc_amount):
        self.btc_amount = btc_amount

    def set_money_invested(self, money_invested):
        self.money_invested = money_invested

    def set_sell_date(self, sell_date):
        self.sell_date = sell_date

    def set_sell_earn(self, sell_earn):
        self.sell_earn = sell_earn