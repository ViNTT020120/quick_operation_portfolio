from abc import ABCMeta, abstractmethod
import pandas as pd

class AbstractETFBasketManager(object):
    """
    The AbstractETFBasket class is an abstract base class (ABC) designed for managing and retrieving information
    related to ETF (Exchange-Traded Fund) baskets. This class establishes a common interface for all subclasses that
    handle ETF basket data, with a focus on retrieving information from an Outlook system.
    """
    _metaclass_ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def _get_info_for_1_basket(self):
        """
        This method is called to retrieve information about a single ETF basket from the Outlook system and save it to
        predefined path(s)
        :return:
        """
        raise NotImplementedError("Should implement get_info_for_1_basket")

    @abstractmethod
    async def get_daily_etf_baskets_info(self):
        """
        This method retrieves information for all ETF basket KIS is doing AP/LP. For each
        ticker, it calls _get_info_for_1_basket to get the corresponding ETF basket information.
        """
        raise NotImplementedError("Should implement get_daily_etf_baskets_info")
    
class ETFBasketManager(AbstractETFBasketManager):
    """
    The ETFBasketManager class is a concrete implementation of the AbstractETFBasket class. This class is responsible"
    for managing and retrieving information related to ETF (Exchange-Traded Fund) baskets from the Outlook system.
    """
    def __init__(self, etf_basket_folder, outlook_client = None):
        """
        Initialize the ETFBasketManager with an instance of the OutlookClient and the path to the ETF basket folder.
        :param outlook_client: An instance of the OutlookClient class used to interact with the Outlook system.
        :param etf_basket_folder: The path to the folder where ETF basket information will be saved.
        """
        self.outlook_client = outlook_client
        self.etf_basket_folder = etf_basket_folder
        self.etf_list = [
            'E1VFVN30', 'FUESSV50', 'FUESSVFL', 'FUEVFVND', 
            'FUEVN100', 'FUESSV30', 'FUEMAV30', 'FUEKIV30', 
            'FUEDCMID', 'FUEKIVFS', 'FUEMAVND', 'FUEKIVND'
            ]
        self.fol_check_list = [
            "AP/Nhà đầu tư nước ngoài\nForeign AP/Investor",
            "Nhà đầu tư nước ngoài/AP nước ngoài Foreign Investor/Foreign AP",
            "KIS (*)",
            "KIS",
            "KIS, MAS",
            ]

    def _get_info_for_1_basket(self, ticker):
        """
        Retrieve information about a single ETF basket with the given ticker from Outlook.
        """
        pass    
    
    def save_etf_basket_info(self, etf_basket_info):
        """
        Save the ETF basket information to the predefined path(s).
        :param etf_basket_info: The information of the ETF basket to be saved.
        """
        # Save the ETF basket information to the predefined path(s)
        pass

    async def get_daily_etf_baskets_info(self):
        """
        Retrieve information for all ETF baskets KIS is doing AP/LP. For each ticker,
        it calls _get_info_for_1_basket to get the corresponding ETF basket information
        and then saves the information to the predefined path(s).
        """
        pass

    def _load_1_basket_from_excel(self, ticker) -> pd.DataFrame:
        """
        Retrieve information about a single ETF basket with the given ticker from an Excel file.
        :param ticker: The ticker symbol of the ETF basket.
        :return: The information of the ETF basket.
        """
        df = pd.read_excel(self.etf_basket_folder + "/Daily_trading_basket_update/" + ticker + '_Import.xlsx')
        df = df[df[df.columns[0]] == ticker]
        return df

    
    def load_all_basket_from_excel(self) -> dict:

        dict_etf_basket_info = {}

        for etf in self.etf_list:
            etf_basket_info = self._load_1_basket_from_excel(etf)
            dict_etf_basket_info[etf] = etf_basket_info

        return dict_etf_basket_info
    
    def get_fol_basket(self, ticker) -> list:
        '''
        Get list of FOL from ETF basket
        '''
        basket = self._load_1_basket_from_excel(ticker)
        fol_df = basket[basket[basket.columns[len(basket.columns)-1]].isin(self.fol_check_list)]
        return fol_df[fol_df.columns[2]].tolist()
    
    def get_nfol_basket(self, ticker) -> list:
        '''
        Get list of nFOL from ETF basket
        '''
        basket = self._load_1_basket_from_excel(ticker)
        nfol_df = basket[~basket[basket.columns[len(basket.columns)-1]].isin(self.fol_check_list)]
        return nfol_df[nfol_df.columns[2]].tolist()
    
    def test(self):
        print('test')
        ticker = 'FUEDCMID'
        fol = self.get_fol_basket(ticker)
        nfol = self.get_nfol_basket(ticker)
        print(f'{ticker}: {nfol}')

etf_basket_folder = r"C:\Users\vi.nt\Downloads\quick_operation_portfolio\Daily Trading" 
basket_manager = ETFBasketManager(etf_basket_folder)
basket_manager.test()