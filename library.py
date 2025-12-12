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

# モデル評価
def model_eva(df, weekly_seasonal, yearly_seasonal, holidays, periods):
    import pandas as pd
    from prophet import Prophet
    from sklearn.metrics import mean_absolute_error
    import matplotlib.pyplot as plt
    import numpy as np
    import japanize_matplotlib

    # データの分割（最後の365日をテスト用に設定）
    train_df = df.iloc[:-periods].copy()
    test_df = df.iloc[-periods:].copy()

    # モデルの構築
    model = Prophet(weekly_seasonality=weekly_seasonal,yearly_seasonality=yearly_seasonal,holidays=holidays)
    model.fit(train_df)

    # テスト期間と同じ日付のデータフレームを作成
    future_test = test_df[['ds','Weather','Bargain']].copy()
    forecast = model.predict(future_test)

    # MAE計算
    comparison_df = pd.DataFrame({
        'y_true': test_df['y'].values,
        'y_pred': forecast['yhat'].values,
    }).dropna()

    mae = mean_absolute_error(comparison_df['y_true'], comparison_df['y_pred'])
    print('----------------------------------------------------------------------------------')
    print(f"モデルの精度(MAE): {mae:.2f}")
    print(f"解釈：　予測は平均して、実績から±{mae:.0f}ズレている。")
    print('----------------------------------------------------------------------------------')

    # 視覚的な評価
    plt.figure(figsize=(15, 6))

    # 学習データ
    plt.plot(
        pd.to_datetime(train_df['ds']).values, 
        train_df['y'].values, 
        label='学習データ(Train)', color='gray', alpha=0.5
    )

    # 実測値（テストデータ）
    plt.plot(
        pd.to_datetime(test_df['ds']).values, 
        test_df['y'].values, 
        label='実測値(Test)', color='black'
    )

    # 予測値
    plt.plot(
        pd.to_datetime(forecast['ds']).values, 
        forecast['yhat'].values, 
        label='予測値(Forecast)', color='blue', alpha=0.8
    )

    plt.title('学習データ vs テストデータ vs 予測値')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True) 
    plt.show()