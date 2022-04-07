from src.app.feature.wallet_total import wallet_total

def all_address_wallet(wallets):
    for i in range(len(wallets)):
        cf = wallet_total(wallets[i])
        print(cf)   #joi ou merge avec les dataframe
    return