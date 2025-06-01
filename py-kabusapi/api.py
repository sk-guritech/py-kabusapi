import json
import sys
from enum import IntEnum
from typing import Any, Dict, List, Literal, Optional, TypedDict, cast
from urllib.parse import urlencode

import requests
from error import OrderPlacementError, RequestCheckError


class ApiCategory(IntEnum):
    AUTHENTICATION = 0
    ORDER_PLACEMENT = 1
    TRADING_CAPACITY = 2
    INFORMATION = 3
    STOCK_REGISTRATION = 4


class HttpErrorResponse(TypedDict):
    Code: int  # エラーコード
    Message: str  # エラーメッセージ


class ApiErrorResponse(TypedDict):
    ResultCode: int  # エラーコード


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

    def token(self, api_password: str):
        """APIトークンを発行します
        ```
        発行したトークンは有効である限り使用することができ、リクエストごとに発行する必要はありません。
        発行されたAPIトークンは以下のタイミングで無効となります。
        ・kabuステーションを終了した時
        ・kabuステーションからログアウトした時
        ・別のトークンが新たに発行された時
        ※kabuステーションは早朝、強制的にログアウトいたしますのでご留意ください。
        ```

        Args:
            api_password (str): APIパスワード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    ResultCode: int  # 結果コード
                    Token: str  # APIトークン
        """

        class ApiResponse(TypedDict):
            ResultCode: int  # 結果コード
            Token: str  # APIトークン

        payload = {
            "APIPassword": api_password,
        }

        response_json = self.call_api("token", ApiCategory.AUTHENTICATION, "POST", payload)

        if "ResultCode" in response_json:
            if response_json["ResultCode"] == 0:
                self.x_api_key = response_json["Token"]
                return cast(ApiResponse, response_json)

            return cast(ApiErrorResponse, response_json)

        return cast(HttpErrorResponse, response_json)

    def sendorder(
        self,
        symbol: str,
        exchange: Literal[1, 3, 5, 6, 9, 27],
        security_type: Literal[1],
        side: Literal["1", "2"],
        cash_margin: Literal[1, 2, 3],
        deliv_type: Literal[0, 2, 3],
        account_type: Literal[2, 4, 12],
        qty: int,
        price: float,
        expire_day: int,
        front_order_type: Literal[10, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 30],
        margin_trade_type: Optional[Literal[1, 2, 3]] = None,
        margin_premium_unit: Optional[float] = None,
        fund_type: Optional[Literal["  ", "02", "AA", "11"]] = None,
        close_position_order: Optional[Literal[0, 1, 2, 3, 4, 5, 6, 7]] = None,
        close_positions: Optional[List[Dict[str, Any]]] = None,
        reverse_limit_order: Optional[Dict[str, Any]] = None,
    ):
        """
        ```
        注文を発注します。
        同一の銘柄に対しての注文は同時に5件ほどを上限としてご利用ください。
        ```

        Args:
            symbol (str): 銘柄コード
            exchange (Literal[1, 3, 5, 6, 9, 27]): 市場コード
            security_type (Literal[1]): 商品種別
            side (Literal["1", "2"]): 売買区分
            cash_margin (Literal[1, 2, 3]): 信用区分
            deliv_type (Literal[0, 2, 3]): 受渡区分
            account_type (Literal[2, 4, 12]): 口座種別
            qty (int): 注文数量
            price (float): 注文価格
            expire_day (int): 注文有効期限
            front_order_type (Literal[10, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 30]): 執行条件
            margin_trade_type (Optional[Literal[1, 2, 3]], optional): 信用取引区分
            margin_premium_unit (Optional[float], optional): １株あたりのプレミアム料(円)
            fund_type (Optional[Literal["  ", "02", "AA", "11"]], optional): 資産区分（預り区分）
            close_position_order (Optional[Literal[0, 1, 2, 3, 4, 5, 6, 7]], optional): 決済順序
            close_positions (Optional[List[Dict[str, any]]], optional): 返済建玉指定のリスト
            reverse_limit_order (Optional[Dict[str, any]]], optional): 逆指値条件

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Result: int  # 結果コード
                    OrderId: str  # 受付注文番号
        """

        class ApiResponse(TypedDict):
            Result: int  # 結果コード
            OrderId: str  # 受付注文番号

        payload = {
            "Symbol": symbol,
            "Exchange": exchange,
            "SecurityType": security_type,
            "Side": side,
            "CashMargin": cash_margin,
            "DelivType": deliv_type,
            "AccountType": account_type,
            "Qty": qty,
            "Price": price,
            "ExpireDay": expire_day,
            "FrontOrderType": front_order_type,
        }

        if margin_trade_type is not None:
            payload["MarginTradeType"] = margin_trade_type
        if margin_premium_unit is not None:
            payload["MarginPremiumUnit"] = margin_premium_unit
        if fund_type is not None:
            payload["FundType"] = fund_type
        if close_position_order is not None:
            payload["ClosePositionOrder"] = close_position_order
        if close_positions is not None:
            payload["ClosePositions"] = close_positions
        if reverse_limit_order is not None:
            payload["ReverseLimitOrder"] = reverse_limit_order

        response_json = self.call_api("sendorder", ApiCategory.ORDER_PLACEMENT, "POST", payload)

        if "Result" in response_json:
            if response_json["Result"] == 0:
                return cast(ApiResponse, response_json)

            return cast(ApiErrorResponse, response_json)

        else:
            return cast(HttpErrorResponse, response_json)

    def sendorder_future(
        self,
        symbol: str,
        exchange: int,
        trade_type: int,
        time_in_force: int,
        side: str,
        qty: int,
        price: float,
        expire_day: int,
        front_order_type: int,
        close_position_order: Optional[int] = None,
        close_positions: Optional[List[Dict[str, Any]]] = None,
        reverse_limit_order: Optional[Dict[str, Any]] = None,
    ):
        """
        ```
        先物銘柄の注文を発注します。
        同一の銘柄に対しての注文は同時に5件ほどを上限としてご利用ください。
        ```

        Args:
            symbol (str): 銘柄コード
            exchange (int): 市場コード
            trade_type (int): 取引区分
            time_in_force (int): 有効期間条件
            side (str): 売買区分
            qty (int): 注文数量
            price (float): 注文価格
            expire_day (int): 注文有効期限 (yyyyMMdd形式)
            front_order_type (int): 執行条件
            close_position_order (int, optional): 決済順序
            close_positions (list, optional): 返済建玉指定
            reverse_limit_order (dict, optional): 逆指値条件
        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Result: int  # 結果コード
                    OrderId: str  # 受付注文番号
        """

        class ApiResponse(TypedDict):
            Result: int  # 結果コード
            OrderId: str  # 受付注文番号

        payload = {
            "Symbol": symbol,
            "Exchange": exchange,
            "TradeType": trade_type,
            "TimeInForce": time_in_force,
            "Side": side,
            "Qty": qty,
            "Price": price,
            "ExpireDay": expire_day,
            "FrontOrderType": front_order_type,
        }

        if close_position_order is not None:
            payload["ClosePositionOrder"] = close_position_order
        if close_positions is not None:
            payload["ClosePositions"] = close_positions
        if reverse_limit_order is not None:
            payload["ReverseLimitOrder"] = reverse_limit_order

        response_json = self.call_api("sendorder/future", ApiCategory.ORDER_PLACEMENT, "POST", payload)

        if "Result" in response_json:
            if response_json["Result"] == 0:
                return cast(ApiResponse, response_json)

            return cast(ApiErrorResponse, response_json)

        else:
            return cast(HttpErrorResponse, response_json)

    def sendorder_option(
        self,
        symbol: str,
        exchange: int,
        trade_type: int,
        time_in_force: int,
        side: str,
        qty: int,
        price: float,
        expire_day: int,
        front_order_type: int,
        close_position_order: Optional[int] = None,
        close_positions: Optional[List[Dict[str, Any]]] = None,
        reverse_limit_order: Optional[Dict[str, Any]] = None,
    ):
        """
        ```
        オプション銘柄の注文を発注します。
        同一の銘柄に対しての注文は同時に5件ほどを上限としてご利用ください。
        ```

        Args:
            symbol (str): 銘柄コード
            exchange (int): 市場コード
            trade_type (int): 取引区分
            time_in_force (int): 有効期間条件
            side (str): 売買区分
            qty (int): 注文数量
            price (float): 注文価格
            expire_day (int): 注文有効期限 (yyyyMMdd形式)
            front_order_type (int): 執行条件
            close_position_order (int, optional): 決済順序
            close_positions (list, optional): 返済建玉指定
            reverse_limit_order (dict, optional): 逆指値条件

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Result: int  # 結果コード
                    OrderId: str  # 受付注文番号
        """

        class ApiResponse(TypedDict):
            Result: int  # 結果コード
            OrderId: str  # 受付注文番号

        payload = {
            "Symbol": symbol,
            "Exchange": exchange,
            "TradeType": trade_type,
            "TimeInForce": time_in_force,
            "Side": side,
            "Qty": qty,
            "Price": price,
            "ExpireDay": expire_day,
            "FrontOrderType": front_order_type,
        }

        if close_position_order is not None:
            payload["ClosePositionOrder"] = close_position_order
        if close_positions is not None:
            payload["ClosePositions"] = close_positions
        if reverse_limit_order is not None:
            payload["ReverseLimitOrder"] = reverse_limit_order

        response_json = self.call_api("sendorder/option", ApiCategory.ORDER_PLACEMENT, "POST", payload)

        if "Result" in response_json:
            if response_json["Result"] == 0:
                return cast(ApiResponse, response_json)

            return cast(ApiErrorResponse, response_json)

        else:
            return cast(HttpErrorResponse, response_json)

    def cancelorder(self, order_id: str):
        """
        注文を取消します

        Args:
            order_id (str): 注文番号

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Result: int  # 結果コード
                    OrderId: str  # 受付注文番号
        """

        class ApiResponse(TypedDict):
            Result: int  # 結果コード
            OrderId: str  # 受付注文番号

        payload = {"OrderId": order_id}
        response_json = self.call_api("cancelorder", ApiCategory.ORDER_PLACEMENT, "PUT", payload)

        if "Result" in response_json:
            if response_json["Result"] == 0:
                return cast(ApiResponse, response_json)

            return cast(ApiErrorResponse, response_json)

        else:
            return cast(HttpErrorResponse, response_json)

    def wallet_cash(self):
        """
        口座の取引余力（現物）を取得します

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    StockAccountWallet: float  # 現物買付可能額
                    AuKCStockAccountWallet: float  # うち、三菱UFJ eスマート証券可能額
                    AuJbnStockAccountWallet: float  # うち、auじぶん銀行残高
        """

        class ApiResponse(TypedDict):
            StockAccountWallet: float  # 現物買付可能額
            AuKCStockAccountWallet: float  # うち、三菱UFJ eスマート証券可能額
            AuJbnStockAccountWallet: float  # うち、auじぶん銀行残高

        response_json = self.call_api("wallet/cash", ApiCategory.TRADING_CAPACITY, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def wallet_cash_by_symbol(self, symbol: str):
        """
        指定した銘柄の取引余力（現物）を取得します

        Args:
            symbol (str): 銘柄コード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    StockAccountWallet: float  # 現物買付可能額
                    AuKCStockAccountWallet: float  # うち、三菱UFJ eスマート証券可能額
                    AuJbnStockAccountWallet: float  # うち、auじぶん銀行残高
        """

        class ApiResponse(TypedDict):
            StockAccountWallet: float  # 現物買付可能額
            AuKCStockAccountWallet: float  # うち、三菱UFJ eスマート証券可能額
            AuJbnStockAccountWallet: float  # うち、auじぶん銀行残高

        response_json = self.call_api(f"wallet/cash/{symbol}", ApiCategory.TRADING_CAPACITY, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def wallet_margin(self):
        """
        口座の取引余力（信用）を取得します

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    MarginAccountWallet: float  # 信用新規可能額
                    DepositkeepRate: float  # 保証金維持率
                    ConsignmentDepositRate: float  # 委託保証金率
                    CashOfConsignmentDepositRate: float  # 現金委託保証金率
        """

        class ApiResponse(TypedDict):
            MarginAccountWallet: float  # 信用新規可能額
            DepositkeepRate: float  # 保証金維持率
            ConsignmentDepositRate: float  # 委託保証金率
            CashOfConsignmentDepositRate: float  # 現金委託保証金率

        response_json = self.call_api("wallet/margin", ApiCategory.TRADING_CAPACITY, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def wallet_margin_by_symbol(self, symbol: str):
        """
        指定した銘柄の信用新規可能額を取得します。

        Args:
            symbol (str): 銘柄コード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    MarginAccountWallet: float  # 信用新規可能額
                    DepositkeepRate: float  # 保証金維持率
                    ConsignmentDepositRate: float  # 委託保証金率
                    CashOfConsignmentDepositRate: float  # 現金委託保証金率
        """

        class ApiResponse(TypedDict):
            MarginAccountWallet: float  # 信用新規可能額
            DepositkeepRate: float  # 保証金維持率
            ConsignmentDepositRate: float  # 委託保証金率
            CashOfConsignmentDepositRate: float  # 現金委託保証金率

        response_json = self.call_api(f"wallet/margin/{symbol}", ApiCategory.TRADING_CAPACITY, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def wallet_future(self):
        """
        口座の取引余力（先物）を取得します

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    FutureTradeLimit: float  # 新規建玉可能額
                    MarginRequirement: float  # 買い必要証拠金額
                    MarginRequirementSell: float  # 売り必要証拠金額
        """

        class ApiResponse(TypedDict):
            FutureTradeLimit: float  # 新規建玉可能額
            MarginRequirement: float  # 買い必要証拠金額
            MarginRequirementSell: float  # 売り必要証拠金額

        response_json = self.call_api("wallet/future", ApiCategory.TRADING_CAPACITY, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def wallet_future_by_symbol(self, symbol: str):
        """
        指定した銘柄の取引余力（先物）を取得します

        Args:
            symbol (str): 銘柄コード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    FutureTradeLimit: float  # 新規建玉可能額
                    MarginRequirement: float  # 買い必要証拠金額
                    MarginRequirementSell: float  # 売り必要証拠金額
        """

        class ApiResponse(TypedDict):
            FutureTradeLimit: float  # 新規建玉可能額
            MarginRequirement: float  # 買い必要証拠金額
            MarginRequirementSell: float  # 売り必要証拠金額

        response_json = self.call_api(f"wallet/future/{symbol}", ApiCategory.TRADING_CAPACITY, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def wallet_option(self):
        """
        口座の取引余力（オプション）を取得します

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    OptionBuyTradeLimit: float  # 買新規建玉可能額
                    OptionSellTradeLimit: float  # 売新規建玉可能額
                    MarginRequirement: float  # 必要証拠金額
        """

        class ApiResponse(TypedDict):
            OptionBuyTradeLimit: float  # 買新規建玉可能額
            OptionSellTradeLimit: float  # 売新規建玉可能額
            MarginRequirement: float  # 必要証拠金額

        response_json = self.call_api("wallet/option", ApiCategory.TRADING_CAPACITY, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def wallet_option_by_symbol(self, symbol: str):
        """
        指定した銘柄の取引余力（オプション）を取得します

        Args:
            symbol (str): 銘柄コード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    OptionBuyTradeLimit: float  # 買新規建玉可能額
                    OptionSellTradeLimit: float  # 売新規建玉可能額
                    MarginRequirement: float  # 必要証拠金額
        """

        class ApiResponse(TypedDict):
            OptionBuyTradeLimit: float  # 買新規建玉可能額
            OptionSellTradeLimit: float  # 売新規建玉可能額
            MarginRequirement: float  # 必要証拠金額

        response_json = self.call_api(f"wallet/option/{symbol}", ApiCategory.TRADING_CAPACITY, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def board_by_symbol(self, symbol: str):
        """
        ```
        指定した銘柄の時価情報・板情報を取得します
        レスポンスの一部にnullが発生した場合、該当銘柄を銘柄登録をしてから、
        再度時価情報・板情報APIを実行してください。
        ```

        Args:
            symbol (str): 銘柄コード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    class BidAskDetail(TypedDict):
                        Time: str  # 時刻
                        Sign: str  # 気配フラグ
                        Price: float # 値段
                        Qty: float   # 数量

                    Symbol: str  # 銘柄コード
                    SymbolName: str  # 銘柄名
                    Exchange: int  # 市場コード
                    ExchangeName: str  # 市場名称
                    CurrentPrice: float  # 現値
                    CurrentPriceTime: str  # 現値時刻
                    CurrentPriceChangeStatus: str  # 現値前値比較
                    CurrentPriceStatus: int  # 現値ステータス
                    CalcPrice: float  # 計算用現値
                    PreviousClose: float  # 前日終値
                    PreviousCloseTime: str  # 前日終値日付
                    ChangePreviousClose: float  # 前日比
                    ChangePreviousClosePer: float  # 騰落率
                    OpeningPrice: float  # 始値
                    OpeningPriceTime: str  # 始値時刻
                    HighPrice: float  # 高値
                    HighPriceTime: str  # 高値時刻
                    LowPrice: float  # 安値
                    LowPriceTime: str  # 安値時刻
                    TradingVolume: float  # 売買高
                    TradingVolumeTime: str  # 売買高時刻
                    VWAP: float  # 売買高加重平均価格(VWAP)
                    TradingValue: float  # 売買代金
                    BidQty: float  # 最良売気配数量
                    BidPrice: float  # 最良売気配値段
                    BidTime: str  # 最良売気配時刻
                    BidSign: str  # 最良売気配フラグ
                    MarketOrderSellQty: float  # 売成行数量
                    Sell1: BidAskDetail  # 売気配数量1本目
                    Sell2: BidAskDetail  # 売気配数量2本目
                    Sell3: BidAskDetail  # 売気配数量3本目
                    Sell4: BidAskDetail  # 売気配数量4本目
                    Sell5: BidAskDetail  # 売気配数量5本目
                    Sell6: BidAskDetail  # 売気配数量6本目
                    Sell7: BidAskDetail  # 売気配数量7本目
                    Sell8: BidAskDetail  # 売気配数量8本目
                    Sell9: BidAskDetail  # 売気配数量9本目
                    Sell10: BidAskDetail # 売気配数量10本目
                    AskQty: float  # 最良買気配数量
                    AskPrice: float  # 最良買気配値段
                    AskTime: str  # 最良買気配時刻
                    AskSign: str  # 最良買気配フラグ
                    MarketOrderBuyQty: float  # 買成行数量
                    Buy1: BidAskDetail   # 買気配数量1本目
                    Buy2: BidAskDetail   # 買気配数量2本目
                    Buy3: BidAskDetail   # 買気配数量3本目
                    Buy4: BidAskDetail   # 買気配数量4本目
                    Buy5: BidAskDetail   # 買気配数量5本目
                    Buy6: BidAskDetail   # 買気配数量6本目
                    Buy7: BidAskDetail   # 買気配数量7本目
                    Buy8: BidAskDetail   # 買気配数量8本目
                    Buy9: BidAskDetail   # 買気配数量9本目
                    Buy10: BidAskDetail  # 買気配数量10本目
                    OverSellQty: float  # OVER気配数量
                    UnderBuyQty: float  # UNDER気配数量
                    TotalMarketValue: float  # 時価総額
                    ClearingPrice: float  # 清算値
                    IV: float  # インプライド・ボラティリティ
                    Gamma: float  # ガンマ
                    Theta: float  # セータ
                    Vega: float  # ベガ
                    Delta: float  # デルタ
                    SecurityType: int  # 銘柄種別
        """

        class ApiResponse(TypedDict):
            class BidAskDetail(TypedDict):  # type: ignore
                Time: str  # 時刻
                Sign: str  # 気配フラグ
                Price: float  # 値段
                Qty: float  # 数量

            Symbol: str  # 銘柄コード
            SymbolName: str  # 銘柄名
            Exchange: int  # 市場コード
            ExchangeName: str  # 市場名称
            CurrentPrice: float  # 現値
            CurrentPriceTime: str  # 現値時刻
            CurrentPriceChangeStatus: str  # 現値前値比較
            CurrentPriceStatus: int  # 現値ステータス
            CalcPrice: float  # 計算用現値
            PreviousClose: float  # 前日終値
            PreviousCloseTime: str  # 前日終値日付
            ChangePreviousClose: float  # 前日比
            ChangePreviousClosePer: float  # 騰落率
            OpeningPrice: float  # 始値
            OpeningPriceTime: str  # 始値時刻
            HighPrice: float  # 高値
            HighPriceTime: str  # 高値時刻
            LowPrice: float  # 安値
            LowPriceTime: str  # 安値時刻
            TradingVolume: float  # 売買高
            TradingVolumeTime: str  # 売買高時刻
            VWAP: float  # 売買高加重平均価格(VWAP)
            TradingValue: float  # 売買代金
            BidQty: float  # 最良売気配数量
            BidPrice: float  # 最良売気配値段
            BidTime: str  # 最良売気配時刻
            BidSign: str  # 最良売気配フラグ
            MarketOrderSellQty: float  # 売成行数量
            Sell1: BidAskDetail  # 売気配数量1本目
            Sell2: BidAskDetail  # 売気配数量2本目
            Sell3: BidAskDetail  # 売気配数量3本目
            Sell4: BidAskDetail  # 売気配数量4本目
            Sell5: BidAskDetail  # 売気配数量5本目
            Sell6: BidAskDetail  # 売気配数量6本目
            Sell7: BidAskDetail  # 売気配数量7本目
            Sell8: BidAskDetail  # 売気配数量8本目
            Sell9: BidAskDetail  # 売気配数量9本目
            Sell10: BidAskDetail  # 売気配数量10本目
            AskQty: float  # 最良買気配数量
            AskPrice: float  # 最良買気配値段
            AskTime: str  # 最良買気配時刻
            AskSign: str  # 最良買気配フラグ
            MarketOrderBuyQty: float  # 買成行数量
            Buy1: BidAskDetail  # 買気配数量1本目
            Buy2: BidAskDetail  # 買気配数量2本目
            Buy3: BidAskDetail  # 買気配数量3本目
            Buy4: BidAskDetail  # 買気配数量4本目
            Buy5: BidAskDetail  # 買気配数量5本目
            Buy6: BidAskDetail  # 買気配数量6本目
            Buy7: BidAskDetail  # 買気配数量7本目
            Buy8: BidAskDetail  # 買気配数量8本目
            Buy9: BidAskDetail  # 買気配数量9本目
            Buy10: BidAskDetail  # 買気配数量10本目
            OverSellQty: float  # OVER気配数量
            UnderBuyQty: float  # UNDER気配数量
            TotalMarketValue: float  # 時価総額
            ClearingPrice: float  # 清算値
            IV: float  # インプライド・ボラティリティ
            Gamma: float  # ガンマ
            Theta: float  # セータ
            Vega: float  # ベガ
            Delta: float  # デルタ
            SecurityType: int  # 銘柄種別

        response_json = self.call_api(f"board/{symbol}", ApiCategory.INFORMATION, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def symbol_by_symbol(self, symbol: str, addinfo: bool = True):
        """
        指定した銘柄の詳細情報を取得します

        Args:
            symbol (str): 銘柄コード
            addinfo (bool): 追加情報出力フラグ

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Symbol: str  # 銘柄コード
                    SymbolName: str  # 銘柄名
                    DisplayName: str  # 銘柄略称
                    Exchange: int  # 市場コード
                    ExchangeName: str  # 市場名称
                    BisCategory: str  # 業種コード名
                    TotalMarketValue: float  # 時価総額
                    TotalStocks: float  # 発行済み株式数（千株）
                    TradingUnit: float  # 売買単位
                    FiscalYearEndBasic: int  # 決算期日
                    PriceRangeGroup: str  # 呼値グループ
                    KCMarginBuy: bool  # 一般信用買建フラグ
                    KCMarginSell: bool  # 一般信用売建フラグ
                    MarginBuy: bool  # 制度信用買建フラグ
                    MarginSell: bool  # 制度信用売建フラグ
                    UpperLimit: float  # 値幅上限
                    LowerLimit: float  # 値幅下限
                    Underlyer: str  # 原資産コード
                    DerivMonth: str  # 限月-年月
                    TradeStart: int  # 取引開始日
                    TradeEnd: int  # 取引終了日
                    StrikePrice: float  # 権利行使価格
                    PutOrCall: int  # プット/コール区分
                    ClearingPrice: float  # 清算値
        """

        class ApiResponse(TypedDict):
            Symbol: str  # 銘柄コード
            SymbolName: str  # 銘柄名
            DisplayName: str  # 銘柄略称
            Exchange: int  # 市場コード
            ExchangeName: str  # 市場名称
            BisCategory: str  # 業種コード名
            TotalMarketValue: float  # 時価総額
            TotalStocks: float  # 発行済み株式数（千株）
            TradingUnit: float  # 売買単位
            FiscalYearEndBasic: int  # 決算期日
            PriceRangeGroup: str  # 呼値グループ
            KCMarginBuy: bool  # 一般信用買建フラグ
            KCMarginSell: bool  # 一般信用売建フラグ
            MarginBuy: bool  # 制度信用買建フラグ
            MarginSell: bool  # 制度信用売建フラグ
            UpperLimit: float  # 値幅上限
            LowerLimit: float  # 値幅下限
            Underlyer: str  # 原資産コード
            DerivMonth: str  # 限月-年月
            TradeStart: int  # 取引開始日
            TradeEnd: int  # 取引終了日
            StrikePrice: float  # 権利行使価格
            PutOrCall: int  # プット/コール区分
            ClearingPrice: float  # 清算値

        response_json = self.call_api(
            f"symbol/{symbol}?addinfo={'true' if addinfo else 'false'}", ApiCategory.INFORMATION, "GET"
        )

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def orders(
        self,
        product: Literal["0", "1", "2", "3", "4"] | None = None,
        id: str | None = None,
        updtime: str | None = None,
        details: Literal["true", "false"] | None = None,
        symbol: str | None = None,
        state: Literal["1", "2", "3", "4", "5"] | None = None,
        side: Literal["1", "2"] | None = None,
        cashmargin: Literal["2", "3"] | None = None,
    ):
        """
        注文一覧を取得します。

        Args:
            product: 取得する商品
            id: 注文番号
            updtime: 更新日時(yyyyMMddHHmmss)
            details: 注文詳細抑止
            symbol: 銘柄コード
            state: 状態 (1〜5)
            side: 売買区分 (1: 売, 2: 買)
            cashmargin: 取引区分 (2: 新規, 3: 返済)

        Returns:
            list:
                class Order(TypedDict):
                    class OrderDetail(TypedDict):
                        SeqNum: int
                        Id: str  # 注文詳細番号
                        RecType: int  # 明細種別
                        ExchangeID: str  # 取引所番号
                        State: int  # 状態
                        TransactTime: str  # 処理時刻
                        OrdType: int  # 執行条件
                        Price: float  # 値段
                        Qty: float  # 数量
                        ExecutionID: str  # 約定番号
                        ExecutionDay: str  # 約定日時
                        DelivDay: int  # 受渡日
                        Commission: float  # 手数料
                        CommissionTax: float  # 手数料消費税

                    Id: str  # 注文番号
                    State: str  # 状態
                    OrderState: str  # 注文状態
                    OrdType: int  # 執行条件
                    RecvTime: str  # 受注日時
                    Symbol: str  # 銘柄コード
                    SymbolName: str  # 銘柄名
                    Exchange: int  # 市場コード
                    ExchangeName: str  # 市場名
                    TimeInForce: int  # 有効期間条件
                    Price: float  # 値段
                    OrderQty: float  # 発注数量
                    CumQty: float  # 約定数量
                    Side: str  # 売買区分
                    CashMargin: int  # 取引区分
                    AccountType: int  # 口座種別
                    DelivType: int  # 受渡区分
                    ExpireDay: int  # 有効期限 (yyyyMMdd形式)
                    MarginTradeType: int  # 信用取引区分
                    MarginPremium: float  # プレミアム料
                    Details: list[OrderDetail]  # 注文詳細
        """

        class Order(TypedDict):
            class OrderDetail(TypedDict):  # type: ignore
                SeqNum: int
                Id: str  # 注文詳細番号
                RecType: int  # 明細種別
                ExchangeID: str  # 取引所番号
                State: int  # 状態
                TransactTime: str  # 処理時刻
                OrdType: int  # 執行条件
                Price: float  # 値段
                Qty: float  # 数量
                ExecutionID: str  # 約定番号
                ExecutionDay: str  # 約定日時
                DelivDay: int  # 受渡日
                Commission: float  # 手数料
                CommissionTax: float  # 手数料消費税

            Id: str  # 注文番号
            State: str  # 状態
            OrderState: str  # 注文状態
            OrdType: int  # 執行条件
            RecvTime: str  # 受注日時
            Symbol: str  # 銘柄コード
            SymbolName: str  # 銘柄名
            Exchange: int  # 市場コード
            ExchangeName: str  # 市場名
            TimeInForce: int  # 有効期間条件
            Price: float  # 値段
            OrderQty: float  # 発注数量
            CumQty: float  # 約定数量
            Side: str  # 売買区分
            CashMargin: int  # 取引区分
            AccountType: int  # 口座種別
            DelivType: int  # 受渡区分
            ExpireDay: int  # 有効期限 (yyyyMMdd形式)
            MarginTradeType: int  # 信用取引区分
            MarginPremium: float  # プレミアム料
            Details: list[OrderDetail]  # 注文詳細

        raw_params = {
            "product": product,
            "id": id,
            "updtime": updtime,
            "details": details,
            "symbol": symbol,
            "state": state,
            "side": side,
            "cashmargin": cashmargin,
        }

        params = {k: v for k, v in raw_params.items() if v is not None}
        query_string = urlencode(params)
        endpoint = "orders"
        if query_string:
            endpoint += f"?{query_string}"

        response_json = self.call_api(endpoint, ApiCategory.INFORMATION, method="GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(list[Order], response_json)

    def positions(
        self,
        product: Literal["0", "1", "2", "3", "4"] | None = None,
        symbol: str | None = None,
        side: Literal["1", "2"] | None = None,
        addinfo: Literal["true", "false"] | None = None,
    ):
        """
        残高一覧を取得します。

        Args:
            product: 取得する商品 (0: すべて, 1: 現物, 2: 信用, 3: 先物, 4: OP)
            symbol: 銘柄コード
            side: 売買区分 (1: 売, 2: 買)
            addinfo: 追加情報出力フラグ ("true" または "false")

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    ExecutionID: str  # 約定番号
                    AccountType: int  # 口座種別
                    Symbol: str  # 銘柄コード
                    SymbolName: str  # 銘柄名
                    Exchange: int  # 市場コード
                    ExchangeName: str  # 市場名
                    SecurityType: int  # 銘柄種別
                    ExecutionDay: str  # 約定日（建玉日）
                    Price: float  # 値段
                    LeavesQty: float  # 残数量（保有数量）
                    HoldQty: float  # 拘束数量（返済のために拘束されている数量）
                    Side: str  # 売買区分
                    Expenses: float  # 諸経費
                    Commission: float  # 手数料
                    CommissionTax: float  # 手数料消費税
                    ExpireDay: int  # 返済期日
                    MarginTradeType: int  # 信用取引区分
                    CurrentPrice: float  # 現在値
                    Valuation: float  # 評価金額
                    ProfitLoss: float  # 評価損益額
                    ProfitLossRate: float  # 評価損益率
        """

        class ApiResponse(TypedDict):
            ExecutionID: str  # 約定番号
            AccountType: int  # 口座種別
            Symbol: str  # 銘柄コード
            SymbolName: str  # 銘柄名
            Exchange: int  # 市場コード
            ExchangeName: str  # 市場名
            SecurityType: int  # 銘柄種別
            ExecutionDay: str  # 約定日（建玉日）
            Price: float  # 値段
            LeavesQty: float  # 残数量（保有数量）
            HoldQty: float  # 拘束数量（返済のために拘束されている数量）
            Side: str  # 売買区分
            Expenses: float  # 諸経費
            Commission: float  # 手数料
            CommissionTax: float  # 手数料消費税
            ExpireDay: int  # 返済期日
            MarginTradeType: int  # 信用取引区分
            CurrentPrice: float  # 現在値
            Valuation: float  # 評価金額
            ProfitLoss: float  # 評価損益額
            ProfitLossRate: float  # 評価損益率

        raw_params = {"product": product, "symbol": symbol, "side": side, "addinfo": addinfo}

        params = {k: v for k, v in raw_params.items() if v is not None}
        query_string = urlencode(params)
        endpoint = "positions"
        if query_string:
            endpoint += f"?{query_string}"

        response_json = self.call_api(endpoint, ApiCategory.INFORMATION, method="GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def symbolname_future(self, future_code: str | None = None, deriv_month: int = 0):
        """
        先物銘柄コード取得

        Args:
            future_code: 先物コード
            deriv_month: 限月

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Symbol: str  # 銘柄コード
                    SymbolName: str  # 銘柄名称
        """

        class ApiResponse(TypedDict):
            Symbol: str  # 銘柄コード
            SymbolName: str  # 銘柄名称

        raw_params = {"FutureCode": future_code, "DerivMonth": deriv_month}

        # None を除外してクエリストリング生成
        params = {k: v for k, v in raw_params.items() if v is not None}
        query_string = urlencode(params)
        endpoint = "symbolname/future"
        if query_string:
            endpoint += f"?{query_string}"

        response_json = self.call_api(endpoint, ApiCategory.INFORMATION, method="GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def symbolname_option(
        self,
        deriv_month: int,
        put_or_call: Literal["P", "C"],
        strike_price: int,
        option_code: str | None = None,
    ):
        """
        オプション銘柄コード取得

        Args:
            deriv_month: 限月
            put_or_call: プット or コール
            strike_price: 権利行使価格
            option_code: オプションコード

        Returns:
            dict: リクエスト成功時のJSONデータ。
                class ApiResponse(TypedDict):
                    Symbol: str  # 銘柄コード
                    SymbolName: str  # 銘柄名称
        """

        class ApiResponse(TypedDict):
            Symbol: str  # 銘柄コード
            SymbolName: str  # 銘柄名称

        raw_params = {
            "DerivMonth": deriv_month,
            "PutOrCall": put_or_call,
            "StrikePrice": strike_price,
            "OptionCode": option_code,
        }

        # None を除いたパラメータのみ送信
        params = {k: v for k, v in raw_params.items() if v is not None}
        query_string = urlencode(params)
        endpoint = "symbolname/option"
        if query_string:
            endpoint += f"?{query_string}"

        response_json = self.call_api(endpoint, ApiCategory.INFORMATION, method="GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def symbolname_minioptionweekly(
        self,
        deriv_month: int,
        deriv_weekly: int,
        put_or_call: Literal["P", "C"],
        strike_price: int,
    ):
        """
        ミニオプション（限週）銘柄コード取得

        Args:
            deriv_month: 限月
            deriv_weekly: 限週
            put_or_call: コール or プット
            strike_price: 権利行使価格

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Symbol: str  # 銘柄コード
                    SymbolName: str  # 銘柄名称
        """

        class ApiResponse(TypedDict):
            Symbol: str  # 銘柄コード
            SymbolName: str  # 銘柄名称

        params = {
            "DerivMonth": deriv_month,
            "DerivWeekly": deriv_weekly,
            "PutOrCall": put_or_call,
            "StrikePrice": strike_price,
        }

        query_string = urlencode(params)
        endpoint = f"symbolname/minioptionweekly?{query_string}"

        response_json = self.call_api(endpoint, ApiCategory.INFORMATION, method="GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def ranking(
        self,
        type: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
        exchange_division: Literal["ALL", "T", "TP", "TS", "TG", "M", "FK", "S"],
    ):
        """
        ```
        詳細ランキング画面と同様の各種ランキングを返します。
        ランキングの対象日はkabuステーションが保持している当日のデータとなります。
        ※株価情報ランキング、業種別指数ランキングは、下記の時間帯でデータがクリアされるため、
        その間の詳細ランキングAPIは空レスポンスとなります。
        データクリア: 平日7:53頃-9:00過ぎ頃
        ※信用情報ランキングは毎週第3営業日の7:55頃にデータが更新されます。
        ```

        Args:
            type: ランキング種別
            exchange_division: 市場

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    class RankTypeFor1_4(TypedDict):
                        No: Optional[int] # 順位
                        Trend: Literal["0", "1", "2", "3", "4", "5"] # トレンド
                        AverageRanking: float
                        Symbol: str  # 銘柄コード
                        SymbolName: str  # 銘柄名称
                        CurrentPrice: float  # 現在値
                        ChangeRatio: float  # 前日比
                        ChangePercentage: float  # 騰落率(%)
                        CurrentPriceTime: str  # 時刻 HH:mm
                        TradingVolume: float  # 売買高 (千株単位、百株の位を四捨五入)
                        Turnover: float  # 売買代金 (百万円単位、十万円の位を四捨五入)
                        ExchangeName: str  # 市場名
                        CategoryName: str  # 業種名

                    class RankTypeFor5(TypedDict):
                        No: Optional[int] # 順位
                        Trend: Literal["0", "1", "2", "3", "4", "5"] # トレンド
                        AverageRanking: float  # 平均順位
                        Symbol: str  # 銘柄コード
                        SymbolName: str  # 銘柄名称
                        CurrentPrice: float  # 現在値
                        ChangeRatio: float  # 前日比
                        TickCount: int # TICK回数
                        UpCount: int # UP
                        DownCount: int # DOWN
                        ChangePercentage: float  # 騰落率(%)
                        TradingVolume: float  # 売買高 (千株単位で表示、百株の位を四捨五入)
                        Turnover: float  # 売買代金 (百万円単位で表示、十万円の位を四捨五入)
                        ExchangeName: str  # 市場名
                        CategoryName: str  # 業種名

                    class RankTypeFor6(TypedDict):
                        No: Optional[int] # 順位
                        Trend: Literal["0", "1", "2", "3", "4", "5"] # トレンド
                        AverageRanking: float  # 平均順位
                        Symbol: str  # 銘柄コード
                        SymbolName: str  # 銘柄名称
                        CurrentPrice: float  # 現在値
                        ChangeRatio: float  # 前日比
                        RapidTradePercentage: float  # 売買高急増(%)
                        TradingVolume: float  # 売買高 (千株単位で表示、百株の位を四捨五入)
                        CurrentPriceTime: str  # 時刻 HH:mm
                        ChangePercentage: float  # 騰落率(%)
                        ExchangeName: str  # 市場名
                        CategoryName: str  # 業種名

                    class RankTypeFor7(TypedDict):
                        No: Optional[int] # 順位
                        Trend: Literal["0", "1", "2", "3", "4", "5"] # トレンド
                        AverageRanking: float  # 平均順位
                        Symbol: str  # 銘柄コード
                        SymbolName: str  # 銘柄名称
                        CurrentPrice: float  # 現在値
                        ChangeRatio: float  # 前日比
                        RapidPaymentPercentage: float  # 代金急増(%)
                        Turnover: float  # 売買代金: 百万円単位で表示され、十万円の位を四捨五入します。
                        CurrentPriceTime: str  # 時刻: HH:mm
                        ChangePercentage: float  # 騰落率(%)
                        ExchangeName: str  # 市場名
                        CategoryName: str  # 業種名

                    class RankTypeFor8_13(TypedDict):
                        No: Optional[int] # 順位
                        Symbol: str  # 銘柄コード
                        SymbolName: str  # 銘柄名称
                        SellRapidPaymentPercentage: float  # 売残（千株）
                        SellLastWeekRatio: float  # 売残前週比
                        BuyRapidPaymentPercentage: float  # 買残（千株）
                        BuyLastWeekRatio: float  # 買残前週比
                        Ratio: float  # 倍率
                        ExchangeName: str  # 市場名
                        CategoryName: str  # 業種名

                    class RankTypeFor14_15(TypedDict):
                        No: Optional[int] # 順位
                        Trend: Literal["0", "1", "2", "3", "4", "5"] # トレンド
                        AverageRanking: float  # 平均順位
                        Category: str  # 業種コード
                        CategoryName: str  # 業種名
                        CurrentPrice: float  # 現在値
                        ChangeRatio: float  # 前日比
                        CurrentPriceTime: str  # 時刻: HH:mm
                        ChangePercentage: float  # 騰落率(%)

                    Type: str  # 種別
                    ExchangeDivision: str  # 市場
                    Ranking: list[RankTypeFor1To4] | list[RankTypeFor5] | list[RankTypeFor6] | list[RankTypeFor7] | list[RankTypeFor8To13] | list[RankTypeFor14To15]  # ランキングデータ
        """

        class ApiResponse(TypedDict):
            class RankTypeFor1To4(TypedDict):  # type: ignore
                No: Optional[int]  # 順位
                Trend: Literal["0", "1", "2", "3", "4", "5"]  # トレンド
                AverageRanking: float
                Symbol: str  # 銘柄コード
                SymbolName: str  # 銘柄名称
                CurrentPrice: float  # 現在値
                ChangeRatio: float  # 前日比
                ChangePercentage: float  # 騰落率(%)
                CurrentPriceTime: str  # 時刻 HH:mm
                TradingVolume: float  # 売買高 (千株単位、百株の位を四捨五入)
                Turnover: float  # 売買代金 (百万円単位、十万円の位を四捨五入)
                ExchangeName: str  # 市場名
                CategoryName: str  # 業種名

            class RankTypeFor5(TypedDict):  # type: ignore
                No: Optional[int]  # 順位
                Trend: Literal["0", "1", "2", "3", "4", "5"]  # トレンド
                AverageRanking: float  # 平均順位
                Symbol: str  # 銘柄コード
                SymbolName: str  # 銘柄名称
                CurrentPrice: float  # 現在値
                ChangeRatio: float  # 前日比
                TickCount: int  # TICK回数
                UpCount: int  # UP
                DownCount: int  # DOWN
                ChangePercentage: float  # 騰落率(%)
                TradingVolume: float  # 売買高 (千株単位で表示、百株の位を四捨五入)
                Turnover: float  # 売買代金 (百万円単位で表示、十万円の位を四捨五入)
                ExchangeName: str  # 市場名
                CategoryName: str  # 業種名

            class RankTypeFor6(TypedDict):  # type: ignore
                No: Optional[int]  # 順位
                Trend: Literal["0", "1", "2", "3", "4", "5"]  # トレンド
                AverageRanking: float  # 平均順位
                Symbol: str  # 銘柄コード
                SymbolName: str  # 銘柄名称
                CurrentPrice: float  # 現在値
                ChangeRatio: float  # 前日比
                RapidTradePercentage: float  # 売買高急増(%)
                TradingVolume: float  # 売買高 (千株単位で表示、百株の位を四捨五入)
                CurrentPriceTime: str  # 時刻 HH:mm
                ChangePercentage: float  # 騰落率(%)
                ExchangeName: str  # 市場名
                CategoryName: str  # 業種名

            class RankTypeFor7(TypedDict):  # type: ignore
                No: Optional[int]  # 順位
                Trend: Literal["0", "1", "2", "3", "4", "5"]  # トレンド
                AverageRanking: float  # 平均順位
                Symbol: str  # 銘柄コード
                SymbolName: str  # 銘柄名称
                CurrentPrice: float  # 現在値
                ChangeRatio: float  # 前日比
                RapidPaymentPercentage: float  # 代金急増(%)
                Turnover: float  # 売買代金: 百万円単位で表示され、十万円の位を四捨五入します。
                CurrentPriceTime: str  # 時刻: HH:mm
                ChangePercentage: float  # 騰落率(%)
                ExchangeName: str  # 市場名
                CategoryName: str  # 業種名

            class RankTypeFor8To13(TypedDict):  # type: ignore
                No: Optional[int]  # 順位
                Symbol: str  # 銘柄コード
                SymbolName: str  # 銘柄名称
                SellRapidPaymentPercentage: float  # 売残（千株）
                SellLastWeekRatio: float  # 売残前週比
                BuyRapidPaymentPercentage: float  # 買残（千株）
                BuyLastWeekRatio: float  # 買残前週比
                Ratio: float  # 倍率
                ExchangeName: str  # 市場名
                CategoryName: str  # 業種名

            class RankTypeFor14To15(TypedDict):  # type: ignore
                No: Optional[int]  # 順位
                Trend: Literal["0", "1", "2", "3", "4", "5"]  # トレンド
                AverageRanking: float  # 平均順位
                Category: str  # 業種コード
                CategoryName: str  # 業種名
                CurrentPrice: float  # 現在値
                ChangeRatio: float  # 前日比
                CurrentPriceTime: str  # 時刻: HH:mm
                ChangePercentage: float  # 騰落率(%)

            Type: str  # 種別
            ExchangeDivision: str  # 市場
            Ranking: (
                list[RankTypeFor1To4]
                | list[RankTypeFor5]
                | list[RankTypeFor6]
                | list[RankTypeFor7]
                | list[RankTypeFor8To13]
                | list[RankTypeFor14To15]
            )  # ランキングデータ

        params = {"Type": type, "ExchangeDivision": exchange_division}

        query_string = urlencode(params)
        endpoint = f"ranking?{query_string}"

        response_json = self.call_api(endpoint, ApiCategory.INFORMATION, method="GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def exchange_by_symbol(
        self,
        symbol: Literal[
            "usdjpy", "eurjpy", "gbpjpy", "audjpy", "chfjpy", "cadjpy", "nzdjpy", "zarjpy", "eurusd", "gbpusd", "audusd"
        ],
    ):
        """
        マネービューの情報を取得する

        Args:
            symbol (str): 通貨ペア

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Symbol: str  # 通貨
                    BidPrice: float  # BID
                    Spread: float  # SP
                    AskPrice: float  # ASK
                    Change: float  # 前日比
                    Time: str  # 時刻 (HH:mm:ss形式)
        """

        class ApiResponse(TypedDict):
            Symbol: str  # 通貨
            BidPrice: float  # BID
            Spread: float  # SP
            AskPrice: float  # ASK
            Change: float  # 前日比
            Time: str  # 時刻 (HH:mm:ss形式)

        response_json = self.call_api(f"exchange/{symbol}", ApiCategory.INFORMATION, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def regulations_by_symbol(self, symbol: str):
        """
        規制情報＋空売り規制情報を取得する

        Args:
            symbol (str): 銘柄コード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    class RegulationInfo(TypedDict):
                        Exchange: int  # 規制市場
                        Product: int  # 規制取引区分
                        Side: str  # 規制売買
                        Reason: str  # 理由
                        LimitStartDay: str  # 制限開始日 (yyyy/MM/dd HH:mm形式)
                        LimitEndDay: str  # 制限終了日 (yyyy/MM/dd HH:mm形式)
                        Level: int  # コンプライアンスレベル

                    Symbol: str  # 銘柄コード
                    RegulationsInfo: list[RegulationInfo]  # 規制情報
        """

        class ApiResponse(TypedDict):
            class RegulationInfo(TypedDict):  # type: ignore
                Exchange: int  # 規制市場
                Product: int  # 規制取引区分
                Side: str  # 規制売買
                Reason: str  # 理由
                LimitStartDay: str  # 制限開始日 (yyyy/MM/dd HH:mm形式)
                LimitEndDay: str  # 制限終了日 (yyyy/MM/dd HH:mm形式)
                Level: int  # コンプライアンスレベル

            Symbol: str  # 銘柄コード
            RegulationsInfo: list[RegulationInfo]  # 規制情報

        response_json = self.call_api(f"regulations/{symbol}", ApiCategory.INFORMATION, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def primaryexchange_by_symbol(self, symbol: str):
        """
        株式の優先市場を取得する

        Args:
            symbol (str): 銘柄コード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Symbol: str  # 銘柄コード
                    PrimaryExchange: int  # 優先市場
        """

        class ApiResponse(TypedDict):
            Symbol: str  # 銘柄コード
            PrimaryExchange: int  # 優先市場

        response_json = self.call_api(f"primaryexchange/{symbol}", ApiCategory.INFORMATION, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def apisoftlimit(self):
        """
        kabuステーションAPIのソフトリミット値を取得する

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    Stock: float  # 現物のワンショット上限 (万円)
                    Margin: float  # 信用のワンショット上限 (万円)
                    Future: float  # 先物のワンショット上限 (枚)
                    FutureMini: float  # ミニ先物のワンショット上限 (枚)
                    FutureMicro: float  # マイクロ先物のワンショット上限 (枚)
                    Option: float  # オプションのワンショット上限 (枚)
                    MiniOption: float  # ミニオプションのワンショット上限 (枚)
                    KabuSVersion: str  # kabuステーションのバージョン
        """

        class ApiResponse(TypedDict):
            Stock: float  # 現物のワンショット上限 (万円)
            Margin: float  # 信用のワンショット上限 (万円)
            Future: float  # 先物のワンショット上限 (枚)
            FutureMini: float  # ミニ先物のワンショット上限 (枚)
            FutureMicro: float  # マイクロ先物のワンショット上限 (枚)
            Option: float  # オプションのワンショット上限 (枚)
            MiniOption: float  # ミニオプションのワンショット上限 (枚)
            KabuSVersion: str  # kabuステーションのバージョン

        response_json = self.call_api("apisoftlimit", ApiCategory.INFORMATION, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)

    def margin_marginpremium_by_symbol(self, symbol: str):
        """
        指定した銘柄のプレミアム料を取得するAPI

        Args:
            symbol (str): 銘柄コード

        Returns:
            dict:
                class ApiResponse(TypedDict):
                    class GeneralMarginDetail(TypedDict):
                        MarginPremiumType: int  # プレミアム料入力区分
                        MarginPremium: float  # 確定プレミアム料
                        UpperMarginPremium: float  # 上限プレミアム料
                        LowerMarginPremium: float  # 下限プレミアム料
                        TickMarginPremium: float  # プレミアム料刻値

                    class DayTradeDetail(TypedDict):
                        MarginPremiumType: int  # プレミアム料入力区分
                        MarginPremium: float  # 確定プレミアム料
                        UpperMarginPremium: float  # 上限プレミアム料
                        LowerMarginPremium: float  # 下限プレミアム料
                        TickMarginPremium: float  # プレミアム料刻値

                    Symbol: str  # 銘柄コード
                    GeneralMargin: GeneralMarginDetail  # 一般信用(長期)
                    DayTrade: DayTradeDetail  # 一般信用(デイトレ)
        """

        class ApiResponse(TypedDict):
            class GeneralMarginDetail(TypedDict):  # type: ignore
                MarginPremiumType: int  # プレミアム料入力区分
                MarginPremium: float  # 確定プレミアム料
                UpperMarginPremium: float  # 上限プレミアム料
                LowerMarginPremium: float  # 下限プレミアム料
                TickMarginPremium: float  # プレミアム料刻値

            class DayTradeDetail(TypedDict):  # type: ignore
                MarginPremiumType: int  # プレミアム料入力区分
                MarginPremium: float  # 確定プレミアム料
                UpperMarginPremium: float  # 上限プレミアム料
                LowerMarginPremium: float  # 下限プレミアム料
                TickMarginPremium: float  # プレミアム料刻値

            Symbol: str  # 銘柄コード
            GeneralMargin: GeneralMarginDetail  # 一般信用(長期)
            DayTrade: DayTradeDetail  # 一般信用(デイトレ)

        response_json = self.call_api(f"margin/marginpremium/{symbol}", ApiCategory.INFORMATION, "GET")

        if "Code" in response_json:
            return cast(HttpErrorResponse, response_json)

        return cast(ApiResponse, response_json)
