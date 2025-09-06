# Author - Vedang Sunilkumar Sharma
# Description: Console app to analyze stock percent changes over a date range.

import datetime
import yfinance as yf

def getStock(stkInput, dayInput):
    dt = datetime.date.today()
    dtPast = dt - datetime.timedelta(days=dayInput)
    dfStock = yf.download(stkInput, start=dtPast, end=dt, progress=False)
    dfStock = dfStock[["Close", "Volume"]].dropna()
    return dfStock

print("-" * 30 + " \nStock Report Menu Options ")
print("-" * 30)

while True:
    user_input = str.lower(input("\n1. Report changes for a stock\n2. Quit\nYour Selected Option: "))

    if user_input == "2":
        print("We hate to say goodbye. Please, visit us again later!")
        break

    if user_input == "1":
        stock_input = input("Please enter the ticker symbol of the Stock on which you'd like a report on: ")
        num_days = int(input("Please enter the number of days for the analysis: "))

        df = getStock(stock_input, num_days)

        df["Volume % Change"] = 0.0
        df["Close % Change"] = 0.0

        for i in range(1, len(df)):
            prev_volume = df.iloc[i - 1]["Volume"]
            curr_volume = df.iloc[i]["Volume"]
            vol_change = ((curr_volume - prev_volume) / prev_volume) * 100
            df.iloc[i, df.columns.get_loc("Volume % Change")] = round(vol_change, 2)

            prev_close = df.iloc[i - 1]["Close"]
            curr_close = df.iloc[i]["Close"]
            close_change = ((curr_close - prev_close) / prev_close) * 100
            df.iloc[i, df.columns.get_loc("Close % Change")] = round(close_change, 2)

        print("*" * 60)
        print(f"Daily Percent Changes - {df.index[0].date()} to {df.index[-1].date()} * {stock_input.upper()} *")
        print("*" * 60)
        print("Date        Close      Volume     Volume % Change (%)     Close % Change (%)")

        for i in range(len(df)):
            date = df.index[i].strftime("%Y-%m-%d")
            close = float(df.iloc[i]["Close"])
            volume = int(df.iloc[i]["Volume"])
            vol_change = float(df.iloc[i]["Volume % Change"])
            close_change = float(df.iloc[i]["Close % Change"])
            print(f"{date:<12}{close:<12.2f}{volume:<12}{vol_change:<20.2f}{close_change:<20.2f}")
