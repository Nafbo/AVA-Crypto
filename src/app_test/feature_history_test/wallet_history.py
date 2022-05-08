from link_address_history import link_address_history
import dateutil.parser
import pandas as pd
import matplotlib.pyplot as plt

def wallet_history(address,chain_id):
    df= link_address_history(address,chain_id)
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
    cf = wallet_history("0xb71f6064b01c7e2e14f3bb93db665400ac7acb37", 1)
    print(cf)  
    cf.plot(x ='Date', y='Holdings (en USD)', kind = 'line')
    plt.show()  