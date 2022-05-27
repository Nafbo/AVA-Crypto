import requests as rq
import pandas as pd

def test_link_address_balance(address="0x102e0206113e2b662ea784eb5db4e8de1d18c8ae", chain_id=1):
    '''Retrieving and formatting information from the api
    
    Parameters:
    address (string): wallet address
    chain_id (int): chain id of the wallet
    
    Returns:
    df (Dataframe): dataframe usable with all the information of the api
    '''
    
    api_key = 'ckey_4e20bd1de6b3424c81eefbd7157'
    url = "https://api.covalenthq.com/v1/{}/address/{}/balances_v2/?key={}".format(chain_id, address, api_key)
    r = rq.get(url).json()['data']['items']
    df = pd.DataFrame(r)  
    return(df)

