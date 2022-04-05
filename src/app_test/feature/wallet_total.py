from src.app_test.feature.link_address import link_address
from src.app_test.feature.wallet import wallet
import pandas as pd

def wallet_total(address):
    chain_id = {"ETH" : 1, 
             "MATIC": 137,
             "AVAX" : 43114,
             "BSC" : 56,
             "FTM" : 250,}
    crypto_response = []
    crypto = {}
    total = 0
    for i in chain_id:
        df= link_address(address, chain_id[i])
 
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
    print("\n Total: ", total)
    cf = pd.DataFrame(crypto_response)
    cf = cf.sort_values(by=['Name'] ,ascending=True) #Triage par devise et transaction
        
    return cf
        
        
    
    