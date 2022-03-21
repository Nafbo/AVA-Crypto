#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 23:02:23 2022

@author: adri22
"""
import requests

API_KEY = 'ckey_4e20bd1de6b3424c81eefbd7157'
base_url = 'https://api.covalenthq.com/v1'
fantom_chain_id = '250'
demo_address = '0xFEC4f9D5B322Aa834056E85946A32c35A3f5aDD8'

def get_wallet_balance(chain_id, address):
    endpoint = f'/{chain_id}/address/{address}/balances_v2/?key={API_KEY}'
    url = base_url + endpoint
    result = requests.get(url).json()
    data = result["data"]
    print(data)
    return(data)


# Example address request
get_wallet_balance(fantom_chain_id, demo_address)


print()
import requests
import json
import pandas as pd

result = requests.get("https://api.covalenthq.com/v1/1/address/0xB1AdceddB2941033a090dD166a462fe1c2029484/stacks/compound/acts/?key=ckey_4e20bd1de6b3424c81eefbd7157")

result.json()

path="/Users/adri22/covalent_api_example.csv"
df = pd.read_csv(path , sep="," )

print(df)