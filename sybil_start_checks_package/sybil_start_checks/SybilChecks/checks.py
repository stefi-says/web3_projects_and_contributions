import pandas as pd
import numpy as np
from datetime import datetime 
import requests

def first_trx_during_round(wallet_id, api_key, chain_id, round_start, round_finish):
    wallets = []
    answers = []
    
    session = requests.Session() 
    session.auth = (api_key, '') 

    response = session.get(f'https://api.covalenthq.com/v1/{chain_id}/address/{wallet_id}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=true&no-logs=true')
    
    if ((response.status_code == 200) & (len(response.json()['data']['items']) != 0)) == True:
        
        first_trx= response.json()['data']['items'][0]['block_signed_at']
        first_trx = first_trx.split("T")[0]
        first_trx  = datetime.strptime(first_trx , '%Y-%m-%d')

        round_start = datetime.strptime( round_start , '%Y-%m-%d')
        round_finish  = datetime.strptime(round_finish , '%Y-%m-%d')
    
        answers.append(round_start <= first_trx <= round_finish)
        wallets.append(wallet_id)
    
    else: 
        
        wallets.append(wallet_id)
        answers.append('no data on this chain')
        
    return [wallets[0], answers[0]]





    
    
def wallet_initiated_by(wallet_id, api_key, chain_id, list_for_testing):
    
        session = requests.Session() 
        session.auth = (api_key, '') 
        response = session.get(f'https://api.covalenthq.com/v1/{chain_id}/address/{wallet_id}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=true&no-logs=true')
        
        if ((response.status_code == 200) & (len(response.json()['data']['items']) != 0)) == True:
        
            answers= []
            first_trx= response.json()['data']['items']
            initiated_by = []
            
            for i in range(len(first_trx)): 
                if (first_trx[i]['successful'] == True) and (int(first_trx[i]['value']) != 0): 
                    received_from  = first_trx[i]['from_address']
                    initiated_by.append(received_from)
           
            
            answers.append(pd.Series(list_for_testing).isin(initiated_by).unique().sum() >0)
            
        else: 
        
            answers = []
            answers.append('no data on this chain')
        
    
        return [wallet_id, answers[0]]
     
    
    
    


def trx_between_wallets(wallet_id, api_key, chain_id, list_for_testing):
    

        session = requests.Session() 
        session.auth = (api_key, '') 
        response = session.get(f'https://api.covalenthq.com/v1/{chain_id}/address/{wallet_id}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=true&no-logs=true')
      
        
        if ((response.status_code == 200) & (len(response.json()['data']['items']) != 0)) == True:
            
            answers = []
           
            trx_data= response.json()['data']['items']

            received_trx = []
            destination_trx = []
            for i in range(len(trx_data)):
                    if trx_data[i]['from_address'] != wallet_id:
                        received_from  = trx_data[i]['from_address']
                        received_trx.append(received_from)


            for i in range(len(trx_data)):
                    if (trx_data[i]['to_address'] != wallet_id) & (trx_data[i]['to_address'] != None):
                        sended_to  = trx_data[i]['to_address']
                        destination_trx.append(sended_to)

            received_wallets = np.unique(received_trx)
            destination_wallets = np.unique(destination_trx)

            all_wallets = list(received_wallets) + list(destination_wallets)

            answers.append(pd.Series(list_for_testing).isin(all_wallets).sum() > 0 )
       
        else: 
        
            answers = []
            answers.append('no data on this chain')
        
    
        return [wallet_id, answers[0]] 
    
    
    
def wallets_trx_during_round(wallet_id, api_key, chain_id, round_start, round_finish, list_for_testing):


        session = requests.Session() 
        session.auth = (api_key, '') 
        response = session.get(f'https://api.covalenthq.com/v1/{chain_id}/address/{wallet_id}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=true&no-logs=true')

        trx_data= response.json()['data']['items']

        if ((response.status_code == 200) & (len(response.json()['data']['items']) != 0)) == True:
            answers = []
            
            round_start = datetime.strptime(round_start, '%Y-%m-%d')
            round_finish = datetime.strptime(round_finish, '%Y-%m-%d')

            received_trx = []
            destination_trx = []
            for i in range(len(trx_data)):

                    if (round_start <= datetime.strptime(trx_data[i]['block_signed_at']
                                                     .split('T')[0], '%Y-%m-%d') < round_finish) == True:

                        if (trx_data[i]['from_address'] != wallet_id) & (trx_data[i]['from_address'] != None):
                            received_from  = trx_data[i]['from_address']
                            received_trx.append(received_from)          

                        else:
                            
                            if trx_data[i]['from_address'] != None:
                                
                                sended_to  = trx_data[i]['to_address']
                                destination_trx.append(sended_to) 




            received_wallets = np.unique(received_trx)
            destination_wallets = np.unique(destination_trx)

            all_wallets = list(received_wallets) + list(destination_wallets)

            answers.append(pd.Series(list_for_testing).isin(all_wallets).sum() > 0)
            
        else: 
        
            answers = []
            answers.append('no data on this chain')
        
    
        return [wallet_id, answers[0]]
 
    
    

def wallet_historical_trx(wallets_list , api_key, chain_id):

        trx = []
    
        for i in range(len(wallets_list)):

            wallet_id = wallets_list[i]
            session = requests.Session() 
            session.auth = (api_key, '') 
            response = session.get(f'https://api.covalenthq.com/v1/{chain_id}/address/{wallet_id}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=true&no-logs=true')
    
            w_trx= response.json()['data']['items']
            trx.extend(w_trx)
               
        df_trx = []
        df_trx = pd.DataFrame(df_trx, columns = ['block_signed_at', 'block_height', 'tx_hash', 'tx_offset', 'successful',
                       'from_address', 'from_address_label', 'to_address', 'to_address_label',
                   'value', 'value_quote', 'gas_offered', 'gas_spent', 'gas_price',
                   'fees_paid', 'gas_quote', 'gas_quote_rate']) 

        for i in range(len(trx)):
    
            trx_obj = pd.DataFrame(trx[i].items()).set_index(0).transpose()
            df_trx = pd.concat([df_trx,trx_obj], axis = 0)

        return df_trx.reset_index(drop = True)
    
