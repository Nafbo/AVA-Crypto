import numpy as np
from all_address_wallet import all_address_wallet
from wallet import wallet

address_ETH = "0x102e0206113e2b662ea784eb5db4e8de1d18c8ae"
address_BSC = "0x68a01e1b22790c3b074a7cfe4b522de16c4367ef"
chain_id = {"ETH" : 1, 
             "MATIC": 137,
             "AVAX" : 43114,
             "BSC" : 56,
             "FTM" : 250,}
adresses = np.array([["0x102e0206113e2b662ea784eb5db4e8de1d18c8ae",chain_id["ETH"]], ["0x68a01e1b22790c3b074a7cfe4b522de16c4367ef", chain_id["BSC"]]])

address, chain_id = address_ETH, chain_id['ETH']

# df, total = wallet(address, chain_id)
# df, total = all_address_wallet(adresses)

# print(df)
# print("Total : ", total)
