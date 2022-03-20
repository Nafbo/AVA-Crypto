import requests as rq
import json
import pandas as pd

API_KEY = "ckey_4e20bd1de6b3424c81eefbd7157"
chain_id ="1"
adress = "0xb1adceddb2941033a090dd166a462fe1c2029484"

url = "https://api.covalenthq.com/v1/{}/address/{}/stacks/compound/acts/?key={}".format(chain_id, adress, API_KEY)

result = rq.get(url).json()['data']['items']
df = pd.DataFrame(result)
df = df.set_index('act_at')

print(df)
