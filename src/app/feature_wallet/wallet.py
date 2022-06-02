from src.app.feature_wallet.link_address_balance import link_address_balance
import pandas as pd
import numpy as np

def wallet(address,chain_id):
    '''Formatting the information retrieved for a wallet
    
    Parameters:
    address (string): wallet address
    chain_id (int): chain id of the wallet
    
    Returns:
    cf (Dataframe): dataframe usable with the Name, the Balance, the Holdings (en USD) and the Profit/Loss in 24h for each cryptocurrency of the wallet
    total(float): total of the wallet in USD
    '''
    df= link_address_balance(address, chain_id)
    crypto = {}
    crypto_response = []
    total = 0
 
    for i in range(len(df)):
        x = df.loc[i]
        if x["contract_ticker_symbol"] is not None:
            crypto["Name"] = x["contract_ticker_symbol"]
            y = int(x["balance"])*(10**(-int(x["contract_decimals"])))
            crypto["Balance"] = format(y,'.5f')
            crypto["Holdings (en USD)"] = format(x['quote'], ".5f")
            if x['quote_rate_24h'] is None or x['quote_rate'] is None:
                crypto["Profit/Loss"] = None
            else:
                crypto["Profit/Loss"] = format((y*x['quote_rate']) - (y*x['quote_rate_24h']), '.5f')
            total += x['quote']
            crypto_response.append(crypto)
            crypto = {}
    cf = pd.DataFrame(crypto_response)
    cf = cf.sort_values(by=['Name'] ,ascending=True)

    return(cf, total)


if __name__ == '__main__':
    print(wallet("0x4fB36d955dB74ca2ba608b4F93d51eAcfe888349", 1))