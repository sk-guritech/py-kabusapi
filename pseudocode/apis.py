def post_token(api_password: str) -> dict:
    """
    トークンを発行します。

    Args:
        api_password (str): APIパスワード。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - ResultCode (int): 結果コード。0が成功、それ以外はエラーコード。
            - Token (str): APIトークン。
    """
    pass


def post_sendorder(
    symbol: str,
    exchange: int,
    security_type: int,
    side: str,
    cash_margin: int,
    deliv_type: int,
    account_type: int,
    qty: int,
    price: float,
    expire_day: int,
    front_order_type: int,
    margin_trade_type: int = None,
    margin_premium_unit: float = None,
    fund_type: str = None,
    close_position_order: int = None,
    close_positions: list = None,
    reverse_limit_order: dict = None,
) -> dict:
    """
    注文を発注します。

    Args:
        symbol (str): 銘柄コード。
        exchange (int): 市場コード。
            - 1: 東証
            - 3: 名証
            - 5: 福証
            - 6: 札証
            - 9: SOR
            - 27: 東証+
        security_type (int): 商品種別。
            - 1: 株式
        side (str): 売買区分。
            - "1": 売
            - "2": 買
        cash_margin (int): 信用区分。
            - 1: 現物
            - 2: 新規
            - 3: 返済
        deliv_type (int): 受渡区分。現物買と信用返済は必須。現物売と信用新規は「0(指定なし)」を設定。
            - 0: 指定なし
            - 2: お預り金
            - 3: auマネーコネクト (auマネーコネクト有効時のみ)
        account_type (int): 口座種別。
            - 2: 一般
            - 4: 特定
            - 12: 法人
        qty (int): 注文数量。信用一括返済の場合、返済したい合計数量。
        price (float): 注文価格。成行の場合は0。
        expire_day (int): 注文有効期限 (yyyyMMdd形式)。0を指定すると「本日」に対応。
        front_order_type (int): 執行条件。
            - 10: 成行 (Price=0)
            - 13: 寄成（前場） (Price=0)
            - 14: 寄成（後場） (Price=0)
            - 15: 引成（前場） (Price=0)
            - 16: 引成（後場） (Price=0)
            - 17: IOC成行 (Price=0)
            - 20: 指値 (Price=発注したい金額)
            - 21: 寄指（前場） (Price=発注したい金額)
            - 22: 寄指（後場） (Price=発注したい金額)
            - 23: 引指（前場） (Price=発注したい金額)
            - 24: 引指（後場） (Price=発注したい金額)
            - 25: 不成（前場） (Price=発注したい金額)
            - 26: 不成（後場） (Price=発注したい金額)
            - 27: IOC指値 (Price=発注したい金額)
            - 30: 逆指値 (Price=指定なし、ReverseLimitOrderで指定)
        margin_trade_type (int, optional): 信用取引区分。現物取引の場合は指定不要、信用取引の場合は必須。
            - 1: 制度信用
            - 2: 一般信用（長期）
            - 3: 一般信用（デイトレ）
        margin_premium_unit (float, optional): 1株あたりのプレミアム料(円)。入札受付中のプレミアム料入札可能銘柄の場合、必須。
        fund_type (str, optional): 資産区分（預り区分）。現物買は必須。現物売は「'  '」 (半角スペース2つ) を指定必須。信用新規と信用返済は「11」を指定するか、指定なしでも可。
            - "  ": 現物売の場合
            - "02": 保護
            - "AA": 信用代用
            - "11": 信用取引
        close_position_order (int, optional): 決済順序。信用返済の場合、必須。
            - 0: 日付（古い順）、損益（高い順）
            - 1: 日付（古い順）、損益（低い順）
            - 2: 日付（新しい順）、損益（高い順）
            - 3: 日付（新しい順）、損益（低い順）
            - 4: 損益（高い順）、日付（古い順）
            - 5: 損益（高い順）、日付（新しい順）
            - 6: 損益（低い順）、日付（古い順）
            - 7: 損益（低い順）、日付（新しい順）
        close_positions (list, optional): 返済建玉指定。信用返済の場合、必須。
            - HoldID (str): 建玉ID。
            - Qty (int): 返済したい数量。
        reverse_limit_order (dict, optional): 逆指値条件。FrontOrderTypeで逆指値を指定した場合のみ必須。
            - TriggerSec (int): トリガ銘柄。
                - 1: 発注銘柄
                - 2: NK225指数
                - 3: TOPIX指数
            - TriggerPrice (float): トリガ価格。
            - UnderOver (int): 以上／以下。
                - 1: 以下
                - 2: 以上
            - AfterHitOrderType (int): ヒット後執行条件。
                - 1: 成行
                - 2: 指値
                - 3: 不成
            - AfterHitPrice (float): ヒット後注文価格。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Result (int): 結果コード。0が成功、それ以外はエラーコード。
            - OrderId (str): 受付注文番号。
    """
    pass


