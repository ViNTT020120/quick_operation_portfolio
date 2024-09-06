from datetime import datetime
import pandas as pd

class TransactionManager:
    def __init__(self, path, inventory, basket):
        """
        Initialize the transaction manager with the necessary managers.
        :param inventory_manager: An instance of the InventoryManager class.
        :param etf_basket_manager: An instance of the ETFBasketManager class.
        """ 
        self.path = path
        self.inventory = inventory
        self.basket = basket

    def load_transaction_history(self) -> pd.DataFrame:
        """
        Retrieve the transaction history from the transaction log.
        """
        df = pd.read_excel(self.path)
        return df

    def update_inventory(self, order_type, etf_name, quantity):
        pass

    def check_inventory(self, order_type, etf_name, quantity):
        pass

    def max_etf_to_create(self, etf_name) -> int:   
        pass