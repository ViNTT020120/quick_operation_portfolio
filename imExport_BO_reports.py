# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 09:50:04 2020

@author: dang.tk
"""

import pandas as pd
import os   
###### Report import/export to BO while create/redeem

##### date of hoan doi

etf_order_day = '20240821'
transaction_day_report_format = '2024-08-23'

################## read file import(trade_raw_from_etf)

path_raw = r'Y:\ETF\KIS ETF AP_LP_QIII2019\github\etf_report_kis\Daily Update\trade_raw_from_etf.xlsx'
df_raw = pd.read_excel(path_raw,
                       dtype={'orderDate':str})

##### gather data by day

df_f0 = df_raw[df_raw['orderDate'] == etf_order_day]

# Write to Export basket file new format (export & import in the same file with W/D remark) to DAILY QUICK OPERATION folder
col_name = ['MARKET ID', 'SUB ACCOUNT ID', 'ACC SEQ','STOCK ID','SETTLED BALANCE',
             'Trade Date(yyyy-MM-dd)','Location','REMARK','Tran Type','To Sub Account ID','BonusQty']

export_bas_df_new = pd.DataFrame(columns = col_name)

list_HNX  = ['IDC', 'SHS', 'PVS'] # HARD CODE

export_bas_df_new['STOCK ID'] = df_f0['stockCode']
export_bas_df_new['SETTLED BALANCE'] = df_f0['matchedQuantity']
export_bas_df_new['MARKET ID'] = 'HO'
export_bas_df_new['SUB ACCOUNT ID'] = 'ECB5693X5'
export_bas_df_new['ACC SEQ'] = 5
export_bas_df_new['Trade Date(yyyy-MM-dd)'] = transaction_day_report_format
export_bas_df_new['Location'] = 'TDCN'
export_bas_df_new['REMARK'] = df_f0['orderNumber']
export_bas_df_new['Tran Type'] = df_f0['sellBuyType']
export_bas_df_new['Tran Type'].replace(["BUY","SELL"],["D","W"], inplace = True)
export_bas_df_new['BonusQty'] = 0

for idx, row in export_bas_df_new.iterrows():
    if export_bas_df_new.loc[idx,'STOCK ID'] in list_HNX:
        export_bas_df_new.loc[idx,'MARKET ID'] = 'HA'

# FOR BO REPORT ################################################
##### group by ticker,q-ty, BUY/SELL
df_f1 = df_f0[df_f0['sellBuyType'] == 'SELL']

df_f0.loc[df_f1.index,'matchedQuantity'] = df_f0.loc[df_f1.index,'matchedQuantity'] * (-1)
######  BUY q-ty - SELL q-ty

###### print new DF with a result
df_f2 = df_f0.groupby('stockCode', as_index = False)[['stockCode','matchedQuantity']].sum()

#### export file to BO inventory ##########################
saving_path = "Y:\ETF\KIS ETF AP_LP_QIII2019\Dang\To BO"

os.chdir(saving_path) 

#### save a copy to DAILY QUICK OPERATION
saving_path = "Y:\ETF\KIS ETF AP_LP_QIII2019\DAILY QUICK OPERATION"
os.chdir(saving_path) 

df_f2.to_excel('to BO'+'_' + transaction_day_report_format + '.xlsx')
export_bas_df_new.to_excel('etfImExport' + transaction_day_report_format + '.xlsx', index=False )