def post_sendorder_future(
    symbol: str,
    exchange: int,
    trade_type: int,
    time_in_force: int,
    side: str,
    qty: int,
    price: float,
    expire_day: int,
    front_order_type: int,
    close_position_order: int = None,
    close_positions: list = None,
    reverse_limit_order: dict = None,
) -> dict:
    """
    先物取引の注文を発注します。

    Args:
        symbol (str): 銘柄コード。
        exchange (int): 市場コード。
            - 2: 日通し
            - 23: 日中
            - 24: 夜間
            - 32: SOR日通し
            - 33: SOR日中
            - 34: SOR夜間
        trade_type (int): 取引区分。
            - 1: 新規
            - 2: 返済
        time_in_force (int): 有効期間条件。
            - 1: FAS
            - 2: FAK
            - 3: FOK
        side (str): 売買区分。
            - "1": 売
            - "2": 買
        qty (int): 注文数量。
        price (float): 注文価格。成行を指定した場合、0を指定。
        expire_day (int): 注文有効期限 (yyyyMMdd形式)。0を指定すると「本日」に対応。
        front_order_type (int): 執行条件。
            - 18: 引成（派生） (Price=0)
            - 20: 指値 (Price=発注したい金額)
            - 28: 引指（派生） (Price=発注したい金額)
            - 30: 逆指値 (Price=指定なし、ReverseLimitOrderで指定)
            - 120: 成行（マーケットオーダー） (Price=0)
        close_position_order (int, optional): 決済順序。ClosePositionOrderとClosePositionsはどちらか一方のみ指定可能。
            - 0: 日付（古い順）、損益（高い順）
            - 1: 日付（古い順）、損益（低い順）
            - 2: 日付（新しい順）、損益（高い順）
            - 3: 日付（新しい順）、損益（低い順）
            - 4: 損益（高い順）、日付（古い順）
            - 5: 損益（高い順）、日付（新しい順）
            - 6: 損益（低い順）、日付（古い順）
            - 7: 損益（低い順）、日付（新しい順）
        close_positions (list, optional): 返済建玉指定。ClosePositionOrderとClosePositionsはどちらか一方のみ指定可能。
            - HoldID (str): 建玉ID。
            - Qty (int): 返済したい数量。
        reverse_limit_order (dict, optional): 逆指値条件。FrontOrderTypeで逆指値を指定した場合のみ必須。
            - TriggerPrice (float): トリガ価格。
            - UnderOver (int): 以上／以下。
                - 1: 以下
                - 2: 以上
            - AfterHitOrderType (int): ヒット後執行条件。
                - 1: 成行
                - 2: 指値
            - AfterHitPrice (float): ヒット後注文価格。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Result (int): 結果コード。0が成功、それ以外はエラーコード。
            - OrderId (str): 受付注文番号。
    """
    pass


