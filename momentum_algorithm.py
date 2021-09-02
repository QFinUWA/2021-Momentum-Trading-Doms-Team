import pandas as pd
from talib.abstract import *

# local imports
from gemini_modules import engine

# read in data preserving dates
df = pd.read_csv("data/USDT_XRP.csv", parse_dates=[0])

# globals
training_period = 200

#backtesting
backtest = engine.backtest(df)

'''Algorithm function, lookback is a data frame parsed to function continuously until end of initial dataframe is reached.'''
def logic(account, lookback):
    try:
        today = len(lookback)-1
        if(today > training_period): 
            long_moving_average = lookback["close"][-200:].mean()  # update PMA
            short_moving_average = lookback["close"][-50:].mean()
            volumn_moving_average = lookback['volume'].rolling(window=training_period).mean()[today]  # update VMA

            if(long_moving_average < short_moving_average):
                #if(lookback['volume'][today] > volumn_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today])
            else:
                if(long_moving_average > short_moving_average):
                    #if(lookback['volume'][today] < volumn_moving_average):
                        for position in account.positions:
                                account.close_position(position, 1, lookback['close'][today]) 
    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset


if __name__ == "__main__":
    backtest.start(100, logic)
    backtest.results()
    backtest.chart()
