import json
import threading
from typing import Any, Callable, Dict, List, Literal, Optional, Type, TypeVar
from urllib.parse import urlencode

import requests
import websocket as ws
from pydantic import BaseModel

from .const import ApiCategory, ApiResultCategory
from .response_model import (
    ApiErrorResponse,
    ApiResultApiError,
    ApiResultHttpError,
    ApiResultSuccess,
    ApisoftlimitApiResponse,
    BoardBySymbolApiResponse,
    CancelorderApiResponse,
    ExchangeBySymbolApiResponse,
    HttpErrorResponse,
    MarginMarginpremiumBySymbolApiResponse,
    OrdersApiResponse,
    PositionsApiResponse,
    PrimaryexchangeBySymbolApiResponse,
    RankingApiResponse,
    RegisterApiResponse,
    RegulationsBySymbolApiResponse,
    SendorderApiResponse,
    SendorderFutureApiResponse,
    SendorderOptionApiResponse,
    SymbolBySymbolApiResponse,
    SymbolnameFutureApiResponse,
    SymbolnameMinioptionweeklyApiResponse,
    SymbolnameOptionApiResponse,
    TokenApiResponse,
    UnregisterAllApiResponse,
    UnregisterApiResponse,
    WalletCashApiResponse,
    WalletCashBySymbolApiResponse,
    WalletFutureApiResponse,
    WalletFutureBySymbolApiResponse,
    WalletMarginApiResponse,
    WalletMarginBySymbolApiResponse,
    WalletOptionApiResponse,
    WalletOptionBySymbolApiResponse,
    WebSocketPushData,
)

