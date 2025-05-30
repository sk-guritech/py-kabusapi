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
