from config import TOKEN_CUR, SOURCE
import requests
import json

CURRENCY_LIST: dict = {
        'евро': 'EUR',
        'доллар': 'USD',
        'рубль': 'RUB'}


class APIException(Exception):
    pass


class PriceRequestor:
    @staticmethod
    def get_values() -> list:
        result = []
        for currency in CURRENCY_LIST.keys():
            result.append(currency)
        return result

    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        try:
            base_currency = base.lower()
            quote_currency = quote.lower()
            if base_currency not in CURRENCY_LIST.keys():
                raise APIException(f'Валюта {base} не найдена в списке доступных для конвертации!')
            if quote_currency not in CURRENCY_LIST.keys():
                raise APIException(f'Валюта {quote} не найдена в списке доступных для конвертации!')
            if base_currency == quote_currency:
                raise APIException('Валюты должны быть разными!')
            amount_float = float(amount)
        except ValueError:
            raise APIException('Количество конвертируемой валюты должно быть указано в виде числа!')
        else:
            pair_currency = CURRENCY_LIST[base_currency] + CURRENCY_LIST[quote_currency]
            res = requests.get(f'{SOURCE}?get=rates&pairs={pair_currency}&key={TOKEN_CUR}')
            currency = json.loads(res.content)
            return float(currency['data'][pair_currency]) * amount_float
