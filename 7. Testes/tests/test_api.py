import pytest
import datetime
from unittest.mock import patch, mock_open

from requests import request
from mercado_bitcoin.api import BtcApi, MercadoBitcoinApi, TradesApi

#python -m pytest
#python -m pytest --cov=mercado_bitcoin tests/
class TestDaySummary:
    @pytest.mark.parametrize(
        'coin, date, expected',
        [
            ('BTC', datetime.date(2022,6,1), 'https://www.mercadobitcoin.net/api/BTC/day-summary/2022/6/1'),
            ('ETH', datetime.date(2022,6,1), 'https://www.mercadobitcoin.net/api/ETH/day-summary/2022/6/1'),
            #('BTC', datetime.date(2022,6,13), 'https://www.mercadobitcoin.net/api/BTC/day-summary/2022/6/13')
        ]
    )
    def test_get_endpoint(self,coin, date, expected):
        api = BtcApi(coin=coin)
        actual = api._get_endpoint(date=date) #valor que o endpoint vai retornar
        assert actual == expected


class TestTradesApi:
    @pytest.mark.parametrize(
        'coin, date_to, date_from, expected',
        [
            ('TEST', datetime.datetime(2022, 6, 1), datetime.datetime(2022, 6, 3), 'https://www.mercadobitcoin.net/api/TEST/trades/1654225200/1654052400'),
            ('TEST', None, None, 'https://www.mercadobitcoin.net/api/TEST/trades/'),
            ('TEST', None, datetime.datetime(2022, 6, 3), 'https://www.mercadobitcoin.net/api/TEST/trades/1654225200'),
            ('TEST', datetime.datetime(2022, 6, 1), None, 'https://www.mercadobitcoin.net/api/TEST/trades/')
        ]
    )
    def test_get_endpoint(self, coin, date_to, date_from, expected):
        actual = TradesApi(coin=coin)._get_endpoint(date_to=date_to,date_from=date_from) #valor que o endpoint vai retornar
        assert actual == expected

    
    # def test_get_endpoint_date_from_greater_date_to(self):
    #     with pytest.raises(RuntimeError):
    #         TradesApi(coin='TEST')._get_endpoint(
    #             date_from= datetime.datetime(2022,6,1),
    #             date_to= datetime.datetime(2022,6,3)
    #         )

    @pytest.mark.parametrize(
        'date, expected',
        [
            (datetime.datetime(2022,6,1), 1654052400),
            (datetime.datetime(2022,6,1), int(datetime.datetime(2022,6,1).timestamp())),
            (datetime.datetime(2022,6,3), 1654225200)
        ]
    )
    def test_get_unix_epoch(self, date, expected):
        actual = TradesApi(coin='Teste')._get_unix_epoch(date)
        assert actual == expected


@pytest.fixture()
@patch('mercado_bitcoin.api.MercadoBitcoinApi.__abstractmethods__', set())
def fixture_mercado_bitcoin_api():
    return MercadoBitcoinApi(coin='test')

#Monkey patches
def mocked_requests_get(*args, **kwargs):
    class MockResponse(request.Response):
        def __init__(self, json_data, status_code):
            super().__init__()
            self.status_code = status_code
            self.json_data = json_data
        
        def json(self):
            return self.json_data
        
        def raise_for_status(self) -> None:
            if self.status_code != 200:
                raise Exception
    
    if args[0] == 'valid_endpoint':
        return MockResponse(json_data={'foo':'bar'}, status_code=200)
    else:
        return MockResponse(json_data=None, status_code=404)



class TestMercadoBitcoinApi:
    @patch('requests.get')
    @patch('mercado_bitcoin.api.MercadoBitcoinApi._get_endpoint', return_value='valid_endpoint')
    def test_get_data_requests_is_called(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        fixture_mercado_bitcoin_api.get_data()
        mock_requests.assert_called_once_with('valid_endpoint')

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('api.MercadoBitcoinApi._get_endpoint', return_value='valid_endpoint')
    def text_get_data_with_valid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        actual = fixture_mercado_bitcoin_api.get_data()
        expected = {'foo':'bar'}
        assert actual == expected

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('mercado_bitcoin.api.MercadoBitcoinApi._get_endpoint', return_value='valid_endpoint')
    def text_get_data_with_valid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        with pytest.raises(Exception):
            fixture_mercado_bitcoin_api.get_data()