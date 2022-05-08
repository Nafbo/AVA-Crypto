from link_address_balance import link_address_balance
import pandas as pd

def wallet(address,chain_id):
    df= link_address_balance(address, chain_id)
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

'''
Fonction qui prend une adresse et le numero de la blockchain en argument.
Et qui retourn une DataFrame avec le nom de la crypto "Name", le nombre de currency de cette crypto "balance", la balance 
de la crypto en USD "Holdings", la perte/gain en 24h de cette crypto en USD "Profit/loss" et retoure aussi
le total de ce portefeuilleen USD "total"
'''