import requests as rq
import json
import pandas as pd

#%%
def fetch_wallet_balance(address):
    api_url = 'https://api.covalenthq.com'
    endpoint = f'/v1/1/address/{address}/balances_v2/'
    url = api_url + endpoint
    r = rq.get(url, auth=("ckey_4e20bd1de6b3424c81eefbd7157",''))
    print(r.json()['data']['items'])
    return(r.json())

#Example address request
fetch_wallet_balance('0xFEC4f9D5B322Aa834056E85946A32c35A3f5aDD8')


#%%
chain_id ="1" #ETH
adress = "0xb1adceddb2941033a090dd166a462fe1c2029484"
API_KEY = 'ckey_4e20bd1de6b3424c81eefbd7157'

url = "https://api.covalenthq.com/v1/{}/address/{}/stacks/compound/acts/?key={}".format(chain_id, adress, API_KEY)
url2 = "https://api.covalenthq.com/v1/{}/address/{}/balances_v2/?key={}".format(chain_id, adress, API_KEY)

result = rq.get(url2).json()['data']['items']
df = pd.DataFrame(result)
#df = df.set_index('act_at')

print(df.iloc[1])