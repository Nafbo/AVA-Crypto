from src.app.feature_wallet.link_address_balance import link_address_balance
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

        crypto["Holdings (en USD)"] = format(x['quote'], ".5f")

        crypto["Profit/Loss"] = format((y*x['quote_rate']) - (y*x['quote_rate_24h']), '.5f')
        total += x['quote']
        
        crypto_response.append(crypto)
        crypto = {}
    cf = pd.DataFrame(crypto_response)
    cf = cf.sort_values(by=['Name'] ,ascending=True)

    return(cf, total)


if __name__ == '__main__':
    print(wallet("0x102e0206113e2b662ea784eb5db4e8de1d18c8ae", 1))
    cf , total = wallet("0x102e0206113e2b662ea784eb5db4e8de1d18c8ae", 1)
    dff= cf[cf['Name'] == 'ETH']
    # balance_text = "{}".format(dff['Balance'])
    # balance_split = balance_text.split('\n',1)[0].split('    ',1)[1]
    balance_text = dff['Balance'][1]
    print("Balance : ",balance_text)


'''
Fonction qui prend une adresse et le numero de la blockchain en argument.
Et qui retourn une DataFrame avec le nom de la crypto "Name", le nombre de currency de cette crypto "balance", la balance 
de la crypto en USD "Holdings", la perte/gain en 24h de cette crypto en USD "Profit/loss" et retoure aussi
le total de ce portefeuilleen USD "total"
'''