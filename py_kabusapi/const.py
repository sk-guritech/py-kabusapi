from enum import IntEnum


class ApiCategory(IntEnum):
    AUTHENTICATION = 0
    ORDER_PLACEMENT = 1
    TRADING_CAPACITY = 2
    INFORMATION = 3
    STOCK_REGISTRATION = 4


class ApiResultCategory(IntEnum):
    SUCCESS = 0
    HTTP_ERROR = 1
    API_ERROR = 2
