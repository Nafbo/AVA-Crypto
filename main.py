import requests as rq
import json
import pandas as pd


def wallet_balance(address):
    api_key = 'ckey_4e20bd1de6b3424c81eefbd7157'
    chain_id = '1' #ETH
    formatage = "balances_v2"  # ->Soldes / 'transactions_v2' -> Opérations / 'transfers_v2' -> Transfers
    
    api_url = 'https://api.covalenthq.com'
    endpoint = f'/v1/{chain_id}/address/{adress}/{formatage}/?key={api_key}'
    url = api_url + endpoint
    
    r = rq.get(url).json()['data']['items']
    
    df = pd.DataFrame(r)
    
    print(df)
    return

adress = "0xb1adceddb2941033a090dd166a462fe1c2029484"
wallet_balance(adress)
