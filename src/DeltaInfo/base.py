from abc import ABC, abstractmethod
import pandas as pd


class AbstractDeltaManager(ABC):
    def __init__(self, config):
        """
        Initialize the processor with configuration details.
        :param config: Dictionary containing config details like path, operatorID, password, etc.
        """
        self.config = config
        self.token = None
        self.dataframes = {}

    async def authenticate(self):
        """
        Perform authentication and store the token.
        """
        self.token = self._authenticate_user(
            self.config['operatorID'],
            self.config['password'],
            self.config['channelID']
        )

    def load_data(self):
        """
        Load the initial data from an external source (e.g., Excel file).
        """
        self.dataframes = self._load_initial_data(self.config['path'])

    async def process(self):
        """
        Main processing function that coordinates data fetching, transformation, and saving.
        """
        await self.authenticate()
        self.load_data()
        await self.fetch_trade_data()
        self.aggregate_and_save_results()

    async def fetch_trade_data(self):
        """
        Fetch trading data using the API and update the internal data structures.
        """
        for i in range(len(self.dataframes['input']) - 1):
            self.dataframes[f'equity_{i}'] = await self._fetch_equity_data(
                self.token,
                self.dataframes['input'].loc[i, 'subAccount'],
                int(self.dataframes['input'].loc[i, 'tradeSeq']),
                self.dataframes['input'].loc[i, 'clientID'],
                self.config['operatorID'],
                start=int(self.dataframes['input'].loc[i, 'start_20221219'])
            )

        self.dataframes['future'] = await self._fetch_future_data(
            self.token,
            self.dataframes['input'].iloc[-1]['subAccount'],
            int(self.dataframes['input'].iloc[-1]['tradeSeq']),
            self.dataframes['input'].iloc[-1]['clientID'],
            self.config['operatorID']
        )

    def aggregate_and_save_results(self):
        """
        Aggregate trading data and save the results back to an external source.
        """
        df_combined = self._aggregate_trading_data()
        df_summary = self._generate_summary(df_combined)
        self._save_results(df_summary, df_combined)

    @abstractmethod
    async def _authenticate_user(self, operatorID, password, channelID):
        """
        Abstract method for authenticating the user and returning a token.
        eg: Implement the API call to authenticate the user
        """
        raise NotImplementedError("Should implement _authenticate_user")

    @abstractmethod
    def _load_initial_data(self, path):
        """
        Abstract method for loading the initial data from a file or database.
        eg:
        # Load the Excel sheets or other initial data sources
        return {
            'input': pd.read_excel(path, sheet_name='input'),
            'sumBuySell': pd.read_excel(path, sheet_name='sumBuySell'),
            'output_tradeData': pd.read_excel(path, sheet_name='output_tradeData')
        }
        """
        raise NotImplementedError("Should implement _load_initial_data")

    @abstractmethod
    async def _fetch_equity_data(self, token, subAccountID, tradingAccSeq, clientID, operatorID, start, limit=1000):
        """
        Abstract method for fetching equity trading data.
        """
        raise NotImplementedError("Should implement _load_initial_data")

    @abstractmethod
    async def _fetch_future_data(self, token, subAccountID, tradingAccSeq, clientID, operatorID):
        """
        Abstract method for fetching future trading data.
        """
        raise NotImplementedError("Should implement _fetch_future_data")

    @abstractmethod
    def _aggregate_trading_data(self):
        """
        Abstract method for aggregating the fetched trading data.
        """
        raise NotImplementedError("Should implement _aggregate_trading_data")

    @abstractmethod
    def _generate_summary(self, df_combined):
        """
        Abstract method for generating a summary of the aggregated data.
        """
        raise NotImplementedError("Should implement _generate_summary")

    @abstractmethod
    def _save_results(self, summary_df, combined_df):
        """
        Abstract method for saving the results to a file or database.
        """
        raise NotImplementedError("Should implement _save_results")

class DeltaManager(AbstractDeltaManager):
    async def _authenticate_user(self, operatorID, password, channelID):
        """
        Perform authentication and return a token.
        """
        # Perform authentication and return a token
        return "dummy_token"

    def _load_initial_data(self, path):
        """
        Load the initial data from an Excel file.
        """
        dic_data = pd.read_excel(path, sheet_name=None)
        return dic_data

    async def _fetch_equity_data(self, token, subAccountID, tradingAccSeq, clientID, operatorID, start, limit=1000):
        """
        Fetch equity trading data using the token and other parameters.
        """
        # Fetch equity trading data
        return pd.DataFrame()

    async def _fetch_future_data(self, token, subAccountID, tradingAccSeq, clientID, operatorID):
        """
        Fetch future trading data using the token and other parameters.
        """
        # Fetch future trading data
        return pd.DataFrame()

    def _aggregate_trading_data(self):
        """
        Aggregate the fetched trading data.
        """
        # Aggregate trading data
        return pd.DataFrame()

    def _generate_summary(self, df_combined):
        """
        Generate a summary of the aggregated data.
        """
        # Generate summary
        return pd.DataFrame()

    def _save_results(self, summary_df, combined_df):
        """
        Save the results to an Excel file.
        """
        # Save results to an Excel file
        pass

    def load_data(self):
        """
        Load the initial data from an external source (e.g., Excel file).
        """
        pass