# main.py
# 自作ライブラリーのインポート
import library as lb
# 他のライブラリーのインポート
import pandas as pd
import matplotlib

# データの読み込みと確認
url = "data/data.xlsx"
df = lb.read_excel(url)
print(df)

df['ds'] = pd.to_datetime(df["ds"])

df.info()

print(df.describe().T)

# 時系列プロット
lb.plot_line(df['ds'], df['y'], "timeline", "data")

#　祝日の取得
tmp = lb.get_holiday(1990,1,1,1993,12,31)
hd = [x[0] for x in tmp]
print(hd)

# 天候の日付を取得
ra = df["ds"][df["Weather"]==1]

# バーゲンの日付を取得
ev = df["ds"][df["Bargain"]==1]

# イベント効果の追加
h1 = pd.DataFrame({
    'holiday': 'e1',
    'ds': hd,
    'lower_window': 0,
    'upper_window': 0,
})

h2 = pd.DataFrame({
    'holiday': 'e2',
    'ds': ra,
    'lower_window': 0,
    'upper_window': 0,
})

h3 = pd.DataFrame({
    'holiday': 'e3',
    'ds': ev,
    'lower_window': 0,
    'upper_window': 0,
})

events = pd.concat((h1,h2,h3))

# イベント効果のみ考慮した需要予測
lb.prediction(df, True, True, events, 365)