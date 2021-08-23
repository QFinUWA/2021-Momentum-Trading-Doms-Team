import pandas as pd
from talib.abstract import *
from sklearn.model_selection import train_test_split

# local imports
from gemini_modules import engine

# read in data preserving dates
df = pd.read_csv("data/USDT_XRP.csv", parse_dates=[0])

# globals
TRAINING_PERIOD = 15
ALPHA = 0.3

#backtesting
# train, test = train_test_split(df, test_size = 0.3, shuffle = False)
backtest = engine.backtest(df)

'''Algorithm function, lookback is a data frame parsed to function continuously until end of initial dataframe is reached.'''
def logic(account, lookback):
    try:
        today = len(lookback)-1
        if(today > TRAINING_PERIOD):
            # indicator
            simple_moving_average = lookback['close'].rolling(window=TRAINING_PERIOD).mean()[today]  # update PMA
            exponential_moving_average = lookback['close'].ewm(alpha = ALPHA, adjust = False).mean()[today] # update EMA
            INDICATOR = exponential_moving_average

            # volume filter
            volumn_moving_average = lookback['volume'].rolling(window=TRAINING_PERIOD).mean()[today]  # update VMA



            if(lookback['close'][today] < INDICATOR):
                if(lookback['volume'][today] > volumn_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today])
            else:
                if(lookback['close'][today] > INDICATOR):
                    if(lookback['volume'][today] < volumn_moving_average):
                        for position in account.positions:
                                account.close_position(position, 1, lookback['close'][today])
    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset

def apply_fee(account):
    return 0.999


if __name__ == "__main__":
    backtest.start(100, logic)
    backtest.results()
    backtest.chart()
