from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import pandas as pd

def price(crypto):
    r = cg.get_price(ids=crypto, vs_currencies='usd', include_24hr_change='true')
    price = pd.DataFrame(r)
    if price[crypto]['usd_24h_change'] >=0:
        return(price, 'green')
    else :
        return(price, 'red')

if __name__ == '__main__':
    print(price('bitcoin'))

'''
Affiche le prix par rapport au nom de la crypto
'''    
