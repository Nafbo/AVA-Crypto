import requests as rq
import pandas as pd

def link_address_history(quote_curency, chain_id):
    api_key = 'ckey_4e20bd1de6b3424c81eefbd7157'
    endpoint1 = "historical_by_addresses_v2"  #transaction d'un portefeuille
    
    url = "https://api.covalenthq.com/v1/{}/{}/{}/?key={}".format(chain_id, quote_curency, endpoint1, api_key)
    
    r = rq.get(url).json()['data']
    df = pd.DataFrame(r)
    return(df)


if __name__ == '__main__':
    print(link_address_history("SAND", 1))
    
    
'''
Fonction qui prend en argument une adresse et le numero de la blockchain.
Et qui retourne une DataFrame comprenant les élément neccesaire pour annalyser l'historique du wallet
'''