import requests
import json
from pprint import pprint
import pandas as pd
import folium

"""
reversed_geocode=[]
def get_lib_map():
"""   
url="https://api.calil.jp/library?appkey={key}&pref={pref}&city={city}&format=json&callback=" ""
url=url.format(key="542e9b990d7470446df1c68aa8891e71",pref="福岡県",city="福岡市")

json_data=requests.get(url).json()

m=folium.Map(location=[33.388598, 131.388598],zoom_start=16)
maps=[]
for map in maps:
    geocode=json_data[i]["geocode"]
    reversed_geocode = [geocode[1:], geocode[0:]]  # 緯度と経度を反転
    
    folium.Marker(reversed_geocode).add_to(m)

m.save("lib_map.html")
pprint(reversed_geocode)

#get_lib_map()

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

    
    

