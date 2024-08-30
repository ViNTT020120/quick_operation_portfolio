from abc import ABC, abstractmethod
import os
from datetime import date
import requests
import json
import pandas as pd

class AbstractInventoryManager(ABC):

    def __init__(self, username, password, account_number, base_url, saving_path):
        self.username = username
        self.password = password
        self.account_number = account_number
        self.base_url = base_url
        self.saving_path = saving_path
        self.token_file = "techx_token.json"
        self.headers = None
        self.folder_date = date.today().strftime("%Y%m%d")

    def create_folder_for_today(self):
        """Creates a folder for today's date if it doesn't exist."""
        folder_path = os.path.join(self.saving_path, self.folder_date)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
            print(f'The new folder {self.folder_date} is created!')
        return folder_path

    # @abstractmethod
    # async def _perform_login(self):
    #     """
    #     Performs the login operation and retrieves an access token.
    #     return: accessToke file
    #     """
    #     raise NotImplementedError("Should implement _perform_login")

    @abstractmethod
    def _log_in_kis_api(self):
        """
        Check if there is accessToken file and whether Token is still valid. If not, call _perform_login again to get
        new token.
        """
        raise NotImplementedError("Should implement _log_in_kis_api")

    @abstractmethod
    def _get_inventory_data(self):
        """Retrieves the portfolio data from the API."""
        raise NotImplementedError("Should implement _get_inventory_data")

    @abstractmethod
    def _process_data(self, raw_data):
        """Processes the raw data into a pandas DataFrame."""
        raise NotImplementedError("Should implement _process_data")

    def _save_data_to_excel(self, data, path):
        """Saves the processed data to an Excel file."""
        folder_path = self.create_folder_for_today()
        file_name = os.path.join(folder_path, f"morning_portfolio_{self.folder_date}.xlsx")
        data.to_excel(file_name, index=False)
        print(f"Report saved as {file_name}")

    async def generate_portfolio_positions(self):
        """Orchestrates the process of generating the daily portfolio current positions."""
        await self._log_in_kis_api()
        raw_data = await self._get_inventory_data()
        processed_data = self._process_data(raw_data)
        self._save_data_to_excel(processed_data)

class InventoryManager(AbstractInventoryManager):
    """
    The InventoryManager class is a concrete implementation of the AbstractInventoryManager class. This class is responsible
    for managing and retrieving information related to the portfolio inventory from the KIS API.
    """

    async def _log_in_kis_api(self):
        """
        Performs the login operation and retrieves an access token.
        return: accessToken
        """
        # Perform the login operation and retrieve an access token
        param = {'grant_type': 'password',
         'client_id':'kis-rest',
         'client_secret':'QzHZUA9TxvU2ANbHydihPf5GQdDI0tst05yM6Y19SsVMtfplx5',
         'username': self.username,
         'password': self.password}
    
        url = self.base_url + '/login'
        resp = requests.post(url, data = param)
        outcome = json.loads(resp.text)

        data = {'accessToken':  outcome['accessToken']}
        with open(self.token_file, "w+") as f:
            json.dump(data, f)

    async def _get_inventory_data(self):
        """Retrieves the portfolio data from the API."""
        data = json.load(open(self.token_file))
        accessToken = data['accessToken']

        headers = {'Authorization': 'jwt '+ accessToken}
        resp = requests.get(self.base_url + '/services/eqt/enquiryportfolio', 
                            data = {'accountNumber': self.account_number},
                            headers=headers)
        return json.loads(resp.text)
    
    def _process_data(self, raw_data):
        """Processes the raw data into a pandas DataFrame."""
        # Process the raw data into a pandas DataFrame
        port_df = pd.DataFrame(raw_data[0]['portfolioList'])
        port_df.rename(columns= {'symbol':'Stock (INSTRUMENTID)',
                         'sellable':'Usable (USABLE)', 
                         'boughtT2':'Due (DUE)', 
                         'boughtT1':'Pend. T+1 Buy (TT1UNSETTLEBUY)'},inplace= True)
        return port_df

    def _save_data_to_excel(self, data):
        """Saves the processed data to an Excel file."""
        file_name = "morning_portfolio_" + self.folder_date + ".xlsx"
        data.to_excel(self.saving_path + "/" + file_name, index=False)

    def load_inventory_from_excel(self):
        """Loads the inventory data from an Excel file."""
        file_name = "morning_portfolio_" + self.folder_date + ".xlsx"
        return pd.read_excel(self.saving_path + "/" + file_name)
    
# async def main():
#     username = 'ECB5693'
#     password = 'a123456'
#     account_number = 'ECB5693X5'
#     base_url = 'https://trading.kisvn.vn/rest/api/v1'
#     saving_path = "C:/Users/vi.nt/Downloads/Quick Portfolio Operation/DAILY QUICK OPERATION"

#     inventory_manager = InventoryManager(username, password, account_number, base_url, saving_path)
#     await inventory_manager.generate_portfolio_positions()

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())