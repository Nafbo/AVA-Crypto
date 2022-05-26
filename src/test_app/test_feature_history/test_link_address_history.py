import requests as rq
import pandas as pd
import pytest

@pytest.fixture
def test_link_address_history(address, chain_id):
    '''Retrieving and formatting information from the api
    
    Parameters:
    address (string): wallet address
    chain_id (int): chain id of the wallet
    
    Returns:
    df (Dataframe): dataframe usable with all the information of the api
    '''
    
    api_key = 'ckey_4e20bd1de6b3424c81eefbd7157'
    url = "https://api.covalenthq.com/v1/{}/address/{}/portfolio_v2/?key={}".format(chain_id, address, api_key)
    r = rq.get(url).json()['data']['items'][0]['holdings']
    df = pd.DataFrame(r)

    return(df)


if __name__ == '__main__':
    print(test_link_address_history("0xb71f6064b01c7e2e14f3bb93db665400ac7acb37", 1))
