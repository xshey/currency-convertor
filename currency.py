import constants
from requests import get


class Currency:
    def __init__(self, base_currency=constants.CONSTANTS_BASE_CURRENCY):
        self.base_currency = base_currency
        self.__exchange_values = dict()

    def get_exchange_values(self):
        r = get(
            f'{constants.CONSTANTS_LATEST_URL}?app_id={constants.CONSTANTS_API_KEY}&symbol={self.base_currency}')
        if r.status_code == 200:
            self.__exchange_values = r.json()

    def change_from_usd(self, quote_currency, usd_quantity):
        quote_currency_val = self.currency_value(quote_currency)
        return usd_quantity * quote_currency_val

    def change_between_currencies(self, base_currency, quote_currency, base_currency_quantity):
        quote_currency_val = self.currency_value(quote_currency)
        base_currency_val = self.currency_value(base_currency)
        exchange_rate = base_currency_val / quote_currency_val
        return base_currency_quantity * exchange_rate

    def change_to_all_currencies(self, base_currency, base_currency_quantity):
        base_currency_val = self.currency_value(base_currency)
        exchanged_values = dict()
        for key, val in self.__exchange_values['rate']:
            exchange_rate = base_currency_val / val
            exchanged_values[key] = exchange_rate * base_currency_quantity
        return exchanged_values

    def get_rates(self):
        return self.__exchange_values

    def currency_value(self, currency):
        if currency in self.__exchange_values.keys():
            return self.__exchange_values['rate'][currency]

    def __repr__(self):
        return f"<The base currence is {self.base_currency}"
