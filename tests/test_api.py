"""
Comprehensive API test for py-kabusapi
Tests all py-kabusapi APIs including WebSocket functionality with proper rate limiting:
- Order APIs: 5 requests/second (200ms between calls) - SKIPPED in production
- Other APIs: 10 requests/second (100ms between calls)
"""

import json
import os
import threading
import time
from typing import Literal
from unittest.mock import Mock, patch

import pytest

from py_kabusapi import KabuStationAPI
from py_kabusapi.const import ApiResultCategory
from py_kabusapi.response_model import WebSocketPushData


@pytest.mark.api_integration
class TestRestApi:
    """Tests all py-kabusapi REST APIs sequentially with proper rate limiting"""

    # Rate limits in seconds
    ORDER_API_DELAY = 0.2  # 5 requests/sec = 200ms between calls
    OTHER_API_DELAY = 0.1  # 10 requests/sec = 100ms between calls

    # Test data
    TEST_SYMBOL = "9433@1"  # KDDI at Tokyo Stock Exchange
    TEST_SYMBOL_SIMPLE = "9433"  # KDDI simple symbol

    @pytest.fixture(scope="class")
    def api_client(self):
        """Create and authenticate API client"""
        host_name = (
            "host.docker.internal"
            if os.getenv("KABUS_DOCKER", "true") == "true"
            else os.getenv("KABUS_HOST", "localhost")
        )
        env_str = os.getenv("KABUS_ENV", "production")
        environment: Literal["test", "production"] = "production" if env_str == "production" else "test"
        is_docker = os.getenv("KABUS_DOCKER", "true").lower() == "true"

        api = KabuStationAPI(host_name=host_name, environment=environment, is_in_docker_container=is_docker)

        # Authenticate
        api_password = os.getenv("KABUS_PASSWORD", "CHANGE_ME_FOR_TESTING")
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
    @pytest.mark.test_env
    def test_01_authentication(self):
        """Test authentication API"""
        host_name = os.getenv("KABUS_HOST", "localhost")
        env_str = os.getenv("KABUS_ENV", "production")
        environment: Literal["test", "production"] = "production" if env_str == "production" else "test"
        is_docker = os.getenv("KABUS_DOCKER", "true").lower() == "true"

        api = KabuStationAPI(host_name=host_name, environment=environment, is_in_docker_container=is_docker)

        api_password = os.getenv("KABUS_PASSWORD", "CHANGE_ME_FOR_TESTING")
        token_response = api.token(api_password)

        assert hasattr(token_response, "api_result_category")
        assert token_response.api_result_category == ApiResultCategory.SUCCESS
        assert hasattr(token_response.content, "Token")
        assert len(token_response.content.Token) > 0

    # Information API tests (10 req/sec)
    @pytest.mark.prod_env
    def test_02_board_by_symbol(self, api_client):
        """Test board information API"""
        result = self.api_call_with_rate_limit(
            api_client.board_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_03_symbol_by_symbol(self, api_client):
        """Test symbol information API"""
        result = self.api_call_with_rate_limit(
            api_client.symbol_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.test_env
    def test_04_orders(self, api_client):
        """Test orders list API"""
        result = self.api_call_with_rate_limit(api_client.orders, self.OTHER_API_DELAY)
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.test_env
    def test_05_positions(self, api_client):
        """Test positions list API"""
        result = self.api_call_with_rate_limit(api_client.positions, self.OTHER_API_DELAY)
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.test_env
    def test_06_ranking(self, api_client):
        """Test ranking API"""
        result = self.api_call_with_rate_limit(
            api_client.ranking,
            self.OTHER_API_DELAY,
            type="1",  # Price increase rate ranking
            exchange_division="ALL",
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_07_regulations_by_symbol(self, api_client):
        """Test regulations API"""
        result = self.api_call_with_rate_limit(
            api_client.regulations_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_08_primaryexchange_by_symbol(self, api_client):
        """Test primary exchange API"""
        result = self.api_call_with_rate_limit(
            api_client.primaryexchange_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL_SIMPLE
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_09_apisoftlimit(self, api_client):
        """Test API soft limit API"""
        result = self.api_call_with_rate_limit(api_client.apisoftlimit, self.OTHER_API_DELAY)
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_10_exchange_by_symbol(self, api_client):
        """Test exchange information API"""
        result = self.api_call_with_rate_limit(api_client.exchange_by_symbol, self.OTHER_API_DELAY, symbol="usdjpy")
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_11_symbolname_future(self, api_client):
        """Test future symbol name API"""
        result = self.api_call_with_rate_limit(
            api_client.symbolname_future, self.OTHER_API_DELAY, future_code="NK225", deriv_month=0
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_12_symbolname_option(self, api_client):
        """Test option symbol name API"""
        result = self.api_call_with_rate_limit(
            api_client.symbolname_option,
            self.OTHER_API_DELAY,
            option_code="NK225op",
            deriv_month=0,
            put_or_call="C",
            strike_price=40000,
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_13_symbolname_minioptionweekly(self, api_client):
        """Test mini option weekly symbol name API"""
        result = self.api_call_with_rate_limit(
            api_client.symbolname_minioptionweekly,
            self.OTHER_API_DELAY,
            deriv_month=0,
            deriv_weekly=0,
            put_or_call="C",
            strike_price=40000,
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    # Trading Margin API tests (10 req/sec)
    @pytest.mark.prod_env
    def test_14_wallet_cash(self, api_client):
        """Test cash wallet API"""
        result = self.api_call_with_rate_limit(api_client.wallet_cash, self.OTHER_API_DELAY)
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_15_wallet_cash_by_symbol(self, api_client):
        """Test cash wallet by symbol API"""
        result = self.api_call_with_rate_limit(
            api_client.wallet_cash_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_16_wallet_margin(self, api_client):
        """Test margin wallet API"""
        result = self.api_call_with_rate_limit(api_client.wallet_margin, self.OTHER_API_DELAY)
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_17_wallet_margin_by_symbol(self, api_client):
        """Test margin wallet by symbol API"""
        result = self.api_call_with_rate_limit(
            api_client.wallet_margin_by_symbol, self.OTHER_API_DELAY, symbol=self.TEST_SYMBOL
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_18_wallet_future(self, api_client):
        """Test future wallet API"""
        result = self.api_call_with_rate_limit(api_client.wallet_future, self.OTHER_API_DELAY)
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_19_wallet_future_by_symbol(self, api_client):
        """Test future wallet by symbol API"""
        result = self.api_call_with_rate_limit(
            api_client.wallet_future_by_symbol, self.OTHER_API_DELAY, symbol="160060018@2"
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_20_wallet_option(self, api_client):
        """Test option wallet API"""
        result = self.api_call_with_rate_limit(api_client.wallet_option, self.OTHER_API_DELAY)
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_21_wallet_option_by_symbol(self, api_client):
        """Test option wallet by symbol API"""
        result = self.api_call_with_rate_limit(
            api_client.wallet_option_by_symbol, self.OTHER_API_DELAY, symbol="140180018@2"
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.prod_env
    def test_22_margin_marginpremium_by_symbol(self, api_client):
        """Test margin premium API"""
        result = self.api_call_with_rate_limit(
            api_client.margin_marginpremium_by_symbol, self.OTHER_API_DELAY, symbol="9984"
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    # Symbol Registration API tests (10 req/sec)
    @pytest.mark.test_env
    def test_23_register(self, api_client):
        """Test symbol registration API"""
        result = self.api_call_with_rate_limit(
            api_client.register, self.OTHER_API_DELAY, symbols=[{"Symbol": self.TEST_SYMBOL_SIMPLE, "Exchange": 1}]
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.test_env
    def test_24_unregister(self, api_client):
        """Test symbol unregistration API"""
        result = self.api_call_with_rate_limit(
            api_client.unregister, self.OTHER_API_DELAY, symbols=[{"Symbol": self.TEST_SYMBOL_SIMPLE, "Exchange": 1}]
        )
        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.test_env
    def test_25_unregister_all(self, api_client):
        """Test unregister all symbols API"""
        result = self.api_call_with_rate_limit(api_client.unregister_all, self.OTHER_API_DELAY)
        assert result.api_result_category == ApiResultCategory.SUCCESS

    # Order APIs - Test environment only (5 req/sec)
    @pytest.mark.test_env
    def test_26_sendorder_stock(self, api_client):
        """Test stock order API in test environment"""
        result = self.api_call_with_rate_limit(
            api_client.sendorder,
            self.ORDER_API_DELAY,
            symbol="6659",
            exchange="1",
            security_type="1",
            side="2",  # Buy
            cash_margin="1",  # Cash
            deliv_type="2",  # 公式サンプル準拠
            account_type="2",  # 公式サンプル準拠
            qty=100,
            price=40,  # 公式サンプル準拠
            expire_day=0,
            front_order_type="20",  # 公式サンプル準拠
            margin_trade_type=None,
            fund_type="AA",  # 公式サンプル準拠
            reverse_limit_order=None,  # 明示的にNoneを設定
        )

        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.test_env
    def test_27_sendorder_future(self, api_client):
        """Test future order API in test environment"""
        result = self.api_call_with_rate_limit(
            api_client.sendorder_future,
            self.ORDER_API_DELAY,
            symbol="160060018",
            exchange="2",
            trade_type="1",
            time_in_force="1",
            side="2",  # Buy
            qty=1,
            price=39000.0,  # 具体的な価格を指定
            expire_day=0,
            front_order_type="20",  # 指値注文
            reverse_limit_order=None,  # 明示的にNoneを設定
        )

        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.test_env
    def test_28_sendorder_option(self, api_client):
        """Test option order API in test environment"""
        # テスト環境で有効なオプションシンボルコードを試す
        # 260xxxxxx番台がオプションシンボルの可能性
        result = self.api_call_with_rate_limit(
            api_client.sendorder_option,
            self.ORDER_API_DELAY,
            symbol="140180018",  # オプション用のシンボルコード（推測）
            exchange="2",
            trade_type="1",
            time_in_force="1",
            side="2",  # Buy
            qty=1,
            price=140.0,  # 指値価格
            expire_day=0,
            front_order_type="20",  # 指値注文
            reverse_limit_order=None,
        )

        assert result.api_result_category == ApiResultCategory.SUCCESS

    @pytest.mark.skip(reason="Does not work in test environment and is dangerous in production")
    def test_29_cancelorder(self, api_client):
        """Test cancel order API - skipped as it cannot be executed safely"""
        pass


@pytest.mark.websocket
class TestPushApi:
    """Tests WebSocket Push API functionality"""

    # Test data
    TEST_SYMBOL = "9433"  # KDDI
    TEST_SYMBOLS = [{"Symbol": TEST_SYMBOL, "Exchange": 1}]

    @pytest.fixture(scope="class")
    def api_client(self):
        """Create and authenticate API client"""
        host_name = os.getenv("KABUS_HOST", "localhost")
        env_str = os.getenv("KABUS_ENV", "production")
        environment: Literal["test", "production"] = "production" if env_str == "production" else "test"
        is_docker = os.getenv("KABUS_DOCKER", "true").lower() == "true"

        api = KabuStationAPI(host_name=host_name, environment=environment, is_in_docker_container=is_docker)

        # Authenticate
        api_password = os.getenv("KABUS_PASSWORD", "CHANGE_ME_FOR_TESTING")
        token_response = api.token(api_password)

        assert hasattr(token_response, "api_result_category")
        assert token_response.api_result_category == ApiResultCategory.SUCCESS

        return api

    @pytest.mark.test_env
    def test_websocket_url_generation(self):
        """Test WebSocket URL generation"""
        # Test environment
        api = KabuStationAPI(host_name="localhost", environment="test", is_in_docker_container=False)
        expected_url = "ws://localhost:18081/kabusapi/websocket"
        assert api.websocket_url == expected_url

        # Production environment
        api = KabuStationAPI(host_name="localhost", environment="production", is_in_docker_container=False)
        expected_url = "ws://localhost:18080/kabusapi/websocket"
        assert api.websocket_url == expected_url

        # Docker container
        api = KabuStationAPI(host_name="localhost", environment="test", is_in_docker_container=True)
        expected_url = "ws://host.docker.internal:18081/kabusapi/websocket"
        assert api.websocket_url == expected_url

    @pytest.mark.test_env
    def test_websocket_connection_without_token(self):
        """Test WebSocket connection without authentication token"""
        api = KabuStationAPI()

        with pytest.raises(ValueError, match="API token is not set"):
            api.start_websocket()

    @pytest.mark.test_env
    def test_websocket_connection_state(self, api_client):
        """Test WebSocket connection state management"""
        # Initially not connected
        assert not api_client.is_websocket_connected()

        # Mock WebSocket for testing
        with patch("websocket.WebSocketApp") as mock_ws_app:
            mock_ws_instance = Mock()
            mock_ws_app.return_value = mock_ws_instance

            # Mock thread
            with patch("threading.Thread") as mock_thread:
                mock_thread_instance = Mock()
                mock_thread_instance.is_alive.return_value = True
                mock_thread.return_value = mock_thread_instance

                # Start WebSocket
                api_client.start_websocket()

                # Should be connected (mocked)
                assert api_client.ws is not None
                assert api_client.ws_thread is not None

                # Test double connection error
                with pytest.raises(ValueError, match="WebSocket is already connected"):
                    api_client.start_websocket()

                # Stop WebSocket
                api_client.stop_websocket()

                # Should be disconnected
                assert api_client.ws is None
                assert api_client.ws_thread is None

    @pytest.mark.test_env
    def test_websocket_callbacks(self, api_client):
        """Test WebSocket callback functionality"""
        message_received = threading.Event()
        error_occurred = threading.Event()
        connected = threading.Event()
        disconnected = threading.Event()

        received_data = []
        received_errors = []

        def on_message(data: WebSocketPushData):
            received_data.append(data)
            message_received.set()

        def on_error(error: Exception):
            received_errors.append(error)
            error_occurred.set()

        def on_connect():
            connected.set()

        def on_disconnect():
            disconnected.set()

        with patch("websocket.WebSocketApp") as mock_ws_app:
            mock_ws_instance = Mock()
            mock_ws_app.return_value = mock_ws_instance

            with patch("threading.Thread") as mock_thread:
                mock_thread_instance = Mock()
                mock_thread_instance.is_alive.return_value = True
                mock_thread.return_value = mock_thread_instance

                # Start WebSocket with callbacks
                api_client.start_websocket(
                    on_message=on_message, on_error=on_error, on_connect=on_connect, on_disconnect=on_disconnect
                )

                # Verify callbacks are set
                assert api_client.on_message_callback == on_message
                assert api_client.on_error_callback == on_error
                assert api_client.on_connect_callback == on_connect
                assert api_client.on_disconnect_callback == on_disconnect

                # Simulate message reception
                test_message = {
                    "Symbol": "9433@1",
                    "SymbolName": "ＫＤＤＩ",
                    "Exchange": 1,
                    "ExchangeName": "東証プライム",
                    "CurrentPrice": 5000.0,
                    "CurrentPriceTime": "2025-01-06T09:00:00+09:00",
                }

                # Get the on_message callback that was passed to WebSocketApp
                ws_on_message = mock_ws_app.call_args[1]["on_message"]
                ws_on_message(mock_ws_instance, json.dumps(test_message))

                # Wait a bit for callback processing
                time.sleep(0.1)

                # Verify message was processed
                assert len(received_data) == 1
                assert received_data[0].Symbol == "9433@1"
                assert received_data[0].CurrentPrice == 5000.0

                api_client.stop_websocket()

    @pytest.mark.test_env
    def test_websocket_message_parsing_error(self, api_client):
        """Test WebSocket message parsing error handling"""
        error_occurred = threading.Event()
        received_errors = []

        def on_error(error: Exception):
            received_errors.append(error)
            error_occurred.set()

        with patch("websocket.WebSocketApp") as mock_ws_app:
            mock_ws_instance = Mock()
            mock_ws_app.return_value = mock_ws_instance

            with patch("threading.Thread") as mock_thread:
                mock_thread_instance = Mock()
                mock_thread_instance.is_alive.return_value = True
                mock_thread.return_value = mock_thread_instance

                api_client.start_websocket(on_error=on_error)

                # Simulate invalid JSON message
                ws_on_message = mock_ws_app.call_args[1]["on_message"]
                ws_on_message(mock_ws_instance, "invalid json")

                # Wait a bit for error processing
                time.sleep(0.1)

                # Verify error was caught
                assert len(received_errors) > 0

                api_client.stop_websocket()

    @pytest.mark.test_env
    def test_send_websocket_message(self, api_client):
        """Test sending messages via WebSocket"""
        with patch("websocket.WebSocketApp") as mock_ws_app:
            mock_ws_instance = Mock()
            mock_ws_app.return_value = mock_ws_instance

            with patch("threading.Thread") as mock_thread:
                mock_thread_instance = Mock()
                mock_thread_instance.is_alive.return_value = True
                mock_thread.return_value = mock_thread_instance

                api_client.start_websocket()

                # Test sending message
                test_message = "test message"
                api_client.send_websocket_message(test_message)

                # Verify send was called
                mock_ws_instance.send.assert_called_once_with(test_message)

                api_client.stop_websocket()

    @pytest.mark.test_env
    def test_send_websocket_message_without_connection(self, api_client):
        """Test sending message without WebSocket connection"""
        with pytest.raises(ValueError, match="WebSocket is not connected"):
            api_client.send_websocket_message("test")

    @pytest.mark.test_env
    def test_websocket_headers(self, api_client):
        """Test WebSocket headers are properly set"""
        with patch("websocket.WebSocketApp") as mock_ws_app:
            with patch("threading.Thread") as mock_thread:
                mock_thread_instance = Mock()
                mock_thread_instance.is_alive.return_value = True
                mock_thread.return_value = mock_thread_instance

                api_client.start_websocket()

                # Verify WebSocketApp was called with correct headers
                call_args = mock_ws_app.call_args
                headers = call_args[1]["header"]

                assert "X-API-KEY" in headers
                assert headers["X-API-KEY"] == api_client.x_api_key

                api_client.stop_websocket()

    @pytest.mark.test_env
    def test_websocket_headers_with_docker(self):
        """Test WebSocket headers with Docker container setup"""
        host_name = os.getenv("KABUS_HOST", "localhost")
        env_str = os.getenv("KABUS_ENV", "production")
        environment: Literal["test", "production"] = "production" if env_str == "production" else "test"

        api = KabuStationAPI(host_name=host_name, environment=environment, is_in_docker_container=True)

        # Authenticate
        api_password = os.getenv("KABUS_PASSWORD", "CHANGE_ME_FOR_TESTING")
        token_response = api.token(api_password)
        assert token_response.api_result_category == ApiResultCategory.SUCCESS

        with patch("websocket.WebSocketApp") as mock_ws_app:
            with patch("threading.Thread") as mock_thread:
                mock_thread_instance = Mock()
                mock_thread_instance.is_alive.return_value = True
                mock_thread.return_value = mock_thread_instance

                api.start_websocket()

                # Verify WebSocketApp was called with Docker headers
                call_args = mock_ws_app.call_args
                headers = call_args[1]["header"]

                assert "X-API-KEY" in headers
                assert "Host" in headers
                assert headers["Host"] == "localhost"

                api.stop_websocket()

    @pytest.mark.test_env
    @pytest.mark.skip(reason="Real WebSocket connection test skipped due to time dependency")
    def test_websocket_real_connection(self, api_client):
        """Real WebSocket connection test (requires actual kabuステーション)"""
        if os.getenv("SKIP_REAL_TESTS", "true").lower() == "true":
            pytest.skip("Real tests skipped (set SKIP_REAL_TESTS=false to enable)")

        message_received = threading.Event()
        connection_established = threading.Event()
        received_data = []

        def on_message(data: WebSocketPushData):
            received_data.append(data)
            message_received.set()

        def on_connect():
            connection_established.set()

        def on_error(error: Exception):
            pytest.fail(f"WebSocket error: {error}")

        try:
            # Register test symbol first
            register_result = api_client.register(self.TEST_SYMBOLS)
            assert register_result.api_result_category == ApiResultCategory.SUCCESS

            # Start WebSocket
            api_client.start_websocket(on_message=on_message, on_connect=on_connect, on_error=on_error)

            # Wait for connection
            connection_established.wait(timeout=10)
            assert api_client.is_websocket_connected()

            # Wait for potential message (may not receive one immediately)
            message_received.wait(timeout=5)

            # Test is successful if no errors occurred
            assert True

        finally:
            # Clean up
            api_client.stop_websocket()
            api_client.unregister_all()

            # Verify disconnection
            assert not api_client.is_websocket_connected()


@pytest.mark.websocket_model
class TestWebSocketPushData:
    """Tests for WebSocketPushData model"""

    @pytest.mark.test_env
    def test_websocket_push_data_creation(self):
        """Test WebSocketPushData model creation"""
        data = {
            "Symbol": "9433@1",
            "SymbolName": "ＫＤＤＩ",
            "Exchange": 1,
            "ExchangeName": "東証プライム",
            "CurrentPrice": 5000.0,
            "CurrentPriceTime": "2025-01-06T09:00:00+09:00",
        }

        push_data = WebSocketPushData(**data)

        assert push_data.Symbol == "9433@1"
        assert push_data.SymbolName == "ＫＤＤＩ"
        assert push_data.Exchange == 1
        assert push_data.ExchangeName == "東証プライム"
        assert push_data.CurrentPrice == 5000.0
        assert push_data.CurrentPriceTime == "2025-01-06T09:00:00+09:00"

    @pytest.mark.test_env
    def test_websocket_push_data_minimal(self):
        """Test WebSocketPushData with minimal required fields"""
        data = {"Symbol": "9433@1", "Exchange": 1}
        push_data = WebSocketPushData(**data)
        assert push_data.Symbol == "9433@1"
        assert push_data.Exchange == 1
