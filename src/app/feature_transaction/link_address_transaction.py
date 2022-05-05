import requests as rq
import pandas as pd

def link_address_transaction(address, chain_id):
    api_key = 'ckey_4e20bd1de6b3424c81eefbd7157'

    endpoint1 = "transfers_v2"  #transaction d'un portefeuille
    
    url = "https://api.covalenthq.com/v1/{}/address/{}/{}/?key={}".format(chain_id, address, endpoint1, api_key)
    print(url)
    
    r = rq.get(url).json()#['data']
    # r1 = r['items']
    # r2 = r['pagination']#['page_number'] 
    #https://api.covalenthq.com/v1/56/address/0x29a97c6effb8a411dabc6adeefaa84f5067c8bbe/transactions_v2/?page-number=0&key=ckey_4e20bd1de6b3424c81eefbd7157
    # print(r2)
    # df = pd.DataFrame(r1)
    return(r)


if __name__ == '__main__':
    print(link_address_transaction("0x7ae2f5b9e386cd1b50a4550696d957cb4900f03a", 56))
    
    

'''
Fonction qui prend en argument une adresse et le numero de la blockchain.
Et qui retourne une DataFrame comprenant les élément neccesaire pour annalyser les transactions du wallet
'''