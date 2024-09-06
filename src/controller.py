from abc import ABC, abstractmethod
from inventory.utils import InventoryManager
from basket.utils import ETFBasketManager
from calculate.utils import Calculate
import nest_asyncio
nest_asyncio.apply()

class AbstractController(ABC):
    def __init__(self, calculate, inventory_manager, etf_basket_manager):
        """
        Initialize the controller with the necessary managers.
        :param delta_manager: An instance of the DeltaManager class.
        :param inventory_manager: An instance of the InventoryManager class.
        :param etf_basket_manager: An instance of the ETFBasketManager class.
        """
        self.calculate = calculate
        self.inventory_manager = inventory_manager
        self.etf_basket_manager = etf_basket_manager

    @abstractmethod
    async def run(self):
        """
        Main method to run the orchestration of the different managers.
        This method should handle the sequence of operations, error handling, and coordination between the objects.
        """
        raise NotImplementedError("The run method must be implemented by subclasses")

    def initialize_managers(self):
        """
        Initialize or configure the managers if needed.
        For example, you might want to authenticate all managers or load initial data.
        """
        print("Managers have been initialized.")

    @abstractmethod
    async def _handle_error(self, error):
        """
        Handle any errors that occur during the orchestration process.
        Subclasses should implement specific error handling strategies.
        """
        raise NotImplementedError("The _handle_error method must be implemented by subclasses")

class Controller(AbstractController):
    """
    The Orchestrator class is a concrete implementation of the AbstractOrchestrator class.
    This class is responsible for orchestrating the process of generating the daily portfolio current positions
    and retrieving information related to ETF (Exchange-Traded Fund) baskets.
    """
    async def run(self):
        """
        Main method to run the orchestration of the different managers.
        This method should handle the sequence of operations, error handling, and coordination between the objects.
        """
        try:
            self.initialize_managers()
            await self.inventory_manager.generate_portfolio_positions()
            await self.etf_basket_manager.get_daily_etf_baskets_info()
        except Exception as e:
            await self._handle_error(e)


    async def _handle_error(self, error):
        """
        Handle any errors that occur during the orchestration process.
        Subclasses should implement specific error handling strategies.
        """
        print(f"An error occurred during orchestration: {error}")
        # Log the error, send an alert, or perform any other error handling tasks.

# async def main():
username = 'ECB5693'
password = 'a123456'
account_number = 'ECB5693X5'
base_url = 'https://trading.kisvn.vn/rest/api/v1'
saving_path = "C:/Users/vi.nt/Downloads/quick_operation_portfolio/DAILY QUICK OPERATION"

etf_basket_folder = "C:/Users/vi.nt/Downloads/quick_operation_portfolio/Daily Trading"

calculate = Calculate("")
inventory_manager = InventoryManager(username, password, account_number, base_url, saving_path)
etf_basket_manager = ETFBasketManager(etf_basket_folder)
controller = Controller(calculate, inventory_manager, etf_basket_manager)

df = inventory_manager._load_inventory_from_excel()
print(df)
    # await Controller.run()

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())