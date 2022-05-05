from link_address_transaction import link_address_transaction 
import pandas as pd
from time import *
import dateutil.parser

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
            transaction['Type'] = "Send"
            y = int(x["value"])*(10**(-18))
            transaction['Balance'] = format(-y,'.5f')
            transaction['Holdings (en USD)'] = format(-x['value_quote'], '.5f')
        else:
            transaction['Type'] = "Receive"
            y = int(x["value"])*(10**(-18))
            transaction['Balance'] = format(y,'.5f')
            transaction['Holdings (en USD)'] = format(x['value_quote'], '.5f')
        
        transaction['Chain_id'] = chain_id_list[chain_id]
        transaction['From'] = x['from_address']
        transaction['To'] = x['to_address']
        
        date = x['block_signed_at']
        date = dateutil.parser.isoparse(date)
        transaction['Date'] = date.strftime("%Y-%m-%d %Hh:%Mm")
        
        if x['successful'] == True:
            transaction['Successful'] = 'Confirmed'
        else:
            transaction['Successful'] = 'Failed'
        
        transaction_response.append(transaction)
        transaction = {}
        
    cf = pd.DataFrame(transaction_response)
    cf = cf.sort_values(by=['Date'] ,ascending=True)       
    return (cf)


if __name__ == '__main__':
    print(transaction("0x732a725df61e32fc9450ca9df7092c6ce6339b24", 1))

'''
Cette fonction prend pour argument l'adresse du portefeuille et la blockchain.
Pour afficher toutes les transactions de ce portefeuille: savoir si c'est reçu ou envoyé "type", la valeur échangé "value".
Le portefeuille d'envoyeur "from", le portefeuille du receveur "to", la date du transfert "date".
Ainsi que si c'est la transaction a été réussite ou pas "successful"
'''