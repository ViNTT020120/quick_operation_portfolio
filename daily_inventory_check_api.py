# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 08:19:50 2022

@author: nguyen.na
"""

#Daily inventory report
import requests
import json
#import numpy
import pandas as pd
import os
from datetime import date

    
#folder_date = '20230727'
today = date.today()
folder_date = today_str = today.strftime("%Y%m%d")

os.chdir('Y:/ETF/KIS ETF AP_LP_QIII2019/DAILY QUICK OPERATION')

####### Update delta file #############
import real_time_delta_v1_2

#real_time_delta_v1_2.main()
try:
    real_time_delta_v1_2.main()
    
except Exception as e:
    print(e)
    # pass

####### update basket inventory
         
if not os.path.isdir(folder_date):
    os.makedirs(folder_date)
    print(f'The new folder {folder_date} is created!')
    
saving_path = 'Y:/ETF/KIS ETF AP_LP_QIII2019/DAILY QUICK OPERATION/' + folder_date

os.chdir(saving_path)

def log_in_kis_api_2(username, password, base_url = 'https://trading.kisvn.vn/rest/api/v1', path ='/login', param = {'grant_type': 'password',
         'client_id':'kis-rest',
         'client_secret':'QzHZUA9TxvU2ANbHydihPf5GQdDI0tst05yM6Y19SsVMtfplx5'}):
    
    param['username'] = username
    param['password'] = password
    
    url = base_url + path
    resp = requests.post(url, data = param)
    outcome = json.loads(resp.text)
    #token = outcome['accessToken']
    return outcome

################ LOG IN #################################

#Step 0: log in

try:
    data = json.load(open('techx_token.json'))
    accessToken = data['accessToken']
    headers = {'Authorization': 'jwt '+ accessToken}
    resp = requests.get('https://trading.kisvn.vn/rest' + '/api/v1/services/eqt/enquiryportfolio', 
                        data = {'accountNumber':'ECB5693X5'}, 
                        headers = headers)
    print('accessToken not expired')
except:
    print('accessToken is EXPIRED. Try log in now!')
    outcome = log_in_kis_api_2('ECB5693','a123456')
    headers = {'Authorization': 'jwt '+ outcome['accessToken']}
    data = {'accessToken':  outcome['accessToken']}
    with open("techx_token.json", "w+") as f:
        json.dump(data, f)


# outcome = log_in_kis_api_2('ECB5693','a123456')

# headers = {'Authorization': 'jwt '+ outcome['accessToken']}

####################  GET INVENTORY API   #########################################
base_url = 'https://trading.kisvn.vn/rest'
#path = '/api/v1/services/eqt/accountbalance'
path = '/api/v1/services/eqt/enquiryportfolio'

url = base_url+path
param = {'accountNumber':'ECB5693X5'}

resp = requests.get(url, data = param, headers = headers)
outcome2 = json.loads(resp.text)

############### CONVERT API TO READABLE EXCEL FILE

port_lst = outcome2[0]['portfolioList']
port_df = pd.DataFrame(port_lst)
port_df.rename(columns= {'symbol':'Stock (INSTRUMENTID)',
                         'sellable':'Usable (USABLE)', 
                         'boughtT2':'Due (DUE)', 
                         'boughtT1':'Pend. T+1 Buy (TT1UNSETTLEBUY)'},inplace= True)

########### Save excel file
file_name = "morning_portfolio_"+today_str+".xlsx"

port_df.to_excel(file_name, index= False)


