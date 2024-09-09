from datetime import datetime, timedelta
import pandas as pd
import os

class TransactionManager:
    def __init__(self, path_transaction, path_arbitrage, inventory, basket, etf_trade_path):
        """
        Initialize the transaction manager with the necessary managers.
        :param inventory_manager: An instance of the InventoryManager class.
        :param etf_basket_manager: An instance of the ETFBasketManager class.
        """ 
        self.inventory = inventory
        self.basket = basket
        self.transaction = self.load_df_history(path_transaction)
        self.arbitrage = self.load_df_history(path_arbitrage)
        self.etf_trade = self.load_df_history(etf_trade_path)

    def load_df_history(self, path) -> pd.DataFrame:
        df = pd.read_excel(path)
        return df

    def update_inventory(self, order_type, etf_name, quantity, basket):
        df = self.inventory
        

    def check_inventory(self, order_type, etf_name, quantity):
        pass

    def max_etf_to_create(self, etf_name) -> int:   
        pass

    def update_inventory_morning(self):
        '''
        This function is called automatically in the morning to update the inventory
        T-2: Update the inventory with the create/redeem transactions from T-2:
             Check arbitrage history -> if yes: im/export basket, toBO, FOL
                                        if no: im/export basket + ETF, toBO, FOL
             Update inventory
        T-1: Update the inventory with the create/redeem transactions from T-1:
             Check arbitrage history -> if yes: lock basket + ETF
                                        if no: lock basket
             Update inventory
        T: Update the inventory with the create/redeem transactions from T:
           Check inventory -> if yes (enough to create/redeem): lock basket + ETF
                              if no: import_arbitrage -> save to arbitrage history -> lock basket + ETF
           Export FOL cash
           Update inventory
        '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        pass

    def update_inventory_T2(self):
        '''
        Update the inventory with the create/redeem transactions from T-2
        '''
        print("Updating inventory T-2...")
        trans = self.transaction
        # trans = self.ap_activities
        arbs = self.arbitrage
        # arbs = self.shortsell

        t2 = datetime.today() - timedelta(2)

        if t2.weekday() >= 5:
            t2 = t2 - timedelta(2)

        trans_t2 = trans[(trans['Ngày đặt lệnh'] == pd.to_datetime(t2.date())) & (trans['Loại lệnh'] == 'Lệnh gốc')]
        arb_t2 = arbs[pd.to_datetime(arbs['Trade Date(yyyy-MM-dd)']) == pd.to_datetime(t2.date())]

        if trans_t2.empty:
            print("No transaction on T-2")
            return
        else:
            for tran in trans_t2.iterrows():
                etf = tran['Mã phiên GD ĐK'].split('-')[0]
                order_type = tran['Loại hoán đổi']
                quantity = tran['SL lô ETF đặt mua/bán'] * 100000
                basket = self.basket[str(t2.date())][etf]
                if arb_t2.empty:
                    print("No arbitrage on T-2")
                    self.update_inventory(order_type, etf, quantity, basket)
                else:
                    for arb in arb_t2.iterrows():
                        print(f'''Arbitrage on T-2 ({arb['Trade Date(yyyy-MM-dd)']}): {arb['STOCK ID']} {arb['SETTLED BALANCE']}''')
                        self.update_inventory(order_type, etf, 0, basket)
            self.imExport_BO(etf, basket, str(t2.date()))
            self.get_FOL_info(etf, basket, str(t2.date()))
        return

    def update_inventory_T1(self):
        '''
        Update the inventory with the create/redeem transactions from T-1
        '''
        print("Updating inventory T-1...")
        trans = self.transaction
        arbs = self.arbitrage

        t1 = datetime.today() - timedelta(1)

        while True:
            if t1.weekday() >= 5:
                t1 = t1 - timedelta(1)
            else:
                break

        trans_t1 = trans[(trans['Ngày đặt lệnh'] == pd.to_datetime(t1.date())) & (trans['Loại lệnh'] == 'Lệnh gốc')]
        arb_t1 = arbs[pd.to_datetime(arbs['Trade Date(yyyy-MM-dd)']) == pd.to_datetime(t1.date())]

        if trans_t1.empty:
            print("No transaction on T-1")
            return
        else:
            for tran in trans_t1.iterrows():
                etf = tran['Mã phiên GD ĐK'].split('-')[0]
                order_type = tran['Loại hoán đổi']
                quantity = tran['SL lô ETF đặt mua/bán'] * 100000
                basket = self.basket[str(t1.date())][etf]
                if arb_t1.empty:
                    print("No arbitrage on T-1")
                    self.update_inventory(order_type, etf, quantity, basket)
                else:
                    for arb in arb_t1.iterrows():
                        print(f'''Arbitrage on T-1 ({arb['Trade Date(yyyy-MM-dd)']}): {arb['STOCK ID']} {arb['SETTLED BALANCE']}''')
                        self.update_inventory(order_type, etf, 0, basket)
        return

    def get_remain_stock_from_inventory(self, ticker):
        inv = self.inventory
        usable = inv.loc[inv['Stock (INSTRUMENTID)' == ticker]['Usable (USABLE)']]
        return usable

    def update_inventory_T(self):
        return
    
    def imExport_BO(self, etf, basket, transaction_date):
        return
    
    def get_FOL_info(self, etf, basket, transaction_date):
        return
    
trans = pd.read_excel(r"Y:\ETF\KIS ETF AP_LP_QIII2019\github\etf_report_kis\Daily Update\Hoan doi history\hoan_doi_history_20200407.XLS")
arbs = pd.read_excel(r"Y:\ETF\KIS ETF AP_LP_QIII2019\github\etf_report_kis\Daily Update\Hoan doi history\import_khong_history.xls")

