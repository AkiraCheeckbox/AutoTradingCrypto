# %%
from email.utils import localtime
import os
import numpy as np
from pybit import inverse_perpetual
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime

import matplot

load_dotenv()

API_KEY = os.getenv('API')
SECRET = os.getenv('SECRET_KEY')

session = inverse_perpetual.HTTP(
    endpoint="https://api.bybit.com",
    api_key=API_KEY,
    api_secret=SECRET
)

ws = inverse_perpetual.WebSocket(
    test=False,
    api_key=API_KEY,
    api_secret=SECRET
)

jsonData = datas = session.query_mark_price_kline(
    symbol="BTCUSD",
    interval= "30",
    from_time = 1653408000
)["result"]

df =  pd.DataFrame.from_records(jsonData)

df["start_at"] = pd.to_datetime(df["start_at"],unit='s').dt.strftime("%H:%M")

# df

#ALGO
# high (H), intraday low (L), and closing price (C).
# H + L + C = X
# PivotPoint(P) = X/3
#
# FOMULA
# Y = P*2

# STEP 1 : Create DataFrame with Open High Low Close By Day

df_mod = df[["start_at","open","high","low","close"]]

# STEP 2 : Add New Column PivotPoint

df_mod['PivotPoint'] = (df_mod["high"] + df_mod["low"] + df_mod["close"])/3

df_mod.plot()

plt.show()
# STEP3: Y = P * 2


# First resistance level (R1) = Y – L


# Second resistance level (R2) = P + (H – L)


# First support level (S1) = Y – H


# Second support level (S2) = P – (H – L)



# Pivot Method
# First Starategy for buying time
# 価格が下落してS1・S2に到達：逆張り買いを仕掛ける
# ピボットラインやR1、R2が利食いターゲット
# S3到達したら損切する


