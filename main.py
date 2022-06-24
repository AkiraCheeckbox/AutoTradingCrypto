import bybit
from dotenv import load_dotenv
import ccxt
import pandas as pd
import time

load_dotenv()

import os
API_KEY = os.getenv('API')
SECRET = os.getenv('SECRET_KEY')



#何秒ごとに価格を収集するか
interval = 5

#何ドル分取引するか
quantity = 100

#25個で計算した短期移動平均と75個で計算した長期移動平均のクロスを判定に使う
short_sma_duration = 25
long_sma_duration = 75


client = bybit.bybit(test=True, api_key=API_KEY, api_secret=SECRET)


#初めの100期間は何もせず価格収集する
def price_data_collecting(samples=100):
    prices = []
    for _ in range(samples):
        last_price = client.Market.Market_symbolInfo(symbol="BTCUSD").result()[0]["result"][0]["last_price"]
        prices.append(last_price)
        time.sleep(interval)
        return prices

print("今からしばらくの間（デフォルトで100*5=500秒間）、BTCUSDの価格データを収集します（しばらく何も表示されません）。")
BTCUSD_initial_data = price_data_collecting()

#週したデータをpandasの出たフレームに格納。
#今後の計算もデータフレームを使って行う

df = pd.DataFrame()
df["BTCUSD"] = BTCUSD_initial_data

while True:
    #最新価格を取得
    last_price = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
    df=df.append({'BTCUSD': last_price,}, ignore_index=True)

    #移動平均を計算する
    df["short_sma"]=df["BTCUSD"].rolling(short_sma_duration).mean()
    df["long_sma"]=df["BTCUSD"].rolling(long_sma_duration).mean()

    #ゴールデンクロス（短期移動平均が長期移動平均を下からつきぬける）
    if df["short_sma"].iloc[-1]>df["long_sma"].iloc[-1] and df["short_sma"].iloc[-2]<df["long_sma"].iloc[-2]:
        print("ロングポジションを取ります。")
        print(client.Order.Order_new(side="Buy",symbol="BTCUSD",order_type="Market",qty=quantity,time_in_force="GoodTillCancel").result())

    #デッドクロス(ゴールデンクロスの逆)
    elif df["short_sma"].iloc[-1]<df["long_sma"].iloc[-1] and df["short_sma"].iloc[-2]>df["long_sma"].iloc[-2]:
        print("ショートポジションを取ります。")
        print(client.Order.Order_new(side="Sell",symbol="BTCUSD",order_type="Market",qty=quantity,time_in_force="GoodTillCancel").result())

    else:
        print("２つの移動平均線はクロスしていません。")

    #先頭行を削除してdfの長さを一定に保つ（長時間の運用時のメモリ対策）
    df=df.drop(df.index[0])

    time.sleep(interval)