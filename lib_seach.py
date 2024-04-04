import requests
import json
from pprint import pprint

url="https://api.calil.jp/library?appkey={key}&pref={pref}&city={city}&format=json&callback=" ""
url=url.format(key="542e9b990d7470446df1c68aa8891e71",pref="福岡県",city="福岡市")

json_data=requests.get(url).json()
formal=json_data[0]["formal"]
pprint(formal)
