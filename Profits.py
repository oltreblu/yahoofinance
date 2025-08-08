import json
from pathlib import Path
import yfinance
import random
import string

def insert():
    path = Path('Investments.json')
    file_exceptions(path)
    file_text = path.read_text()

    if not file_text or file_text == '[]':
        print("There are no current investments!")
        user_choice = input("What do you want to do? (N)othing or (A)dd investments?")
        investments = []
    else:
        user_choice = input("What do you want to do? (N)othing, (M)odify or (A)dd investments?")
        investments = json.loads(file_text)

    if 'n' in user_choice.lower():
        return

    elif 'm' in user_choice.lower():
        print("Here are the current investments:")
        for investment in investments:
            print(investment['name'])

        stop_while = False
        while True:
            user_choice = input("Which one do you want to modify?: ")
            i = 0
            for investment in investments:
                if user_choice == investment['name']:
                    investment_to_modify = investment
                    stop_while = True
                    break
                i += 1
            if stop_while:
                break
            print("Error: Not Found. Try Again. (To stop try CTRL + C)")

        user_choice = input("Please select if you want to (A)dd, (R)emove or remove all (S)tocks.")
        if 'a' in user_choice.lower():
            number_stocks, value = modify_stocks('a')

            investment_to_modify['value'] = ((investment_to_modify['value'] *
                                              investment_to_modify['stocks_bought'] + value * number_stocks)
                                             / (number_stocks + investment_to_modify['stocks_bought']))

            investment_to_modify['stocks_bought'] += number_stocks
            print("Done!")
        elif 'r' in user_choice.lower():
            number_stocks = modify_stocks('r')
            investment_to_modify['stocks_bought'] -= number_stocks
            if investment_to_modify['stocks_bought'] <= 0:
                print("There are no stocks left! Removing the investment!")
                del investments[i]
                change_file_name()

            print("Done!")
        else:
            change_file_name()
            del investments[i]

    else:
        print("Warning! Be careful of using the right ticker! You might get the wrong numbers!")
        new_investment = {'name': '', 'value': 0, 'stocks_bought': 0, 'ticker': ''}

        while True:
            try:
                name, value, stocks_bought, ticker = input(
                    "Please tell me the (name,value,stocks bought,ticker) in the same format: ").strip().split(',')
                value = float(value)
                stocks_bought = int(stocks_bought)
                ticker = ticker.upper()
                if len(yfinance.Ticker(ticker).info) < 2:
                    print("The ticker is not valid, Try Again.")
                    continue
                for investment in investments:
                    if name == investment['name'] or ticker == investment['ticker']:
                        print("The investment is already inside!")
                        return
                name.strip().lower()
                break
            except ValueError:
                print("Error! Try Again!")
        i = 0
        values = [name, value, stocks_bought, ticker]
        for key in new_investment:
            new_investment[key] = values[i]
            i += 1
        investments.append(new_investment)
        print("Done!")
    path.write_text(json.dumps(investments))


def file_exceptions(path):
    try:
        try_path = Path(path)
        try_path_text = try_path.read_text()
        if not try_path.read_text():
            try_path.write_text('[]')
    except FileNotFoundError:
        file = open(path, 'w')
        file.write('[]')
        file.close()

def modify_stocks(remove_or_add):
    if remove_or_add == 'a':
        text_print = "Please insert the number of stocks and the value to add in the format (stocks,value): "
        while True:
            try:
                number_stocks, value = input(text_print).strip().split(',')
                number_stocks = int(number_stocks)
                value = float(value)
                return number_stocks, value
            except ValueError:
                print("Try Again.")
    else:
        text_print = "Please insert the number of stocks to remove in the format (stocks): "
        while True:
            try:
                number_stocks = input(text_print).strip()
                number_stocks = int(number_stocks)
                return number_stocks
            except ValueError:
                print("Try Again.")

def change_file_name():
    try:
        with open('Stocks_file', 'r') as file:
            text = file.read()
            open('Stocks_file', 'w')
        file_name = ''
        for digit_in_name in range(10):
            file_name += random.choice(list(string.ascii_lowercase))
        with open(file_name, 'w') as file:
            file.write(text)

    except FileNotFoundError:
        return

if __name__ == '__main__':
    insert()
