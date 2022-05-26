from src.test_app.test_feature_transaction.test_link_address_transaction import test_link_address_transaction 
import pandas as pd
from time import *
import dateutil.parser
import pytest

@pytest.fixture
def test_transaction(address,chain_id):
    '''Formatting the information retrieved for a wallet
    
    Parameters:
    address (string): wallet address
    chain_id (int): chain id of the wallet
    
    Returns:
    cf (Dataframe): dataframe usable with the Type of transaction, the Balance, the Holdings (en USD), the From of the transaction, the To of the transaction and the Succesful of the transaction for a wallet
    '''
    df= test_link_address_transaction(address,chain_id)
    transaction = {}
    transaction_response = []
    
    for i in range(len(df)):
        x = df.loc[i]
        if x['transfers' ][0]['transfer_type'] == 'OUT':
            transaction['Type'] = "Send"
            y = int(x['transfers'][0]["delta"])*(10**(-x['transfers'][0]['contract_decimals']))
            transaction['Balance'] = format(-y,'.3f')
            
            compte=-1
            for i in transaction['Balance']:
                if i != '.':
                    compte+=1                    
                else:
                    if 5<= compte <= 8:  #-1 000 = -1K 
                        transaction['Balance'] = transaction['Balance'][:compte-3] +'.' + transaction['Balance'][compte-3:compte] + ' k'
                    elif 8<= compte <= 11 : #-1 000 000 = -1M
                        transaction['Balance'] = transaction['Balance'][:compte-6] +'.' + transaction['Balance'][compte-6:compte-3] + ' M'
                    elif 12 <= compte:
                        transaction['Balance'] = format(float(transaction['Balance']),'.1E')
                
                
            if x['transfers'][0]['delta_quote'] == None:
                transaction['Holdings (en USD)'] = 'None'
            else:
                transaction['Holdings (en USD)'] = format(-x['transfers'][0]['delta_quote'], '.5f')
        else:
            transaction['Type'] = "Receive"
            y = int(x['transfers'][0]["delta"])*(10**(x['transfers'][0]['contract_decimals']))
            transaction['Balance'] = format(y,'.3f')
            
            
            compte=0
            for i in transaction['Balance']:
                if i != '.':
                    compte+=1                    
                else:
                    if 4<= compte <= 7:  #1 000 = 1K 
                        transaction['Balance'] = transaction['Balance'][:compte-3] +'.' + transaction['Balance'][compte-3:compte] + ' k'
                    elif 8<= compte <= 11 : #1 000 000 = 1M
                        transaction['Balance'] = transaction['Balance'][:compte-6] +'.' + transaction['Balance'][compte-6:compte-3] + ' M'
                    elif 12 <= compte:
                        transaction['Balance'] = format(float(transaction['Balance']),'.1E')
            
            if x['transfers'][0]['delta_quote'] == None:
                transaction['Holdings (en USD)'] = 'None'
            else:
                transaction['Holdings (en USD)'] = format(x['transfers'][0]['delta_quote'], '.5f')        
        
        transaction['Name'] = x['transfers'][0]['contract_ticker_symbol']
        
        transaction['From'] = x['transfers'][0]['from_address']
        transaction['From'] = (transaction['From'][:5]+'...'+transaction['From'][-5:])
        transaction['To'] = x['transfers'][0]['to_address']
        transaction['To'] = (transaction['To'][:5]+'...'+transaction['To'][-5:])
        
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
    # cf = cf.sort_values(by=['Date'] ,ascending=False)       
    return (cf)


if __name__ == '__main__':
    print(test_transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1))


'''
Cette fonction prend pour argument l'adresse du portefeuille et la blockchain.
Pour afficher toutes les transactions de ce portefeuille: savoir si c'est reçu ou envoyé "type", la valeur échangé "value".
Le portefeuille d'envoyeur "from", le portefeuille du receveur "to", la date du transfert "date".
Ainsi que si c'est la transaction a été réussite ou pas "successful"
'''


