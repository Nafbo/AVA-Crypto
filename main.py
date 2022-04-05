from src.app_test.feature.link_address import link_address
from src.app_test.feature.wallet import wallet
from src.app_test.feature.wallet_total import wallet_total

address_ETH = "0x102e0206113e2b662ea784eb5db4e8de1d18c8ae"
address_BSC = "0x68a01e1b22790c3b074a7cfe4b522de16c4367ef"
chain_id = {"ETH" : 1, 
             "MATIC": 137,
             "AVAX" : 43114,
             "BSC" : 56,
             "FTM" : 250,}

#address, chain_id = address_BSC, chain_id['BSC']
address = address_BSC
chain_id = chain_id['BSC']
#df = link_address(address, chain_id)
#df = wallet(address, chain_id)
df = wallet_total(address)
print(df)