T = TypeVar("T", bound=BaseModel)


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
        self.websocket_url = self._generate_websocket_url(host_name, environment, is_in_docker_container)
        self.ws: ws.WebSocketApp | None = None
        self.ws_thread: threading.Thread | None = None
        self.on_message_callback: Callable[[WebSocketPushData], None] | None = None
        self.on_error_callback: Callable[[Exception], None] | None = None
        self.on_connect_callback: Callable[[], None] | None = None
        self.on_disconnect_callback: Callable[[], None] | None = None

    def _generate_websocket_url(
        self, host_name: str, environment: Literal["test"] | Literal["production"], is_in_docker_container: bool
    ) -> str:
        """WebSocket接続用URLを生成"""
        if environment == "test":
            port = 18081
        else:
            port = 18080

        if is_in_docker_container:
            host_name = "host.docker.internal"

        return f"ws://{host_name}:{port}/kabusapi/websocket"

    def call_api(
        self, path: str, api_category: ApiCategory, method: str, api_response_basemodel: Type[T], payload={}
    ) -> ApiResultSuccess[T] | ApiResultHttpError | ApiResultApiError:
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
            response_json: dict | list = response.json()

        except requests.exceptions.JSONDecodeError:
            raise ValueError("Unexpected response")

        if isinstance(response_json, list) or response.status_code == 200:
            if isinstance(response_json, list):
                return ApiResultSuccess[T](content=api_response_basemodel(response_json))  # type: ignore

            if __extract_result(api_category, response_json):
                return ApiResultHttpError(content=ApiErrorResponse(**response_json))  # type: ignore

            return ApiResultSuccess[T](content=api_response_basemodel(**response_json))

        else:
            return ApiResultHttpError(content=HttpErrorResponse(Code=response.status_code, Message=response.reason))

    def __merge_payloads(self, payload: dict[str, Any], optional_payload: dict[str, Any]) -> dict[str, Any]:
        merged_payload = payload.copy()
        for key, value in optional_payload.items():
            if value is not None:
                merged_payload[key] = value

        return merged_payload

    def __build_query_string(self, params: Dict[str, Any]) -> str:
        return urlencode({k: v for k, v in params.items() if v is not None})

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
        """
        payload = {
            "APIPassword": api_password,
        }

        response = self.call_api("token", ApiCategory.AUTHENTICATION, "POST", TokenApiResponse, payload)

        if response.api_result_category == ApiResultCategory.SUCCESS:
            self.x_api_key = response.content.Token

        return response

    def sendorder(
        self,
        symbol: str,
        exchange: Literal["1", "3", "5", "6", "9", "27"],
        security_type: Literal["1"],
        side: Literal["1", "2"],
        cash_margin: Literal["1", "2", "3"],
        deliv_type: Literal["0", "2", "3"],
        account_type: Literal["2", "4", "12"],
        qty: int,
        price: float,
        expire_day: int,
        front_order_type: Literal[
            "10", "13", "14", "15", "16", "17", "20", "21", "22", "23", "24", "25", "26", "27", "30"
        ],
        margin_trade_type: Optional[Literal["1", "2", "3"]] = None,
        margin_premium_unit: Optional[float] = None,
        fund_type: Optional[Literal["  ", "02", "AA", "11"]] = None,
        close_position_order: Optional[Literal["0", "1", "2", "3", "4", "5", "6", "7"]] = None,
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
            exchange (Literal["1", "3", "5", "6", "9", "27"]): 市場コード
            security_type (Literal["1"]): 商品種別
            side (Literal["1", "2"]): 売買区分
            cash_margin (Literal["1", "2", "3"]): 信用区分
            deliv_type (Literal["0", "2", "3"]): 受渡区分
            account_type (Literal["2", "4", "12"]): 口座種別
            qty (int): 注文数量
            price (float): 注文価格
            expire_day (int): 注文有効期限
            front_order_type (Literal["10", "13", "14", "15", "16", "17", "20", "21", "22", "23", "24", "25", "26", "27", "30"]): 執行条件
            margin_trade_type (Optional[Literal["1", "2", "3"]], optional): 信用取引区分
            margin_premium_unit (Optional[float], optional): １株あたりのプレミアム料(円)
            fund_type (Optional[Literal["  ", "02", "AA", "11"]], optional): 資産区分（預り区分）
            close_position_order (Optional[Literal["0", "1", "2", "3", "4", "5", "6", "7"]], optional): 決済順序
            close_positions (Optional[List[Dict[str, any]]], optional): 返済建玉指定のリスト
            reverse_limit_order (Optional[Dict[str, any]]], optional): 逆指値条件
        """
        payload = {
            "Symbol": symbol,
            "Exchange": int(exchange),
            "SecurityType": int(security_type),
            "Side": side,
            "CashMargin": int(cash_margin),
            "DelivType": int(deliv_type),
            "AccountType": int(account_type),
            "Qty": qty,
            "Price": price,
            "ExpireDay": expire_day,
            "FrontOrderType": int(front_order_type),
        }

        optional_payload = {
            "MarginTradeType": int(margin_trade_type) if margin_trade_type is not None else None,
            "MarginPremiumUnit": margin_premium_unit,
            "FundType": fund_type,
            "ClosePositionOrder": int(close_position_order) if close_position_order is not None else None,
            "ClosePositions": close_positions,
            "ReverseLimitOrder": reverse_limit_order,
        }

        return self.call_api(
            "sendorder",
            ApiCategory.ORDER_PLACEMENT,
            "POST",
            SendorderApiResponse,
            self.__merge_payloads(payload, optional_payload),
        )

    def sendorder_future(
        self,
        symbol: str,
        exchange: Literal["2", "17", "18"],
        trade_type: Literal["1", "2"],
        time_in_force: Literal["1", "2", "3"],
        side: Literal["1", "2"],
        qty: int,
        price: float,
        expire_day: int,
        front_order_type: Literal["120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130"],
        close_position_order: Optional[Literal["0", "1", "2"]] = None,
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
            exchange (Literal["2", "17", "18"]): 市場コード
            trade_type (Literal["1", "2"]): 取引区分
            time_in_force (Literal["1", "2", "3"]): 有効期間条件
            side (Literal["1", "2"]): 売買区分
            qty (int): 注文数量
            price (float): 注文価格
            expire_day (int): 注文有効期限 (yyyyMMdd形式)
            front_order_type (Literal["120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130"]): 執行条件
            close_position_order (Literal["0", "1", "2"], optional): 決済順序
            close_positions (list, optional): 返済建玉指定
            reverse_limit_order (dict, optional): 逆指値条件
        """
        payload = {
            "Symbol": symbol,
            "Exchange": int(exchange),
            "TradeType": int(trade_type),
            "TimeInForce": int(time_in_force),
            "Side": side,
            "Qty": qty,
            "Price": price,
            "ExpireDay": expire_day,
            "FrontOrderType": int(front_order_type),
        }

        optional_payload = {
            "ClosePositionOrder": int(close_position_order) if close_position_order is not None else None,
            "ClosePositions": close_positions,
            "ReverseLimitOrder": reverse_limit_order,
        }

        return self.call_api(
            "sendorder/future",
            ApiCategory.ORDER_PLACEMENT,
            "POST",
            SendorderFutureApiResponse,
            self.__merge_payloads(payload, optional_payload),
        )

    def sendorder_option(
        self,
        symbol: str,
        exchange: Literal["2", "17", "18"],
        trade_type: Literal["1", "2"],
        time_in_force: Literal["1", "2", "3"],
        side: Literal["1", "2"],
        qty: int,
        price: float,
        expire_day: int,
        front_order_type: Literal["120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130"],
        close_position_order: Optional[Literal["0", "1", "2"]] = None,
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
            exchange (Literal["2", "17", "18"]): 市場コード
            trade_type (Literal["1", "2"]): 取引区分
            time_in_force (Literal["1", "2", "3"]): 有効期間条件
            side (Literal["1", "2"]): 売買区分
            qty (int): 注文数量
            price (float): 注文価格
            expire_day (int): 注文有効期限 (yyyyMMdd形式)
            front_order_type (Literal["120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130"]): 執行条件
            close_position_order (Literal["0", "1", "2"], optional): 決済順序
            close_positions (list, optional): 返済建玉指定
            reverse_limit_order (dict, optional): 逆指値条件
        """
        payload = {
            "Symbol": symbol,
            "Exchange": int(exchange),
            "TradeType": int(trade_type),
            "TimeInForce": int(time_in_force),
            "Side": side,
            "Qty": qty,
            "Price": price,
            "ExpireDay": expire_day,
            "FrontOrderType": int(front_order_type),
        }

        optional_payload = {
            "ClosePositionOrder": int(close_position_order) if close_position_order is not None else None,
            "ClosePositions": close_positions,
            "ReverseLimitOrder": reverse_limit_order,
        }

        return self.call_api(
            "sendorder/option",
            ApiCategory.ORDER_PLACEMENT,
            "POST",
            SendorderOptionApiResponse,
            self.__merge_payloads(payload, optional_payload),
        )

    def cancelorder(self, order_id: str):
        """
        注文を取消します

        Args:
            order_id (str): 注文番号
        """
        payload = {"OrderId": order_id}

        return self.call_api("cancelorder", ApiCategory.ORDER_PLACEMENT, "PUT", CancelorderApiResponse, payload)

    def wallet_cash(self):
        """
        口座の取引余力（現物）を取得します
        """
        return self.call_api("wallet/cash", ApiCategory.TRADING_CAPACITY, "GET", WalletCashApiResponse)

    def wallet_cash_by_symbol(self, symbol: str):
        """
        指定した銘柄の取引余力（現物）を取得します

        Args:
            symbol (str): 銘柄コード
        """
        return self.call_api(
            f"wallet/cash/{symbol}", ApiCategory.TRADING_CAPACITY, "GET", WalletCashBySymbolApiResponse
        )

    def wallet_margin(self):
        """
        口座の取引余力（信用）を取得します
        """
        return self.call_api("wallet/margin", ApiCategory.TRADING_CAPACITY, "GET", WalletMarginApiResponse)

    def wallet_margin_by_symbol(self, symbol: str):
        """
        指定した銘柄の信用新規可能額を取得します。

        Args:
            symbol (str): 銘柄コード
        """
        return self.call_api(
            f"wallet/margin/{symbol}", ApiCategory.TRADING_CAPACITY, "GET", WalletMarginBySymbolApiResponse
        )

    def wallet_future(self):
        """
        口座の取引余力（先物）を取得します
        """
        return self.call_api("wallet/future", ApiCategory.TRADING_CAPACITY, "GET", WalletFutureApiResponse)

    def wallet_future_by_symbol(self, symbol: str):
        """
        指定した銘柄の取引余力（先物）を取得します

        Args:
            symbol (str): 銘柄コード
        """
        return self.call_api(
            f"wallet/future/{symbol}", ApiCategory.TRADING_CAPACITY, "GET", WalletFutureBySymbolApiResponse
        )

    def wallet_option(self):
        """
        口座の取引余力（オプション）を取得します
        """
        return self.call_api("wallet/option", ApiCategory.TRADING_CAPACITY, "GET", WalletOptionApiResponse)

    def wallet_option_by_symbol(self, symbol: str):
        """
        指定した銘柄の取引余力（オプション）を取得します

        Args:
            symbol (str): 銘柄コード
        """
        return self.call_api(
            f"wallet/option/{symbol}", ApiCategory.TRADING_CAPACITY, "GET", WalletOptionBySymbolApiResponse
        )

    def board_by_symbol(self, symbol: str):
        """
        ```
        指定した銘柄の時価情報・板情報を取得します
        レスポンスの一部にnullが発生した場合、該当銘柄を銘柄登録をしてから、
        再度時価情報・板情報APIを実行してください。
        ```

        Args:
            symbol (str): 銘柄コード
        """
        return self.call_api(f"board/{symbol}", ApiCategory.INFORMATION, "GET", BoardBySymbolApiResponse)

    def symbol_by_symbol(self, symbol: str, addinfo: bool = True):
        """
        指定した銘柄の詳細情報を取得します

        Args:
            symbol (str): 銘柄コード
            addinfo (bool): 追加情報出力フラグ
        """
        return self.call_api(
            f"symbol/{symbol}?addinfo={'true' if addinfo else 'false'}",
            ApiCategory.INFORMATION,
            "GET",
            SymbolBySymbolApiResponse,
        )

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
        """
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

        query_string = self.__build_query_string(raw_params)

        return self.call_api(f"orders?{query_string}", ApiCategory.INFORMATION, "GET", OrdersApiResponse)

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
        """
        raw_params = {
            "product": product,
            "symbol": symbol,
            "side": side,
            "addinfo": addinfo,
        }

        query_string = self.__build_query_string(raw_params)

        return self.call_api(f"positions?{query_string}", ApiCategory.INFORMATION, "GET", PositionsApiResponse)

    def symbolname_future(self, future_code: str | None = None, deriv_month: int = 0):
        """
        先物銘柄コード取得

        Args:
            future_code: 先物コード
            deriv_month: 限月
        """
        raw_params = {
            "FutureCode": future_code,
            "DerivMonth": deriv_month,
        }

        query_string = self.__build_query_string(raw_params)

        return self.call_api(
            f"symbolname/future?{query_string}", ApiCategory.INFORMATION, "GET", SymbolnameFutureApiResponse
        )

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
        """
        raw_params = {
            "DerivMonth": deriv_month,
            "PutOrCall": put_or_call,
            "StrikePrice": strike_price,
            "OptionCode": option_code,
        }

        query_string = self.__build_query_string(raw_params)

        return self.call_api(
            f"symbolname/option?{query_string}", ApiCategory.INFORMATION, "GET", SymbolnameOptionApiResponse
        )

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
        """
        params = {
            "DerivMonth": deriv_month,
            "DerivWeekly": deriv_weekly,
            "PutOrCall": put_or_call,
            "StrikePrice": strike_price,
        }

        query_string = urlencode(params)
        endpoint = f"symbolname/minioptionweekly?{query_string}"

        return self.call_api(endpoint, ApiCategory.INFORMATION, "GET", SymbolnameMinioptionweeklyApiResponse)

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
        """
        params = {"Type": type, "ExchangeDivision": exchange_division}

        query_string = urlencode(params)
        endpoint = f"ranking?{query_string}"

        return self.call_api(endpoint, ApiCategory.INFORMATION, "GET", RankingApiResponse)

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
        """
        return self.call_api(f"exchange/{symbol}", ApiCategory.INFORMATION, "GET", ExchangeBySymbolApiResponse)

    def regulations_by_symbol(self, symbol: str):
        """
        規制情報＋空売り規制情報を取得する

        Args:
            symbol (str): 銘柄コード
        """
        return self.call_api(f"regulations/{symbol}", ApiCategory.INFORMATION, "GET", RegulationsBySymbolApiResponse)

    def primaryexchange_by_symbol(self, symbol: str):
        """
        株式の優先市場を取得する

        Args:
            symbol (str): 銘柄コード
        """
        return self.call_api(
            f"primaryexchange/{symbol}", ApiCategory.INFORMATION, "GET", PrimaryexchangeBySymbolApiResponse
        )

    def apisoftlimit(self):
        """
        kabuステーションAPIのソフトリミット値を取得する
        """
        return self.call_api("apisoftlimit", ApiCategory.INFORMATION, "GET", ApisoftlimitApiResponse)

    def margin_marginpremium_by_symbol(self, symbol: str):
        """
        指定した銘柄のプレミアム料を取得するAPI

        Args:
            symbol (str): 銘柄コード
        """
        return self.call_api(
            f"margin/marginpremium/{symbol}", ApiCategory.INFORMATION, "GET", MarginMarginpremiumBySymbolApiResponse
        )

    def register(self, symbols: List[Dict[str, Any]]):
        """
        ```
        PUSH配信する銘柄を登録します。
        API登録銘柄リストを開くには、kabuステーションAPIインジケーターを右クリックし「API登録銘柄リスト」を選択してください。
        ```

        Args:
            symbols (List[Dict[str, Any]]): 登録する銘柄のリスト
        """
        payload = {"Symbols": symbols}

        return self.call_api("register", ApiCategory.STOCK_REGISTRATION, "PUT", RegisterApiResponse, payload)

    def unregister(self, symbols: List[Dict[str, Any]]):
        """
        ```
        API登録銘柄リストに登録されている銘柄を解除します
        ※為替銘柄を登録する場合、銘柄名は"通貨A" + "/" + "通貨B"、市場コードは"300"で指定してください。
        例：'Symbol': 'EUR/USD', "Exchange": 300
        ```

        Args:
            symbols (List[Dict[str, Any]]): 登録解除する銘柄のリスト
        """
        payload = {"Symbols": symbols}

        return self.call_api("unregister", ApiCategory.STOCK_REGISTRATION, "PUT", UnregisterApiResponse, payload)

    def unregister_all(self):
        """
        API登録銘柄リストに登録されている銘柄をすべて解除します
        """
        return self.call_api("unregister/all", ApiCategory.STOCK_REGISTRATION, "PUT", UnregisterAllApiResponse)

    def start_websocket(
        self,
        on_message: Callable[[WebSocketPushData], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_connect: Callable[[], None] | None = None,
        on_disconnect: Callable[[], None] | None = None,
    ):
        """
        ```
        WebSocket接続を開始し、リアルタイム市場データの受信を開始します。
        事前にregister()で銘柄を登録してください。
        ```

        Args:
            on_message: データ受信時のコールバック関数
            on_error: エラー発生時のコールバック関数
            on_connect: 接続完了時のコールバック関数
            on_disconnect: 切断時のコールバック関数
        """
        if not self.x_api_key:
            raise ValueError("API token is not set. Call 'token' method first.")

        if self.ws is not None:
            raise ValueError("WebSocket is already connected. Call 'stop_websocket' first.")

        self.on_message_callback = on_message
        self.on_error_callback = on_error
        self.on_connect_callback = on_connect
        self.on_disconnect_callback = on_disconnect

        def on_ws_message(ws, message):  # noqa: ARG001
            try:
                data = json.loads(message)
                push_data = WebSocketPushData(**data)
                if self.on_message_callback:
                    self.on_message_callback(push_data)
            except Exception as e:
                if self.on_error_callback:
                    self.on_error_callback(e)

        def on_ws_error(ws, error):  # noqa: ARG001
            if self.on_error_callback:
                self.on_error_callback(error)

        def on_ws_open(ws):  # noqa: ARG001
            if self.on_connect_callback:
                self.on_connect_callback()

        def on_ws_close(ws, close_status_code, close_msg):  # noqa: ARG001
            if self.on_disconnect_callback:
                self.on_disconnect_callback()

        headers = {"X-API-KEY": self.x_api_key}
        if self.is_in_docker_container:
            headers["Host"] = "localhost"

        self.ws = ws.WebSocketApp(
            self.websocket_url,
            header=headers,
            on_message=on_ws_message,
            on_error=on_ws_error,
            on_open=on_ws_open,
            on_close=on_ws_close,
        )

        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def stop_websocket(self):
        """
        WebSocket接続を停止します
        """
        if self.ws is not None:
            self.ws.close()
            self.ws = None

        if self.ws_thread is not None:
            self.ws_thread.join(timeout=5)
            self.ws_thread = None

    def is_websocket_connected(self) -> bool:
        """
        WebSocket接続状態を確認します

        Returns:
            bool: 接続中の場合True
        """
        return self.ws is not None and self.ws_thread is not None and self.ws_thread.is_alive()

    def send_websocket_message(self, message: str):
        """
        WebSocket経由でメッセージを送信します

        Args:
            message (str): 送信するメッセージ
        """
        if self.ws is None:
            raise ValueError("WebSocket is not connected. Call 'start_websocket' first.")

        self.ws.send(message)
