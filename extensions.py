from config import TOKEN_CUR, SOURCE
import requests
import json


class APIException(Exception):
    pass


class PriceRequestor:

    CURRENCY_LIST: dict = {
        'евро': 'EUR',
        'доллар': 'USD',
        'рубль': 'RUB'}

    def get_values(self) -> list:
        result = []
        for currency in self.CURRENCY_LIST.keys():
            result.append(currency)
        return result

    def get_price(self, base: str, quote: str, amount: str) -> float:
        try:
            base_currency = base.lower()
            quote_currency = quote.lower()
            if base_currency not in self.get_values():
                raise APIException(f'Валюта {base} не найдена в списке доступных для конвертации!')
            if quote_currency not in self.get_values():
                raise APIException(f'Валюта {quote} не найдена в списке доступных для конвертации!')
            if base_currency == quote_currency:
                raise APIException('Валюты должны быть разными!')
            amount_float = float(amount)
        except ValueError:
            raise APIException('Количество конвертируемой валюты должно быть указано в виде числа!')
        else:
            pair_currency = self.CURRENCY_LIST[base_currency] + self.CURRENCY_LIST[quote_currency]
            res = requests.get(f'{SOURCE}?get=rates&pairs={pair_currency}&key={TOKEN_CUR}')
            currency = json.loads(res.content)
            return float(currency['data'][pair_currency]) * amount_float
