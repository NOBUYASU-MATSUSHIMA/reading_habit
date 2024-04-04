import requests
import json
from pprint import pprint
import pandas as pd

url="https://api.calil.jp/check?appkey={key}&isbn={isbn}&systemid={pref}&format=json&callback=no"
url=url.format(key="542e9b990d7470446df1c68aa8891e71",isbn="4798068535",pref="Fukuoka_Fukuoka")
jsondata=requests.get(url).json()
pprint(jsondata)

#https://api.calil.jp/check?appkey=542e9b990d7470446df1c68aa8891e71&isbn=4798068535&systemid=Fukuoka_Fukuoka&format=json&callback=no
