import yfinance
from datetime import datetime
import time
class Investment:
    def __init__(self, ticker, bought_value, stocks_bought):
        self.ticker = ticker
        self.bought_value = bought_value
        self.stocks_bought = stocks_bought

    def add_stocks(self, number_stocks, price):
        self.bought_value = (self.bought_value * self.stocks_bought + price * number_stocks) / (
            number_stocks + self.stocks_bought
        )
        self.stocks_bought += number_stocks

    def remove_stocks(self, number_stocks):
        self.stocks_bought -= number_stocks

sp500 = Investment('CSSPX.MI', 100, 400)
investments = [sp500]

def main():
    datas = [yfinance.Ticker(investment.ticker) for investment in investments]
    datas_info = [data.info for data in datas]
    prices = [data_info['regularMarketPrice'] for data_info in datas_info]
    profits = []
    values = {}
    i = 0
    now = datetime.now()
    formatted_date = now.strftime(f'%H:%M\t%d-%m-%Y')
    for investment in investments:
        values[investment] = prices[i]
        profits.append((float(values[investment]) - investment.bought_value) * investment.stocks_bought)
        i += 1
    readable_file = open('Stocks_file', 'r').read()
    if datetime.now().strftime('%d-%m-%Y') in readable_file:
        lines = readable_file.split('\n')
        del lines[-1]
        with open('Stocks_file', 'w') as file:
            print("ATTENTION! YOU ALREADY SCANNED TODAY!")
            print(f"The profits are: {sum(profits)}")
            final_text = ''
            for line in lines[:len(lines) - 1]:
                final_text += line + '\n'
            final_text += f'{formatted_date}\t {sum(profits)}\n'
            file.write(final_text)
    else:
        file = open('Stocks_file', 'a')
        print(f"The profits are: {sum(profits)}")
        file.write(f"{formatted_date}\t {sum(profits)}\n")
        file.close()

main()
time.sleep(1.3)