def post_sendorder_option(
    symbol: str,
    exchange: int,
    trade_type: int,
    time_in_force: int,
    side: str,
    qty: int,
    price: float,
    expire_day: int,
    front_order_type: int,
    close_position_order: int = None,
    close_positions: list = None,
    reverse_limit_order: dict = None,
) -> dict:
    """
    オプション取引の注文を発注します。

    Args:
        symbol (str): 銘柄コード。
        exchange (int): 市場コード。
            - 2: 日通し
            - 23: 日中
            - 24: 夜間
        trade_type (int): 取引区分。
            - 1: 新規
            - 2: 返済
        time_in_force (int): 有効期間条件。
            - 1: FAS
            - 2: FAK
            - 3: FOK
        side (str): 売買区分。
            - "1": 売
            - "2": 買
        qty (int): 注文数量。
        price (float): 注文価格。成行を指定した場合、0を指定。
        expire_day (int): 注文有効期限 (yyyyMMdd形式)。0を指定すると「本日」に対応。
        front_order_type (int): 執行条件。
            - 18: 引成（派生） (Price=0)
            - 20: 指値 (Price=発注したい金額)
            - 28: 引指（派生） (Price=発注したい金額)
            - 30: 逆指値 (Price=指定なし、ReverseLimitOrderで指定)
            - 120: 成行（マーケットオーダー） (Price=0)
        close_position_order (int, optional): 決済順序。ClosePositionOrderとClosePositionsはどちらか一方のみ指定可能。
            - 0: 日付（古い順）、損益（高い順）
            - 1: 日付（古い順）、損益（低い順）
            - 2: 日付（新しい順）、損益（高い順）
            - 3: 日付（新しい順）、損益（低い順）
            - 4: 損益（高い順）、日付（古い順）
            - 5: 損益（高い順）、日付（新しい順）
            - 6: 損益（低い順）、日付（古い順）
            - 7: 損益（低い順）、日付（新しい順）
        close_positions (list, optional): 返済建玉指定。ClosePositionOrderとClosePositionsはどちらか一方のみ指定可能。
            - HoldID (str): 建玉ID。
            - Qty (int): 返済したい数量。
        reverse_limit_order (dict, optional): 逆指値条件。FrontOrderTypeで逆指値を指定した場合のみ必須。
            - TriggerPrice (float): トリガ価格。
            - UnderOver (int): 以上／以下。
                - 1: 以下
                - 2: 以上
            - AfterHitOrderType (int): ヒット後執行条件。
                - 1: 成行
                - 2: 指値
            - AfterHitPrice (float): ヒット後注文価格。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Result (int): 結果コード。0が成功、それ以外はエラーコード。
            - OrderId (str): 受付注文番号。
    """
    pass


def put_cancelorder(order_id: str) -> dict:
    """
    注文をキャンセルします。

    Args:
        order_id (str): 注文番号。sendorderのレスポンスで受け取ったOrderID。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Result (int): 結果コード。0が成功、それ以外はエラーコード。
            - OrderId (str): 受付注文番号。
    """
    pass


def get_wallet_cash() -> dict:
    """
    現物買付可能額を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - StockAccountWallet (float): 現物買付可能額。
            - AuKCStockAccountWallet (float): うち、三菱UFJ eスマート証券可能額。
            - AuJbnStockAccountWallet (float): うち、auじぶん銀行残高。
    """
    pass


def get_wallet_cash_by_symbol(symbol: str) -> dict:
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
    pass


def get_wallet_margin() -> dict:
    """
    信用新規可能額を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - MarginAccountWallet (float): 信用新規可能額。
            - DepositkeepRate (float): 保証金維持率。銘柄指定の場合のみ。
            - ConsignmentDepositRate (float): 委託保証金率。銘柄指定の場合のみ。
            - CashOfConsignmentDepositRate (float): 現金委託保証金率。銘柄指定の場合のみ。
    """
    pass


def get_wallet_margin_by_symbol(symbol: str) -> dict:
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
    pass


def get_wallet_future() -> dict:
    """
    先物新規建玉可能額を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - FutureTradeLimit (float): 新規建玉可能額。
            - MarginRequirement (float): 買い必要証拠金額。銘柄指定の場合のみ。
            - MarginRequirementSell (float): 売り必要証拠金額。銘柄指定の場合のみ。
    """
    pass


def get_wallet_future_by_symbol(symbol: str) -> dict:
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
    pass


def get_wallet_option() -> dict:
    """
    オプション新規建玉可能額を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - OptionBuyTradeLimit (float): 買新規建玉可能額。
            - OptionSellTradeLimit (float): 売新規建玉可能額。
            - MarginRequirement (float): 必要証拠金額。銘柄指定の場合のみ。
    """
    pass


def get_wallet_option_by_symbol(symbol: str) -> dict:
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
    pass


def get_board_by_symbol(symbol: str) -> dict:
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
    pass


def get_symbol_by_symbol(symbol: str) -> dict:
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
    pass


def get_orders() -> list:
    """
    注文一覧を取得します。

    Returns:
        list: リクエスト成功時のJSONデータ（OrdersSuccessオブジェクトのリスト）。
    """
    pass


def get_positions() -> list:
    """
    建玉一覧を取得します。

    Returns:
        list: リクエスト成功時のJSONデータ（PositionsSuccessオブジェクトのリスト）。
    """
    pass


def put_register(symbols: list) -> dict:
    """
    銘柄を登録します。

    Args:
        symbols (list): 登録する銘柄のリスト。
            - Symbol (str): 銘柄コード。
            - Exchange (int): 市場コード。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - RegistList (list): 現在登録されている銘柄のリスト。
                - Symbol (str): 銘柄コード。
                - Exchange (int): 市場コード。
    """
    pass


