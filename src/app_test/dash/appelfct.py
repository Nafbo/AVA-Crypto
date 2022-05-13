#from src.app_test.feature.link_address import link_address
from email.policy import default


import pandas as pd
wallet=pd.read_csv("src/app_test/dash_Alice/ressources/wallet_ex.csv")    
wallet["Name"].fillna("Unknown", inplace=True)
print (wallet)
default_name=wallet['Name'].head(3)
print(default_name[1])