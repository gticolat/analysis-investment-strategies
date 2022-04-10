import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
import seaborn as sns


class Visualization:

    def averageProfitTotal(self, categories, profit_percent, profit_dollar):
        x = np.arange(len(categories))
        width = 0.2
        fig, ax = plt.subplots()

        ax.set_title('Profit moyen en fonction de la stratégie')

        color = 'tab:orange'
        rects1 = ax.bar(x - width / 2, profit_percent, width, label='Profit en pourcentage', color=color)
        ax.set_ylabel('Pourcentage')
        ax.set_xticks(x, categories)

        color = 'tab:blue'
        ax2 = ax.twinx()
        rects2 = ax2.bar(x + width / 2, profit_dollar, width, label='Profit en dollars', color=color)
        ax2.set_ylabel('Dollars')

        ax.bar_label(rects1, padding=3)
        ax2.bar_label(rects2, padding=3)

        ax.legend(handles=[rects1, rects2])
        fig.tight_layout()

        plt.show()
        # plt.savefig("average_profit_strat.png")

    def profit_percent_by_interval(self, interval, profit_percent):
        x = interval
        y = profit_percent

        fig, ax = plt.subplots()
        ax.set_title('Profit moyen en fonction de l\'intervalle')
        ax.set_ylabel('Pourcentage')
        ax.set_xlabel('Intervalle en mois')
        ax.set_xticks(x)
        ax.set_yticks(y)

        ax.plot(x, y, linewidth=2.0)

        plt.show()

    def portfolio_heatmap_profit(self, portfolios, filename):
        date_achat = []
        date_vente = []
        profit = []

        for one_portfolio in portfolios:
            # date_achat.append(datetime.datetime.strptime(one_portfolio.get_date_buy()[0], "%d-%m-%Y"))
            # date_vente.append(datetime.datetime.strptime(one_portfolio.get_sell_date()[0], "%d-%m-%Y"))
            date_achat.append(pd.to_datetime(one_portfolio.get_date_buy()[0], format="%d-%m-%Y"))
            date_vente.append(pd.to_datetime(one_portfolio.get_sell_date()[0], format="%d-%m-%Y"))
            profit.append(float(((one_portfolio.get_sell_earn() - one_portfolio.get_money_invested()) / one_portfolio.get_money_invested()) * 100))


        dataset = {'date achat': date_achat, 'date vente': date_vente, 'profit': profit}

        dataframe = pd.DataFrame(data=dataset)
        dataframe = pd.pivot_table(dataframe, index='date achat', columns='date vente', values='profit')

        plt.figure(figsize=(16, 16))

        sns.heatmap(dataframe)

        plt.show()
        # plt.savefig(filename, dpi=600)



    def portfolio_3d(self, portfolios):
        xAmplitudes = np.random.exponential(10, 10000)  # your data here
        yAmplitudes = np.random.normal(50, 10, 10000)  # your other data here - must be same array length

        x = np.array(xAmplitudes)  # turn x,y data into numpy arrays
        y = np.array(yAmplitudes)  # useful for regular matplotlib arrays

        fig = plt.figure()  # create a canvas, tell matplotlib it's 3d
        ax = fig.add_subplot(111, projection='3d')

        # make histogram stuff - set bins - I choose 20x20 because I have a lot of data
        hist, xedges, yedges = np.histogram2d(x, y, bins=(20, 20))
        xpos, ypos = np.meshgrid(xedges[:-1] + xedges[1:], yedges[:-1] + yedges[1:])

        xpos = xpos.flatten() / 2.
        ypos = ypos.flatten() / 2.
        zpos = np.zeros_like(xpos)

        dx = xedges[1] - xedges[0]
        dy = yedges[1] - yedges[0]
        dz = hist.flatten()

        cmap = cm.get_cmap('jet')  # Get desired colormap - you can change this!
        max_height = np.max(dz)  # get range of colorbars so we can normalize
        min_height = np.min(dz)
        # scale each z to [0,1], and get their rgb values
        rgba = [cmap((k - min_height) / max_height) for k in dz]

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
        plt.title("X vs. Y Amplitudes for ____ Data")
        plt.xlabel("My X data source")
        plt.ylabel("My Y data source")
        #plt.savefig("Your_title_goes_here")
        plt.show()


        '''
        xAmplitudes = np.random.exponential(10, 10000)  # your data here
        yAmplitudes = np.random.normal(50, 10, 10000)  # your other data here - must be same array length

        x = np.array(xAmplitudes)  # turn x,y data into numpy arrays
        y = np.array(yAmplitudes)  # useful for regular matplotlib arrays

        fig = plt.figure()  # create a canvas, tell matplotlib it's 3d
        ax = fig.add_subplot(111, projection='3d')

        # make histogram stuff - set bins - I choose 20x20 because I have a lot of data
        hist, xedges, yedges = np.histogram2d(x, y, bins=(20, 20))
        xpos, ypos = np.meshgrid(xedges[:-1] + xedges[1:], yedges[:-1] + yedges[1:])

        xpos = xpos.flatten() / 2.
        ypos = ypos.flatten() / 2.
        zpos = np.zeros_like(xpos)

        dx = xedges[1] - xedges[0]
        dy = yedges[1] - yedges[0]
        dz = hist.flatten()

        cmap = cm.get_cmap('jet')  # Get desired colormap - you can change this!
        max_height = np.max(dz)  # get range of colorbars so we can normalize
        min_height = np.min(dz)
        # scale each z to [0,1], and get their rgb values
        rgba = [cmap((k - min_height) / max_height) for k in dz]

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
        plt.title("X vs. Y Amplitudes for ____ Data")
        plt.xlabel("My X data source")
        plt.ylabel("My Y data source")
        # plt.savefig("Your_title_goes_here")
        plt.show()
        '''