def put_unregister(symbols: list) -> dict:
    """
    銘柄登録を解除します。

    Args:
        symbols (list): 登録解除する銘柄のリスト。
            - Symbol (str): 銘柄コード。
            - Exchange (int): 市場コード。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - RegistList (list): 現在登録されている銘柄のリスト。
                - Symbol (str): 銘柄コード。
                - Exchange (int): 市場コード。
    """
    pass


def put_unregister_all() -> dict:
    """
    全ての銘柄登録を解除します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - RegistList (dict): 現在登録されている銘柄のリスト。
    """
    pass


def get_symbolname_future() -> dict:
    """
    先物銘柄コードから銘柄名称を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Symbol (str): 銘柄コード。
            - SymbolName (str): 銘柄名称。
    """
    pass


def get_symbolname_option() -> dict:
    """
    オプション銘柄コードから銘柄名称を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Symbol (str): 銘柄コード。
            - SymbolName (str): 銘柄名称。
    """
    pass


def get_symbolname_minioptionweekly() -> dict:
    """
    ミニオプション（週次）銘柄コードから銘柄名称を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Symbol (str): 銘柄コード。
            - SymbolName (str): 銘柄名称。
    """
    pass


def get_ranking() -> dict:
    """
    ランキング情報を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。ランキングの種類によってスキーマが異なります。
    """
    pass


def get_exchange_by_symbol(symbol: str) -> dict:
    """
    為替レート情報を取得します。

    Args:
        symbol (str): 通貨ペア。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Symbol (str): 通貨。
            - BidPrice (float): BID価格。
            - Spread (float): スプレッド。
            - AskPrice (float): ASK価格。
            - Change (float): 前日比。
            - Time (str): 時刻 (HH:mm:ss形式)。
    """
    pass


def get_regulations_by_symbol(symbol: str) -> dict:
    """
    指定した銘柄の規制情報を取得します。

    Args:
        symbol (str): 銘柄コード。対象商品は株式のみ。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Symbol (str): 銘柄コード。
            - RegulationsInfo (list): 規制情報のリスト。
                - Exchange (int): 規制市場。
                - Product (int): 規制取引区分。
                - Side (str): 規制売買。
                - Reason (str): 理由。
                - LimitStartDay (str): 制限開始日 (yyyy/MM/dd HH:mm形式)。
                - LimitEndDay (str): 制限終了日 (yyyy/MM/dd HH:mm形式)。
                - Level (int): コンプライアンスレベル。
    """
    pass


def get_primaryexchange_by_symbol(symbol: str) -> dict:
    """
    指定した銘柄の優先市場を取得します。

    Args:
        symbol (str): 銘柄コード。対象商品は株式のみ。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Symbol (str): 銘柄コード。
            - PrimaryExchange (int): 優先市場。
    """
    pass


def get_apisoftlimit() -> dict:
    """
    APIのワンショット上限値を取得します。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Stock (float): 現物のワンショット上限 (万円)。
            - Margin (float): 信用のワンショット上限 (万円)。
            - Future (float): 先物のワンショット上限 (枚)。
            - FutureMini (float): ミニ先物のワンショット上限 (枚)。
            - FutureMicro (float): マイクロ先物のワンショット上限 (枚)。
            - Option (float): オプションのワンショット上限 (枚)。
            - MiniOption (float): ミニオプションのワンショット上限 (枚)。
            - KabuSVersion (str): kabuステーションのバージョン。
    """
    pass


def get_margin_marginpremium_by_symbol(symbol: str) -> dict:
    """
    指定した銘柄のプレミアム料情報を取得します。

    Args:
        symbol (str): 銘柄コード。

    Returns:
        dict: リクエスト成功時のJSONデータ。
            - Symbol (str): 銘柄コード。
            - GeneralMargin (dict): 一般信用（長期）に関する情報。
                - MarginPremiumType (int): プレミアム料入力区分。
                - MarginPremium (float): 確定プレミアム料。
                - UpperMarginPremium (float): 上限プレミアム料。
                - LowerMarginPremium (float): 下限プレミアム料。
                - TickMarginPremium (float): プレミアム料刻値。
            - DayTrade (dict): 一般信用（デイトレ）に関する情報。
                - MarginPremiumType (int): プレミアム料入力区分。
                - MarginPremium (float): 確定プレミアム料。
                - UpperMarginPremium (float): 上限プレミアム料。
                - LowerMarginPremium (float): 下限プレミアム料。
                - TickMarginPremium (float): プレミアム料刻値。
    """
    pass
