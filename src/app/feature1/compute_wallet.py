import requests as rq
import json
import pandas as pd


def wallet_balance(address):
    """_summary_

    Args:
        address (_type_): _description_

    Returns:
        _type_: _description_
    """
    api_key = 'ckey_4e20bd1de6b3424c81eefbd7157'
    chain_id = '1' #ETH
    formatage = "balances_v2"  # ->Soldes / 'transactions_v2' -> Opérations / 'transfers_v2' -> Transfers
    
    api_url = 'https://api.covalenthq.com'
    endpoint = f'/v1/{chain_id}/address/{address}/{formatage}/?key={api_key}'
    url = api_url + endpoint
    
    r = rq.get(url).json()['data']['items']
    
    df = pd.DataFrame(r)
 
    return df


def fetch_wallet_balance(address):
    api_url = 'https://api.covalenthq.com'
    endpoint = f'/v1/1/address/{address}/balances_v2/'
    url = api_url + endpoint
    r = rq.get(url, auth=("ckey_4e20bd1de6b3424c81eefbd7157",''))
    print(r.json()['data']['items'])
    return(r.json())


if __name__ == '__main__':
    address = "0xFEC4f9D5B322Aa834056E85946A32c35A3f5aDD8"
    #print(wallet_balance(address))
    print(fetch_wallet_balance(address))
    