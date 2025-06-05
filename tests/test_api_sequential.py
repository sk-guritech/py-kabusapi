"""
Sequential API test using pytest
Tests all py-kabusapi APIs in sequence while respecting rate limits:
- Order APIs: 5 requests/second (200ms between calls) - SKIPPED in production
- Other APIs: 10 requests/second (100ms between calls)
"""

import os
import time
from typing import Literal

import pytest

from py_kabusapi import KabuStationAPI
from py_kabusapi.const import ApiResultCategory


@pytest.mark.api_integration
class TestSequentialApi:
    """Tests all py-kabusapi APIs sequentially with proper rate limiting"""

    # Rate limits in seconds
    ORDER_API_DELAY = 0.2  # 5 requests/sec = 200ms between calls
    OTHER_API_DELAY = 0.1  # 10 requests/sec = 100ms between calls

    # Test data
    TEST_SYMBOL = "9433@1"  # KDDI at Tokyo Stock Exchange
    TEST_SYMBOL_SIMPLE = "9433"  # KDDI simple symbol

    @pytest.fixture(scope="class")
    def api_client(self):
        """Create and authenticate API client"""
        host_name = os.getenv("KABUS_HOST", "localhost")
        env_str = os.getenv("KABUS_ENV", "production")
        environment: Literal["test", "production"] = "production" if env_str == "production" else "test"
        is_docker = os.getenv("KABUS_DOCKER", "true").lower() == "true"

        api = KabuStationAPI(host_name=host_name, environment=environment, is_in_docker_container=is_docker)

        # Authenticate
        api_password = os.getenv("KABUS_PASSWORD", "testpassword")
        token_response = api.token(api_password)

        assert hasattr(token_response, "api_result_category")
        assert token_response.api_result_category == ApiResultCategory.SUCCESS

        return api

    def api_call_with_rate_limit(self, api_func, delay: float, *args, **kwargs):
        """Call API with proper rate limiting"""
        result = api_func(*args, **kwargs)
        time.sleep(delay)
        return result

    # Authentication test
    def test_01_authentication(self):
        """Test authentication API"""
        host_name = os.getenv("KABUS_HOST", "localhost")
        env_str = os.getenv("KABUS_ENV", "production")
        environment: Literal["test", "production"] = "production" if env_str == "production" else "test"
        is_docker = os.getenv("KABUS_DOCKER", "true").lower() == "true"

        api = KabuStationAPI(host_name=host_name, environment=environment, is_in_docker_container=is_docker)

        api_password = os.getenv("KABUS_PASSWORD", "testpassword")
        token_response = api.token(api_password)

        assert hasattr(token_response, "api_result_category")
        assert token_response.api_result_category == ApiResultCategory.SUCCESS
        assert hasattr(token_response.content, "Token")
        assert len(token_response.content.Token) > 0

    # Information API tests (10 req/sec)
    def test_02_board_by_symbol(self, api_client):
        """Test board information API"""
        result = self.api_call_with_rate_limit(
            api_client.board_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result is not None

    def test_03_symbol_by_symbol(self, api_client):
        """Test symbol information API"""
        result = self.api_call_with_rate_limit(
            api_client.symbol_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result is not None

    def test_04_orders(self, api_client):
        """Test orders list API"""
        result = self.api_call_with_rate_limit(api_client.orders, self.OTHER_API_DELAY)
        assert result is not None

    def test_05_positions(self, api_client):
        """Test positions list API"""
        result = self.api_call_with_rate_limit(api_client.positions, self.OTHER_API_DELAY)
        assert result is not None

    def test_06_ranking(self, api_client):
        """Test ranking API"""
        result = self.api_call_with_rate_limit(
            api_client.ranking,
            self.OTHER_API_DELAY,
            type="1",  # Price increase rate ranking
            exchange_division="ALL",
        )
        assert result is not None

    def test_07_regulations_by_symbol(self, api_client):
        """Test regulations API"""
        result = self.api_call_with_rate_limit(
            api_client.regulations_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result is not None

    def test_08_primaryexchange_by_symbol(self, api_client):
        """Test primary exchange API"""
        result = self.api_call_with_rate_limit(
            api_client.primaryexchange_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL_SIMPLE
        )
        assert result is not None

    def test_09_apisoftlimit(self, api_client):
        """Test API soft limit API"""
        result = self.api_call_with_rate_limit(api_client.apisoftlimit, self.OTHER_API_DELAY)
        assert result is not None

    def test_10_exchange_by_symbol(self, api_client):
        """Test exchange information API"""
        result = self.api_call_with_rate_limit(api_client.exchange_by_symbol, self.OTHER_API_DELAY, symbol="usdjpy")
        assert result is not None

    def test_11_symbolname_future(self, api_client):
        """Test future symbol name API"""
        result = self.api_call_with_rate_limit(
            api_client.symbolname_future, self.OTHER_API_DELAY, future_code="NK225", deriv_month=202503
        )
        assert result is not None

    def test_12_symbolname_option(self, api_client):
        """Test option symbol name API"""
        result = self.api_call_with_rate_limit(
            api_client.symbolname_option,
            self.OTHER_API_DELAY,
            option_code="NK225op",
            deriv_month=202503,
            put_or_call="C",
            strike_price=40000,
        )
        assert result is not None

    def test_13_symbolname_minioptionweekly(self, api_client):
        """Test mini option weekly symbol name API"""
        result = self.api_call_with_rate_limit(
            api_client.symbolname_minioptionweekly,
            self.OTHER_API_DELAY,
            deriv_month=202503,
            deriv_weekly=1,
            put_or_call="C",
            strike_price=40000,
        )
        assert result is not None

    # Trading Margin API tests (10 req/sec)
    def test_14_wallet_cash(self, api_client):
        """Test cash wallet API"""
        result = self.api_call_with_rate_limit(api_client.wallet_cash, self.OTHER_API_DELAY)
        assert result is not None

    def test_15_wallet_cash_by_symbol(self, api_client):
        """Test cash wallet by symbol API"""
        result = self.api_call_with_rate_limit(
            api_client.wallet_cash_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result is not None

    def test_16_wallet_margin(self, api_client):
        """Test margin wallet API"""
        result = self.api_call_with_rate_limit(api_client.wallet_margin, self.OTHER_API_DELAY)
        assert result is not None

    def test_17_wallet_margin_by_symbol(self, api_client):
        """Test margin wallet by symbol API"""
        result = self.api_call_with_rate_limit(
            api_client.wallet_margin_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result is not None

    def test_18_wallet_future(self, api_client):
        """Test future wallet API"""
        result = self.api_call_with_rate_limit(api_client.wallet_future, self.OTHER_API_DELAY)
        assert result is not None

    def test_19_wallet_future_by_symbol(self, api_client):
        """Test future wallet by symbol API"""
        result = self.api_call_with_rate_limit(
            api_client.wallet_future_by_symbol, self.OTHER_API_DELAY, symbol="NK225mini"
        )
        assert result is not None

    def test_20_wallet_option(self, api_client):
        """Test option wallet API"""
        result = self.api_call_with_rate_limit(api_client.wallet_option, self.OTHER_API_DELAY)
        assert result is not None

    def test_21_wallet_option_by_symbol(self, api_client):
        """Test option wallet by symbol API"""
        result = self.api_call_with_rate_limit(
            api_client.wallet_option_by_symbol, self.OTHER_API_DELAY, symbol="NK225op"
        )
        assert result is not None

    def test_22_margin_marginpremium_by_symbol(self, api_client):
        """Test margin premium API"""
        result = self.api_call_with_rate_limit(
            api_client.margin_marginpremium_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result is not None

    # Symbol Registration API tests (10 req/sec)
    def test_23_register(self, api_client):
        """Test symbol registration API"""
        result = self.api_call_with_rate_limit(
            api_client.register, self.OTHER_API_DELAY, symbols=[{"Symbol": self.TEST_SYMBOL_SIMPLE, "Exchange": 1}]
        )
        assert result is not None

    def test_24_unregister(self, api_client):
        """Test symbol unregistration API"""
        result = self.api_call_with_rate_limit(
            api_client.unregister, self.OTHER_API_DELAY, symbols=[{"Symbol": self.TEST_SYMBOL_SIMPLE, "Exchange": 1}]
        )
        assert result is not None

    def test_25_unregister_all(self, api_client):
        """Test unregister all symbols API"""
        result = self.api_call_with_rate_limit(api_client.unregister_all, self.OTHER_API_DELAY)
        assert result is not None

    # Order APIs are skipped in production testing
    @pytest.mark.skip(reason="Order APIs skipped in production testing to prevent accidental trades")
    def test_order_apis_skipped(self):
        """Order APIs (sendorder, sendorder_future, sendorder_option, cancelorder) are skipped"""
        pass
