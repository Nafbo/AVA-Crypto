import requests as rq
import pandas as pd

def link_address_balance(address, chain_id):
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

if __name__ == '__main__':
    print(link_address_balance("0x9f5c44f84901018275b7f02f0feF1b6183A1B5A1", 56))
