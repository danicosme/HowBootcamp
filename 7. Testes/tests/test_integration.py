#Teste de caixa preta -> testa somente a saída
import datetime
import pytest
from mercado_bitcoin.api import BtcApi

class TestDaySummaryApi:
    # def test_get_data(self):
    #     actual = BtcApi(coin = 'BTC').get_data(date=datetime.date(2022,6,1))
    #     expected = {'amount': 4621,'avg_price': 146789.82685081,'closing': 144596.32749,'date': '2022-06-01','highest': 152000,'lowest': 142396.02574,'opening': 151441.99999998,'quantity': '47.31859469','volume': '6945888.32136877'} == {'amount': 4621,'avg_price': 146789.82685081,'closing': 144596.32749,'date': '2022-06-01'}
    #     assert actual == expected

    def test_get_data_better(self):
        actual = BtcApi(coin = 'BTC').get_data(date=datetime.date(2022,6,1)).get('date')
        expected ='2022-06-01'
        assert actual == expected