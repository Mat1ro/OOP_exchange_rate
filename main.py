import json
import os
from datetime import datetime

import requests


class CurrencyRate:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(current_dir, "exchange_rates.json")

    @classmethod
    def _get_time(cls) -> str:
        """
        Returns the current date in 'YYYY-MM-DD' format.

        Returns:
            str: The current date in 'YYYY-MM-DD' format.
        """
        return datetime.now().date().strftime('%Y-%m-%d')

    @classmethod
    def _get_currency_rate(cls, foreign_exchange: str) -> dict:
        """
        Retrieves the exchange rate data for a given foreign exchange currency using the apilayer API.

        Args:
            foreign_exchange (str): The foreign exchange currency code.

        Returns:
            dict: A dictionary containing exchange rate data.
        """
        url = f"https://api.apilayer.com/exchangerates_data/latest"
        params = {
            "symbols": "RUB",
            "base": foreign_exchange
        }
        headers = {
            "apikey": "zNsVDD08MLFICvo1xwvOcegbL8CKAbqE"
        }

        response = requests.request("GET", url, headers=headers, params=params).json()
        return response

    @classmethod
    def _save_to_json(cls, data: dict):
        """
        Appends the provided data dictionary to the JSON file specified by 'path'.

        Args:
            data (dict): The data dictionary to be saved.
        """
        with open(cls.path) as json_file:
            data_list = json.load(json_file)
        data_list.append(data)
        with open(cls.path, "w") as json_file:
            json.dump(data_list, json_file)

    @classmethod
    def get_exchange_rate(cls, foreign_exchange):
        """
        Retrieves the exchange rate data for a given foreign exchange currency and stores it in the JSON file.

        Args:
            foreign_exchange (str): The foreign exchange currency code.
        """
        rate = cls._get_currency_rate(foreign_exchange)
        data = {
            "time": cls._get_time(),
            "base": rate["base"],
            "rate": rate["rates"]
        }
        cls._save_to_json(data)


currency = input()
currency_rate = CurrencyRate()
currency_rate.get_exchange_rate(currency)
print("all is good")
