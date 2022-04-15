import pandas as pd
from datetime import datetime
from link_address_transaction import link_address_transaction 
from datetime import datetime
from time import *

def transaction(address,chain_id):
    df= link_address_transaction(address,chain_id)
    transaction = {}
    transaction_response = []
    
    for i in range(len(df)):
        x = df.loc[i]
        chain_id_list = {1: "ETH", 
             137:"MATIC",
             43114: "AVAX",
             56:"BSC",
             250:"FTM",}
        if x['from_address'] == address:
            transaction['type'] = "Send"
            y = int(x["value"])*(10**(-18))
            transaction['value'] = format(-y,'.4f')
        else:
            transaction['type'] = "Receive"
            y = int(x["value"])*(10**(-18))
            transaction['value'] = format(y,'.4f')
        
        transaction['crypto'] = chain_id_list[chain_id]
        transaction['from'] = x['from_address']
        transaction['to'] = x['to_address']
        
        date = x['block_signed_at']
        import dateutil.parser
        date = dateutil.parser.isoparse(date)
        transaction['date'] = date.strftime("%Y-%m-%d %Hh:%Mm")
        
        if x['successful'] == True:
            transaction['successful'] = 'Confirmed'
        else:
            transaction['successful'] = 'Failed'
        
        transaction_response.append(transaction)
        transaction = {}
        
    cf = pd.DataFrame(transaction_response)
    cf = cf.sort_values(by=['date'] ,ascending=True)       
    return (cf)


'''
Cette fonction prend pour argument l'adresse du portefeuille et la blockchain.
Pour afficher toutes les transactions de ce portefeuille: savoir si c'est reçu ou envoyé "type", la valeur échangé "value".
Le portefeuille d'envoyeur "from", le portefeuille du receveur "to", la date du transfert "date".
Ainsi que si c'est la transaction a été réussite ou pas "successful"
'''