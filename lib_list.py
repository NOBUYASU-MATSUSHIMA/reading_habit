import requests
import json
from pprint import pprint
import pandas as pd

def api_data():  
    url = "https://api.calil.jp/library?appkey={key}&pref={pref}&city={city}&format=json&callback="
    res = url.format(key="542e9b990d7470446df1c68aa8891e71", pref="福岡県", city="福岡市")

    api_data = requests.get(res).json()

    extracted_data = []  # 抽出したデータを格納するリスト

    # APIから取得したデータを処理して、必要な情報を抽出する
    for data in api_data:
        extracted_data.append({
            "formal": data.get("formal", ""),   # "formal" キーの値を取得し、存在しない場合は空文字列を返す
            "address": data.get("address", ""), # "address" キーの値を取得し、存在しない場合は空文字列を返す
            "tel": data.get("tel", "")          # "tel" キーの値を取得し、存在しない場合は空文字列を返す
        })

    return extracted_data

# データを取得してデータフレームに変換
extracted_data = api_data()
df = pd.DataFrame(extracted_data)

# CSVファイルにデータを保存
csv_file_path = "library_data.csv"
df.to_csv(csv_file_path, index=False)
print("CSVファイルを保存しました:", csv_file_path)

# CSVファイルを読み込む
csv_file_path = "library_data.csv"
df = pd.read_csv(csv_file_path)

# データフレームの内容を表示
print(df)
