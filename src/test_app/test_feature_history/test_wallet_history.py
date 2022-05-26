from src.test_app.test_feature_history.test_link_address_history import test_link_address_history
import dateutil.parser
import pandas as pd
import matplotlib.pyplot as plt
import pytest

@pytest.fixture
def test_wallet_history(address,chain_id):
    '''Formatting the information retrieved for a wallet
    
    Parameters:
    address (string): wallet address
    chain_id (int): chain id of the wallet
    
    Returns:
    cf (Dataframe): dataframe usable with the Holdings (en USD) and the date of this balance of the wallet
    '''
    df= test_link_address_history(address,chain_id)
    history = {}
    history_response = []
    for i in range(len(df)):
        x = df.loc[i]
        
        date = x['timestamp']
        date = dateutil.parser.isoparse(date)
        history['Date'] = date.strftime("%Y-%m-%d")
        
        history['Holdings (en USD)'] = x['quote_rate']
    
        history_response.append(history)
        history = {}
        
    cf = pd.DataFrame(history_response)                
    return(cf)
    
if __name__ == '__main__':
    cf = print(test_wallet_history("0xb71f6064b01c7e2e14f3bb93db665400ac7acb37", 1))  
    cf.plot(x ='Date', y='Holdings (en USD)', kind = 'line')
    plt.show()  
