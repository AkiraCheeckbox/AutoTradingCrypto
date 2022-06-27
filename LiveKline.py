#%%
import os
from signal import pause
from pybit import inverse_perpetual
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import count
import time
from datetime import datetime as dt


load_dotenv()

API_KEY = os.getenv('API')
SECRET = os.getenv('SECRET_KEY')


ws = inverse_perpetual.WebSocket(
    test=False,
    api_key=API_KEY,
    api_secret=SECRET
)


plt.style.use('fivethirtyeight')


x_values = []
y_values = []

df = pd.DataFrame(y_values)

index = count()


def handle_kline(message):
    # I will be called every time there is new orderbook data!
    data = message["data"][0]
    price = data["high"]
    print(price)
    # tdatetime = dt.strptime(data["timestamp"], '%Y-%m-%dT%H:%M:%S.000Z')
    # strt = tdatetime.strftime('%m/%d %H:%M')
    # x_values.append(next(index))
    df.append(price)


def handle_message(message):
    # pprint(message, sort_keys=True, indent=4, separators=(",", ": "))
    print(message)



def animate(i):
    plt.cla()
    df.plot()
    # plt.xticks(x_values, rotation=45)


ws.kline_stream(handle_kline, "BTCUSD",interval="D")

ani = animation.FuncAnimation(plt.gcf(),animate,interval = 100)
plt.tight_layout()
plt.show()