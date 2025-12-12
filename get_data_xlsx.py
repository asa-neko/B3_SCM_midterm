def get_data(url,file_path):
    import requests
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)
        
        print(f"Excelファイル{file_path}が正常に保存されました！")
    except requests.exceptions.RequestException as e:
        print(f"ダウンロード中にエラーが発生しました：{e}")

url = "http://misc.0093.tv/misc/apparel.xlsx"
file_path = "data/data.xlsx"

get_data(url,file_path)