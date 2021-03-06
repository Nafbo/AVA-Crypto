from src.test_app.test_feature_wallet.test_link_address_balance import test_link_address_balance
import pandas as pd
import numpy as np


def test_all_address_wallet(addresses=(np.array([["0x1B6c73B564E277B67bF47DDAB355fEC4f30EF961",1], ["0x68a01e1b22790c3b074a7cfe4b522de16c4367ef", 56]]))):
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
            if x['quote_rate_24h'] is None or x['quote_rate'] == None:
                crypto["Profit/Loss"] = None
            else:
                crypto["Profit/Loss"] = format((y*x['quote_rate']) - (y*x['quote_rate_24h']), '.5f')
            total += x['quote']
        
            crypto_response.append(crypto)
            crypto = {}
        cf = pd.DataFrame(crypto_response)
        cf = cf.sort_values(by=['Name'] ,ascending=True)
    return(cf, total)
