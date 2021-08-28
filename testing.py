import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

# importing data and splitting into training and testing period
df = pd.read_csv('./data/USDT_XRP.csv')
train, test = train_test_split(df, test_size = 0.3, shuffle = False)

train['sma_20'] = train['close'].rolling(10).mean()
train['ema1'] = train['close'].ewm(alpha = 0.4, adjust = False).mean()
train[['close','sma_20', 'ema1']].plot(linewidth = 1)

plt.show()
