# library.py
def read_excel(url):
    import pandas as pd
    import openpyxl
    try:
        df = pd.read_excel(url)
    except FileNotFoundError:
        print("ファイルが見つかりませんでした。")
    df.head()
    return df

# 指定範囲の祝日を取得（開始年, 開始月, 開始日, 終了年, 終了月, 終了日）
def get_holiday(year1,month1,day1,year2,month2,day2):
    import jpholiday
    import datetime
    holiday = jpholiday.between(datetime.date(year1,month1,day1), datetime.date(year2,month2,day2))
    return holiday

def plot_line(x, y, xlabel, ylabel):
    import matplotlib.pyplot as plt
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

# 需要予測（データ, 週効果, 月効果, 祝日, 予測期間）
# イベントは雨やバーゲン、祝日などすべて含んでいる。
def prediction(df, weekly_seasonal, yearly_seasonal, holidays, periods):
    from prophet import Prophet
    # モデルの生成
    m = Prophet(weekly_seasonality=weekly_seasonal,yearly_seasonality=yearly_seasonal, holidays=holidays)
    m.fit(df)
    
    # 予測する日付を生成
    future = m.make_future_dataframe(periods=periods)

    # 予測を実施
    forecast = m.predict(future)

    # 実際のデータとトレンドを重ね合わせて表示
    fig1 = m.plot(forecast)

    # トレンドのみ表示
    fig2 = m.plot_components(forecast)

    fig1.show()
    input("Enterを押して次のグラフへ")
    fig2.show()
    input("Enterを押して表示終了")