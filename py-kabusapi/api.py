import json
import sys
from enum import IntEnum
from typing import Any, Dict, Literal

import requests
from error import OrderPlacementError, RequestCheckError


class ApiCategory(IntEnum):
    AUTHENTICATION = 0
    ORDER_PLACEMENT = 1
    TRADING_CAPACITY = 2
    INFORMATION = 3
    STOCK_REGISTRATION = 4


class KabuStationAPI:
    def __init__(
        self,
        host_name: str = "localhost",
        environment: Literal["test"] | Literal["production"] = "test",
        is_in_docker_container: bool = False,
    ):
        def __generate_base_url(
            host_name: str, environment: Literal["test"] | Literal["production"], is_in_docker_container: bool
        ):
            if environment == "test":
                port = 18081
            else:
                port = 18080

            if is_in_docker_container:
                host_name = "host.docker.internal"

            return f"http://{host_name}:{port}/kabusapi"

        self.is_in_docker_container = is_in_docker_container
        self.base_url = __generate_base_url(host_name, environment, is_in_docker_container)
        self.x_api_key: str | None = None

    def call_api(self, path: str, api_category: ApiCategory, method: str, payload={}) -> dict:
        def __build_headers(api_category: ApiCategory):
            headers = {
                "content-type": "application/json",
            }

            if self.is_in_docker_container:
                headers["Host"] = "localhost"

            if api_category != ApiCategory.AUTHENTICATION:
                if not self.x_api_key:
                    raise ValueError("API token is not set. Call 'token' method first.")

                headers["X-API-KEY"] = self.x_api_key

            return headers

        def __extract_result(api_category: ApiCategory, response_json: dict) -> int | None:
            if api_category == ApiCategory.AUTHENTICATION:
                return response_json.get("ResultCode", None)

            elif api_category == ApiCategory.ORDER_PLACEMENT:
                return response_json.get("Result", None)

            else:
                return None

        headers = __build_headers(api_category)
        url = f"{self.base_url}/{path}"

        if method == "GET":
            response = requests.request(method, url, headers=headers)
        else:
            response = requests.request(method, url, headers=headers, data=json.dumps(payload).encode("utf-8"))

        try:
            response_json: dict = response.json()

        except requests.exceptions.JSONDecodeError:
            raise ValueError("Unexpected response")

        if response.status_code == 200:
            if result := __extract_result(api_category, response_json):
                order_placement_error = OrderPlacementError.from_code(result)
                print(order_placement_error, file=sys.stderr)

        else:
            code: int = response_json["Code"]
            request_check_error = RequestCheckError.from_code(code)
            print(request_check_error, file=sys.stderr)

        return response_json

    def token(self, api_password: str) -> Dict[str, Any]:
        """
        APIトークンを発行します。発行したトークンはインスタンス内に保存され、以降のAPI呼び出しで使用されます。

        Args:
            api_password (str): パスワード。

        Returns:
            {"ResultCode": int, "Token": str}

        """
        payload = {
            "APIPassword": api_password,
        }

        response_json = self.call_api("token", ApiCategory.AUTHENTICATION, "POST", payload)

        if "ResultCode" in response_json and response_json["ResultCode"] == 0:
            self.x_api_key = response_json["Token"]

        return response_json

    def wallet_cash(self) -> Dict[str, Any]:
        """
        口座の取引余力（現物）を取得します。

        Returns:
            {"StockAccountWalletnumber": float, "AuKCStockAccountWalletnumber": float, "AuJbnStockAccountWalletnumber": float}
        """
        response_json = self.call_api("wallet/cash", ApiCategory.TRADING_CAPACITY, "GET")

        return response_json

    def get_wallet_cash_by_symbol(self, symbol: str) -> dict:
        """
        指定した銘柄の現物買付可能額を取得します。

        Args:
            symbol (str): 銘柄コード。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - StockAccountWallet (float): 現物買付可能額。
                - AuKCStockAccountWallet (float): うち、三菱UFJ eスマート証券可能額。
                - AuJbnStockAccountWallet (float): うち、auじぶん銀行残高。
        """
        response_json = self.call_api(f"wallet/cash/{symbol}", ApiCategory.TRADING_CAPACITY, "GET")
        return response_json

    def get_wallet_margin(self) -> dict:
        """
        信用新規可能額を取得します。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - MarginAccountWallet (float): 信用新規可能額。
                - DepositkeepRate (float): 保証金維持率。銘柄指定の場合のみ。
                - ConsignmentDepositRate (float): 委託保証金率。銘柄指定の場合のみ。
                - CashOfConsignmentDepositRate (float): 現金委託保証金率。銘柄指定の場合のみ。
        """
        response_json = self.call_api("wallet/margin", ApiCategory.TRADING_CAPACITY, "GET")
        return response_json

    def get_wallet_margin_by_symbol(self, symbol: str) -> dict:
        """
        指定した銘柄の信用新規可能額を取得します。

        Args:
            symbol (str): 銘柄コード。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - MarginAccountWallet (float): 信用新規可能額。
                - DepositkeepRate (float): 保証金維持率。
                - ConsignmentDepositRate (float): 委託保証金率。
                - CashOfConsignmentDepositRate (float): 現金委託保証金率。
        """
        response_json = self.call_api(f"wallet/margin/{symbol}", ApiCategory.TRADING_CAPACITY, "GET")
        return response_json

    def get_wallet_future(self) -> dict:
        """
        先物新規建玉可能額を取得します。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - FutureTradeLimit (float): 新規建玉可能額。
                - MarginRequirement (float): 買い必要証拠金額。銘柄指定の場合のみ。
                - MarginRequirementSell (float): 売り必要証拠金額。銘柄指定の場合のみ。
        """
        response_json = self.call_api("wallet/future", ApiCategory.TRADING_CAPACITY, "GET")
        return response_json

    def get_wallet_future_by_symbol(self, symbol: str) -> dict:
        """
        指定した銘柄の先物新規建玉可能額を取得します。

        Args:
            symbol (str): 銘柄コード。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - FutureTradeLimit (float): 新規建玉可能額。
                - MarginRequirement (float): 買い必要証拠金額。
                - MarginRequirementSell (float): 売り必要証拠金額。
        """
        response_json = self.call_api(f"wallet/future/{symbol}", ApiCategory.TRADING_CAPACITY, "GET")
        return response_json

    def get_wallet_option(self) -> dict:
        """
        オプション新規建玉可能額を取得します。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - OptionBuyTradeLimit (float): 買新規建玉可能額。
                - OptionSellTradeLimit (float): 売新規建玉可能額。
                - MarginRequirement (float): 必要証拠金額。銘柄指定の場合のみ。
        """
        response_json = self.call_api("wallet/option", ApiCategory.TRADING_CAPACITY, "GET")
        return response_json

    def get_wallet_option_by_symbol(self, symbol: str) -> dict:
        """
        指定した銘柄のオプション新規建玉可能額を取得します。

        Args:
            symbol (str): 銘柄コード。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - OptionBuyTradeLimit (float): 買新規建玉可能額。
                - OptionSellTradeLimit (float): 売新規建玉可能額。
                - MarginRequirement (float): 必要証拠金額。
        """
        response_json = self.call_api(f"wallet/option/{symbol}", ApiCategory.TRADING_CAPACITY, "GET")
        return response_json

    def get_board_by_symbol(self, symbol: str) -> dict:
        """
        指定した銘柄の板情報を取得します。

        Args:
            symbol (str): 銘柄コード。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - Symbol (str): 銘柄コード。
                - SymbolName (str): 銘柄名。
                - Exchange (int): 市場コード。
                - ExchangeName (str): 市場名称。
                - CurrentPrice (float): 現値。
                - CurrentPriceTime (str): 現値時刻。
                - CurrentPriceChangeStatus (str): 現値前値比較。
                - CurrentPriceStatus (int): 現値ステータス。
                - CalcPrice (float): 計算用現値。
                - PreviousClose (float): 前日終値。
                - PreviousCloseTime (str): 前日終値日付。
                - ChangePreviousClose (float): 前日比。
                - ChangePreviousClosePer (float): 騰落率。
                - OpeningPrice (float): 始値。
                - OpeningPriceTime (str): 始値時刻。
                - HighPrice (float): 高値。
                - HighPriceTime (str): 高値時刻。
                - LowPrice (float): 安値。
                - LowPriceTime (str): 安値時刻。
                - TradingVolume (float): 売買高。
                - TradingVolumeTime (str): 売買高時刻。
                - VWAP (float): 売買高加重平均価格（VWAP）。
                - TradingValue (float): 売買代金。
                - BidQty (float): 最良売気配数量。
                - BidPrice (float): 最良売気配値段。
                - BidTime (str): 最良売気配時刻。
                - BidSign (str): 最良売気配フラグ。
                - MarketOrderSellQty (float): 売成行数量。
                - Sell1 (dict): 売気配数量1本目。
                    - Time (str): 時刻。
                    - Sign (str): 気配フラグ。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell2 (dict): 売気配数量2本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell3 (dict): 売気配数量3本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell4 (dict): 売気配数量4本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell5 (dict): 売気配数量5本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell6 (dict): 売気配数量6本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell7 (dict): 売気配数量7本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell8 (dict): 売気配数量8本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell9 (dict): 売気配数量9本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Sell10 (dict): 売気配数量10本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - AskQty (float): 最良買気配数量。
                - AskPrice (float): 最良買気配値段。
                - AskTime (str): 最良買気配時刻。
                - AskSign (str): 最良買気配フラグ。
                - MarketOrderBuyQty (float): 買成行数量。
                - Buy1 (dict): 買気配数量1本目。
                    - Time (str): 時刻。
                    - Sign (str): 気配フラグ。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy2 (dict): 買気配数量2本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy3 (dict): 買気配数量3本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy4 (dict): 買気配数量4本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy5 (dict): 買気配数量5本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy6 (dict): 買気配数量6本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy7 (dict): 買気配数量7本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy8 (dict): 買気配数量8本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy9 (dict): 買気配数量9本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - Buy10 (dict): 買気配数量10本目。
                    - Price (float): 値段。
                    - Qty (float): 数量。
                - OverSellQty (float): OVER気配数量。
                - UnderBuyQty (float): UNDER気配数量。
                - TotalMarketValue (float): 時価総額。
                - ClearingPrice (float): 清算値。
                - IV (float): インプライド・ボラティリティ。
                - Gamma (float): ガンマ。
                - Theta (float): セータ。
                - Vega (float): ベガ。
                - Delta (float): デルタ。
                - SecurityType (int): 銘柄種別。
        """
        response_json = self.call_api(f"board/{symbol}", ApiCategory.INFORMATION, "GET")
        return response_json

    def get_symbol_by_symbol(self, symbol: str) -> dict:
        """
        指定した銘柄の詳細情報を取得します。

        Args:
            symbol (str): 銘柄コード。

        Returns:
            dict: リクエスト成功時のJSONデータ。
                - Symbol (str): 銘柄コード。
                - SymbolName (str): 銘柄名。
                - DisplayName (str): 銘柄略称。
                - Exchange (int): 市場コード。
                - ExchangeName (str): 市場名称。
                - BisCategory (str): 業種コード名。
                - TotalMarketValue (float): 時価総額。
                - TotalStocks (float): 発行済み株式数（千株）。
                - TradingUnit (float): 売買単位。
                - FiscalYearEndBasic (int): 決算期日。
                - PriceRangeGroup (str): 呼値グループ。
                - KCMarginBuy (bool): 一般信用買建フラグ。
                - KCMarginSell (bool): 一般信用売建フラグ。
                - MarginBuy (bool): 制度信用買建フラグ。
                - MarginSell (bool): 制度信用売建フラグ。
                - UpperLimit (float): 値幅上限。
                - LowerLimit (float): 値幅下限。
                - Underlyer (str): 原資産コード。
                - DerivMonth (str): 限月-年月。
                - TradeStart (int): 取引開始日。
                - TradeEnd (int): 取引終了日。
                - StrikePrice (float): 権利行使価格。
                - PutOrCall (int): プット/コール区分。
                - ClearingPrice (float): 清算値。
        """
        response_json = self.call_api(f"symbol/{symbol}", ApiCategory.INFORMATION, "GET")
        return response_json

    def get_orders(self) -> dict:
        """
        注文一覧を取得します。

        Returns:
            dict: リクエスト成功時のJSONデータ（OrdersSuccessオブジェクトのリスト）。
        """
        response_json = self.call_api("orders", ApiCategory.INFORMATION, "GET")
        return response_json

    def get_positions(self) -> dict:
        """
        建玉一覧を取得します。

        Returns:
            dict: リクエスト成功時のJSONデータ（PositionsSuccessオブジェクトのリスト）。
        """
        response_json = self.call_api("positions", ApiCategory.INFORMATION, "GET")
        return response_json
