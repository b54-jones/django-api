import pytest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime, timedelta
import os

from .views import BitcoinInfoView

@pytest.fixture
def bitcoin_info_view():
    return BitcoinInfoView()

@patch('requests.get')
def test_get_15m_price_success(mock_get, bitcoin_info_view):
    mock_response = {
        "EUR": {
            "15m": 30000.5
        }
    }

    mock_get.return_value = MagicMock(content=json.dumps(mock_response))

    price = bitcoin_info_view.get_15m_price()

    assert price == 30000.5
    mock_get.assert_called_once_with("https://blockchain.info/ticker")

@patch('requests.get', side_effect=Exception('API Error'))
def test_get_15m_price_failure(mock_get, bitcoin_info_view):
    with pytest.raises(ValueError, match="Failed to get 15m delayed price: API Error"):
        bitcoin_info_view.get_15m_price()

@patch('bitcoin_api.views.datetime')
def test_get_date_month_ago(mock_datetime, bitcoin_info_view):
    mock_datetime.now.return_value = datetime(2024, 12, 18)
    expected_date = "2024-11-18"

    assert bitcoin_info_view.get_date_month_ago() == expected_date


@patch("bitcoin_api.views.requests.get")
@patch("bitcoin_api.views.os.getenv")
@patch("bitcoin_api.views.BitcoinInfoView.get_date_month_ago")
def test_get_exchange_rate(mock_get_date_month_ago, mock_getenv, mock_get, bitcoin_info_view):

    mock_date = "2024-11-18"
    mock_api_key = "dummy_api_key"
    mock_response = {
        "rates": {
            "GBP": 0.85
        }
    }

    mock_get_date_month_ago.return_value = mock_date
    mock_getenv.return_value = mock_api_key
    mock_get.return_value = MagicMock(content=json.dumps(mock_response))

    exchange_rate = bitcoin_info_view.get_exchange_rate()
    expected_url = f"https://api.exchangeratesapi.io/{mock_date}?base=EUR&access_key={mock_api_key}"

    assert exchange_rate == 0.85
    mock_get.assert_called_once_with(expected_url)

@patch("bitcoin_api.views.requests.get", side_effect=Exception('API Error'))
@patch("bitcoin_api.views.os.getenv", return_value="dummy_api_key")
@patch("bitcoin_api.views.BitcoinInfoView.get_date_month_ago", return_value="2024-11-18")
def test_get_exchange_rate_fail(mock_get_date_month_ago, mock_getenv, mock_get, bitcoin_info_view):
    with pytest.raises(ValueError, match="Failed to get exchange rate: API Error"):
        bitcoin_info_view.get_exchange_rate()
