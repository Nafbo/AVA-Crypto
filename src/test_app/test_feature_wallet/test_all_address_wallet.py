from src.test_app.test_feature_wallet.test_link_address_balance import test_link_address_balance
import pandas as pd
import numpy as np
import pytest

@pytest.fixture
def test_all_address_wallet(addresses):
    '''Formatting the information retrieved for wallets
    
    Parameters:
    addresses (array): wallets addresses and chain_id for each wallet
    
    Returns:
    cf (Dataframe): dataframe usable with the Name, the Balance, the Holdings (en USD) and the Profit/Loss in 24h for each cryptocurrency of all wallets
    total(float): total of all wallets in USD
    '''
    for i in range(len(addresses)):
        df= test_link_address_balance(addresses[i,0], addresses[i,1])
        crypto = {}
        crypto_response = []
        total = 0
        for i in range(len(df)):
            x = df.loc[i]
            crypto["Name"] = x["contract_ticker_symbol"]
            y = int(x["balance"])*(10**(-int(x["contract_decimals"])))
            crypto["Balance"] = format(y,'.5f')
            crypto["Holdings"] = format(x['quote'], ".5f")
            crypto["Profit/Loss"] = format((y*x['quote_rate']) - (y*x['quote_rate_24h']), '.5f')
            total += x['quote']
        
            crypto_response.append(crypto)
            crypto = {}
        cf = pd.DataFrame(crypto_response)
        cf = cf.sort_values(by=['Name'] ,ascending=True)
    return(cf, total)

@pytest.fixture
def test_all_address_wallet_fixture(addresses):
    cf, total = test_all_address_wallet(addresses)
    return(cf, total)

if __name__ == '__main__':
    print(test_all_address_wallet(np.array([["0x102e0206113e2b662ea784eb5db4e8de1d18c8ae",1], ["0x68a01e1b22790c3b074a7cfe4b522de16c4367ef", 56]])))
