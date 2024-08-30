# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 16:22:30 2022

@author: HMMETF01
"""


# copy files fot daily stock report at 8am
import os
import shutil

day_str = '20240828'

src =  r'Y:/ETF/KIS ETF AP_LP_QIII2019/DAILY QUICK OPERATION/src'
destination = 'Y:/ETF/KIS ETF AP_LP_QIII2019/DAILY QUICK OPERATION/' + day_str

####################### init folder ############
if not os.path.isdir(destination):
    os.makedirs(destination)
    print(f'The new folder {destination} is created!')

########################################################
# daily import basket files
raw_basket_path = {}
raw_basket_path['E1VFVN30'] = r'C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_E1VFVN30'
raw_basket_path['FUEVFVND'] = r'C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUEVFVND'
raw_basket_path['FUESSVFL'] = r"C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUESSVFL"
raw_basket_path['FUEVN100'] = r"C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUEVN100"
raw_basket_path['FUESSV30'] = r"C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUESSV30"
raw_basket_path['FUESSV50'] = r"C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUESSV50"
raw_basket_path['FUEMAV30'] = r"C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUEMAV30"
raw_basket_path['FUEKIV30'] = r"C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUEKIV30"
raw_basket_path['FUEKIVFS'] = r"C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUEKIVFS"
raw_basket_path['FUEDCMID'] = r'C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUEDCMID'
raw_basket_path['FUEMAVND'] = r'C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUEMAVND'
raw_basket_path['FUEKIVND'] = r'C:\Users\vi.nt\Downloads\Quick Portfolio Operation\data\Daily_basket_FUEKIVND'


print('COPY BASKET FILE TO ', destination)
print('-------------------------------------------------------------------------------------------')

for etf_key in raw_basket_path:
    file_name ='/'+ etf_key + '_Import_' + day_str + '.xlsx'
    file_path = raw_basket_path[etf_key] + file_name
    
    try:
        print('Copy ', file_path)
        shutil.copy(file_path, destination)
    except:
        print('      NO FILE NAME: ', file_path)
        print('      -------------------')

############################################################
# morning stock report
print('-------------------------------------------------------------------------------------------')
print('MAKE MORNING REPORT TO ', destination)
file_name = '/MorningReport.xlsx'
file_path = src + file_name 

shutil.copy(file_path, destination)
print('-------------------------------------------------------------------------------------------')


















