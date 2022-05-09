from pickletools import read_uint1
import requests as rq
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def link_address_transaction(address, chain_id):
    api_key = 'ckey_4e20bd1de6b3424c81eefbd7157'
    url = "https://api.covalenthq.com/v1/{}/address/{}/portfolio_v2/?key={}".format(chain_id, address, api_key)
    r = rq.get(url).json()['data']['items']
    list_contract_address = []
    for i in range(len(r)):
        r = rq.get(url).json()['data']['items'][i]['contract_address']
        if r != '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee' and r != '0xzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz' and r != '0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':
            list_contract_address.append(r)        
        
    df2 = pd.DataFrame()
    for contract_address in list_contract_address:
        url1 = "https://api.covalenthq.com/v1/{}/address/{}/transfers_v2/?contract-address={}&key={}".format(chain_id, address, contract_address, api_key)       
        r2 = rq.get(url1).json()['data']['items']
        if r2 != []:          
            df2 = df2.append(r2, ignore_index=True)
            
    r1 = rq.get(url1).json()['data']['pagination']['has_more']
    nbr1=1
    while r1 == True:       
        url1 = "https://api.covalenthq.com/v1/{}/address/{}/transfers_v2/?page-number={}&contract-address={}&key={}".format(chain_id, address, nbr1, contract_address, api_key)
        r2 = rq.get(url1).json()['data']['items']
        if r2 != []:          
            df2 = df2.append(r2, ignore_index=True)
        r1 = rq.get(url1).json()['data']['pagination']['has_more']
        nbr1 +=1    
                  
    return(df2)


if __name__ == '__main__':
    print(link_address_transaction("0x9f5c44f84901018275b7f02f0feF1b6183A1B5A1", 56))
    
    

'''
Fonction qui prend en argument une adresse et le numero de la blockchain.
Et qui retourne une DataFrame comprenant les élément neccesaire pour annalyser les transactions du wallet
'''