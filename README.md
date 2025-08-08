# yahoofinance
Very simple python script that uses the yfinance library to lookup the current market price of some stocks, writes it into a file for future graphs.
Remember to install the yfinance library!
You can do so by using:

pip install yfinance

To add or modify the investments you made, just run the Insert.py file, you will be guided step by step.

-In this particular branch, it will save it in a file with the format -Time Date Investment_1 Investment_2 ... Sum_Of_Investments
Note that i did this really quickly and may have consistency issues as i have not yet tested it throughly. 
If you ever remove all stocks from an investment, the script will rename the previous 'Stocks_file' into a random named file, so that the format will be consistent.
