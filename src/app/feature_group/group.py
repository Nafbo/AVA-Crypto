import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")
# from src.app.feature_wallet.all_address_wallet import all_address_wallet

def group(wallet, chain_id, action, name_folder):
    
    if action == 'add':
        if os.path.exists('./src/app/feature_group/Folder.json') == True:
            df = pd.DataFrame(pd.read_json('./src/app/feature_group/Folder.json'))
            wallets = np.array([wallet, chain_id])
            total = 3000
            old = (df[df['name']==name_folder]['wallets']).values
            x = np.append(old[0], wallets)
            df.drop(df[df['name']==name_folder]['wallets'].index, 0, inplace=True)
            temp = []
            new = []
            for i in range(0,len(x),2):
                temp.append(x[i])
                temp.append(int(x[i+1]))
                new.append(temp)
                temp = []
            # cf,total = all_address_wallet(wallets)
            folder = {"name" : name_folder,
                        "wallets" : new,
                        "total_folder" : total}
            list_folder = []
            list_folder.append(folder)
            df = df.append(list_folder, ignore_index=True)
            pd.DataFrame(df).to_json('./src/app/feature_group/Folder.json')
            return(pd.read_json('./src/app/feature_group/Folder.json'))
        else:
            return('erreur dossier inexistant')
        
        
    elif action == 'create':
        if os.path.exists('./src/app/feature_group/Folder.json') == True:
            df = pd.DataFrame(pd.read_json('./src/app/feature_group/Folder.json'))
            if df[df['name']== name_folder].empty:
                wallets = np.array([wallet, chain_id], dtype=object)
                # cf,total = all_address_wallet(wallets)
                total = 110
                folder = { "name" : name_folder,
                            "wallets" : wallets,
                            "total_folder" : total}
                list_folder = []
                list_folder.append(folder)
                df = df.append(list_folder, ignore_index=True)
                pd.DataFrame(df).to_json('./src/app/feature_group/Folder.json')
                return(pd.read_json('./src/app/feature_group/Folder.json'))
            else:
                return('erreur dossier existant')
        else:
            wallets = np.array([wallet, chain_id], dtype=object)
            # cf,total = all_address_wallet(wallets)
            total = 110
            folder = { "name" : name_folder,
                        "wallets" : wallets,
                        "total_folder" : total}
            list_folder = []
            list_folder.append(folder)
            pd.DataFrame(list_folder).to_json('./src/app/feature_group/Folder.json')
            return(pd.read_json('./src/app/feature_group/Folder.json'))


    elif action == 'delete_folder':
        df = pd.DataFrame(pd.read_json('./src/app/feature_group/Folder.json'))
        df.drop(df[df['name']==name_folder].index, 0, inplace=True)
        pd.DataFrame(df).to_json('./src/app/feature_group/Folder.json')
        return(pd.read_json('./src/app/feature_group/Folder.json'))
    
    
    elif action == 'delete_wallet':
        df = pd.DataFrame(pd.read_json('./src/app/feature_group/Folder.json'))
        old = (df[df['name']==name_folder]['wallets']).values
        temp = []
        for i in range(len(old[0])):
            if old[0][i][0] != wallet:
                temp.append(old[0][i])
        # cf,total = all_address_wallet(temp)  
        total = 324567      
        folder = {"name" : name_folder,
                    "wallets" : temp,
                    "total_folder" : total}
        list_folder = []
        list_folder.append(folder)
        df.drop(df[df['name']==name_folder]['wallets'].index, 0, inplace=True)
        df = df.append(list_folder, ignore_index=True)
        pd.DataFrame(df).to_json('./src/app/feature_group/Folder.json')
        return(pd.read_json('./src/app/feature_group/Folder.json'))



if __name__ == '__main__':
    # print(group("12345678909876543212345678", 45345678, 'create', 'test89'))
    # print(group("rsetdrvgubhik", 45345678, 'add', 'test56'))
    # print(group("12345678909876543212345678", 45345678, 'delete_wallet', 'test56'))
    print(group("12345678909876543212345678", 45345678, 'delete_folder', 'test56'))