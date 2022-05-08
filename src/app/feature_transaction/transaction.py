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
        if x['transfers' ][0]['transfer_type'] == 'OUT':
            transaction['Type'] = "Send"
            y = int(x['transfers'][0]["delta"])*(10**(-x['transfers'][0]['contract_decimals']))
            transaction['Balance'] = format(-y,'.5f')
            if x['transfers'][0]['delta_quote'] == None:
                transaction['Holdings (en USD)'] = 'None'
            else:
                transaction['Holdings (en USD)'] = format(-x['transfers'][0]['delta_quote'], '.5f')
        else:
            transaction['Type'] = "Receive"
            y = int(x['transfers'][0]["delta"])*(10**(x['transfers'][0]['contract_decimals']))
            transaction['Balance'] = format(y,'.5f')
            if x['transfers'][0]['delta_quote'] == None:
                transaction['Holdings (en USD)'] = 'None'
            else:
                transaction['Holdings (en USD)'] = format(x['transfers'][0]['delta_quote'], '.5f')        
        
        transaction['Name'] = x['transfers'][0]['contract_ticker_symbol']
        
        transaction['From'] = x['transfers'][0]['from_address']
        transaction['To'] = x['transfers'][0]['to_address']
        
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
    cf = cf.sort_values(by=['Date'] ,ascending=False)       
    return (cf)


if __name__ == '__main__':
    print(transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1))


'''
Cette fonction prend pour argument l'adresse du portefeuille et la blockchain.
Pour afficher toutes les transactions de ce portefeuille: savoir si c'est reçu ou envoyé "type", la valeur échangé "value".
Le portefeuille d'envoyeur "from", le portefeuille du receveur "to", la date du transfert "date".
Ainsi que si c'est la transaction a été réussite ou pas "successful"
'''