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

# 欠損値補完
# 今回は休業日が欠損値なので0で埋める
df['y'] = df['y'].fillna(0)
df['Bargain'] = df['Bargain'].fillna(0)
df['Weather'] = df['Weather'].fillna(0)

df.info()

print(df.describe().T)

subset_for_stats = df[df['y'] > 0]['y']
Q1 = subset_for_stats.quantile(0.25)
Q3 = subset_for_stats.quantile(0.75)
IQR = Q3 - Q1

# 上限・下限の設定 (1.5倍)
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 数値的な外れ値候補 (通常の範囲を超えているか)
is_numeric_outlier = (df['y'] < lower_bound) | (df['y'] > upper_bound)

# 除外(保護)条件: イベント(1) または 売上が0
# weatherやbargainが 1 のとき、または y が 0 のときは True
is_protected = (df['Weather'] == 1) | (df['Bargain'] == 1) | (df['y'] == 0)

# 「数値的に外れ値」かつ「保護対象ではない」ものを抽出
final_outliers_mask = is_numeric_outlier & (~is_protected)

# 該当する行を確認
print("--- 除去対象となる外れ値データ ---")
print(df[final_outliers_mask])

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

# モデル評価
lb.model_eva(df, True, True, events, 365)