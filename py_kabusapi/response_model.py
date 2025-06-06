from typing import Generic, Literal, Optional, TypeVar, cast

from pydantic import BaseModel, RootModel, model_validator

from .const import ApiResultCategory

T = TypeVar("T", bound=BaseModel)


class HttpErrorResponse(BaseModel):
    Code: int  # エラーコード
    Message: str  # エラーメッセージ


class ApiErrorResponse(BaseModel):
    ResultCode: int  # エラーコード


class ApiResultSuccess(BaseModel, Generic[T]):
    api_result_category: Literal[ApiResultCategory.SUCCESS] = ApiResultCategory.SUCCESS
    content: T


class ApiResultHttpError(BaseModel):
    api_result_category: Literal[ApiResultCategory.HTTP_ERROR] = ApiResultCategory.HTTP_ERROR
    content: HttpErrorResponse


class ApiResultApiError(BaseModel):
    api_result_category: Literal[ApiResultCategory.API_ERROR] = ApiResultCategory.API_ERROR
    content: ApiErrorResponse


# /token
class TokenApiResponse(BaseModel):
    ResultCode: int  # 結果コード
    Token: str  # APIトークン


# /sendorder
class SendorderApiResponse(BaseModel):
    Result: int  # 結果コード
    OrderId: Optional[str] = None  # 受付注文番号（テスト環境ではnullの場合あり）


# /sendorder/future
class SendorderFutureApiResponse(BaseModel):
    Result: int  # 結果コード
    OrderId: Optional[str] = None  # 受付注文番号（テスト環境ではnullの場合あり）


# /sendorder/option
class SendorderOptionApiResponse(BaseModel):
    Result: int  # 結果コード
    OrderId: Optional[str] = None  # 受付注文番号（テスト環境ではnullの場合あり）


# /cancelorder
class CancelorderApiResponse(BaseModel):
    Result: int  # 結果コード
    OrderId: str  # 受付注文番号


# /wallet/cash
class WalletCashApiResponse(BaseModel):
    StockAccountWallet: float  # 現物買付可能額
    AuKCStockAccountWallet: float  # うち、三菱UFJ eスマート証券可能額
    AuJbnStockAccountWallet: float  # うち、auじぶん銀行残高


# /wallet/cash/{symbol}
class WalletCashBySymbolApiResponse(BaseModel):
    StockAccountWallet: float  # 現物買付可能額
    AuKCStockAccountWallet: float  # うち、三菱UFJ eスマート証券可能額
    AuJbnStockAccountWallet: float  # うち、auじぶん銀行残高


# /wallet/margin
class WalletMarginApiResponse(BaseModel):
    MarginAccountWallet: float  # 信用新規可能額
    DepositkeepRate: float  # 保証金維持率
    ConsignmentDepositRate: float | None  # 委託保証金率
    CashOfConsignmentDepositRate: float | None  # 現金委託保証金率


# /wallet/margin/{symbol}
class WalletMarginBySymbolApiResponse(BaseModel):
    MarginAccountWallet: float  # 信用新規可能額
    DepositkeepRate: float  # 保証金維持率
    ConsignmentDepositRate: float | None  # 委託保証金率
    CashOfConsignmentDepositRate: float | None  # 現金委託保証金率


# /wallet/future
class WalletFutureApiResponse(BaseModel):
    FutureTradeLimit: float  # 新規建玉可能額
    MarginRequirement: float | None  # 買い必要証拠金額
    MarginRequirementSell: float | None  # 売り必要証拠金額


# /wallet/future/{symbol}
class WalletFutureBySymbolApiResponse(BaseModel):
    FutureTradeLimit: float  # 新規建玉可能額

    MarginRequirement: float | None  # 買い必要証拠金額
    MarginRequirementSell: float | None  # 売り必要証拠金額


# /wallet/option
class WalletOptionApiResponse(BaseModel):
    OptionBuyTradeLimit: float  # 買新規建玉可能額
    OptionSellTradeLimit: float  # 売新規建玉可能額

    MarginRequirement: float | None  # 必要証拠金額


# /wallet/option/{symbol}
class WalletOptionBySymbolApiResponse(BaseModel):
    OptionBuyTradeLimit: float  # 買新規建玉可能額
    OptionSellTradeLimit: float  # 売新規建玉可能額
    MarginRequirement: float | None  # 必要証拠金額


# /board/{symbol}
class BoardBySymbolApiResponse(BaseModel):
    class HeadBidAskDetail(BaseModel):
        Time: str  # 時刻

        Sign: str  # 気配フラグ

        Price: float  # 値段
        Qty: float  # 数量

    class BidAskDetail(BaseModel):
        Price: float  # 値段
        Qty: float  # 数量

    Symbol: str  # 銘柄コード
    SymbolName: str  # 銘柄名
    Exchange: int | None = None  # 市場コード
    ExchangeName: str | None = None  # 市場名称
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
    TradingVolume: float | None = None  # 売買高
    TradingVolumeTime: str | None = None  # 売買高時刻
    VWAP: float | None = None  # 売買高加重平均価格(VWAP)
    TradingValue: float | None = None  # 売買代金
    BidQty: float | None = None  # 最良売気配数量
    BidPrice: float | None = None  # 最良売気配値段
    BidTime: str | None = None  # 最良売気配時刻
    BidSign: str | None = None  # 最良売気配フラグ
    MarketOrderSellQty: float | None = None  # 売成行数量
    Sell1: HeadBidAskDetail  # 売気配数量1本目
    Sell2: BidAskDetail  # 売気配数量2本目
    Sell3: BidAskDetail  # 売気配数量3本目
    Sell4: BidAskDetail  # 売気配数量4本目
    Sell5: BidAskDetail  # 売気配数量5本目
    Sell6: BidAskDetail  # 売気配数量6本目
    Sell7: BidAskDetail  # 売気配数量7本目
    Sell8: BidAskDetail  # 売気配数量8本目
    Sell9: BidAskDetail  # 売気配数量9本目
    Sell10: BidAskDetail  # 売気配数量10本目
    AskQty: float | None = None  # 最良買気配数量
    AskPrice: float | None = None  # 最良買気配値段
    AskTime: str | None = None  # 最良買気配時刻
    AskSign: str | None = None  # 最良買気配フラグ
    MarketOrderBuyQty: float | None = None  # 買成行数量
    Buy1: HeadBidAskDetail  # 買気配数量1本目
    Buy2: BidAskDetail  # 買気配数量2本目
    Buy3: BidAskDetail  # 買気配数量3本目
    Buy4: BidAskDetail  # 買気配数量4本目
    Buy5: BidAskDetail  # 買気配数量5本目
    Buy6: BidAskDetail  # 買気配数量6本目
    Buy7: BidAskDetail  # 買気配数量7本目
    Buy8: BidAskDetail  # 買気配数量8本目
    Buy9: BidAskDetail  # 買気配数量9本目
    Buy10: BidAskDetail  # 買気配数量10本目
    OverSellQty: float | None = None  # OVER気配数量
    UnderBuyQty: float | None = None  # UNDER気配数量
    TotalMarketValue: float | None = None  # 時価総額
    ClearingPrice: float | None = None  # 清算値
    IV: float | None = None  # インプライド・ボラティリティ
    Gamma: float | None = None  # ガンマ
    Theta: float | None = None  # セータ
    Vega: float | None = None  # ベガ
    Delta: float | None = None  # デルタ
    SecurityType: int  # 銘柄種別


# /symbol/{symbol}
class SymbolBySymbolApiResponse(BaseModel):
    Symbol: str  # 銘柄コード
    SymbolName: str  # 銘柄名

    DisplayName: str | None = None  # 銘柄略称
    Exchange: int | None = None  # 市場コード
    ExchangeName: str | None = None  # 市場名称
    BisCategory: str | None = None  # 業種コード名
    TotalMarketValue: float | None = None  # 時価総額
    TotalStocks: float | None = None  # 発行済み株式数（千株）
    TradingUnit: float | None = None  # 売買単位
    FiscalYearEndBasic: int | None = None  # 決算期日

    PriceRangeGroup: str | None = None  # 呼値グループ
    KCMarginBuy: bool | None = None  # 一般信用買建フラグ
    KCMarginSell: bool | None = None  # 一般信用売建フラグ
    MarginBuy: bool | None = None  # 制度信用買建フラグ
    MarginSell: bool | None = None  # 制度信用売建フラグ
    UpperLimit: float | None = None  # 値幅上限
    LowerLimit: float | None = None  # 値幅下限
    Underlyer: str | None = None  # 原資産コード
    DerivMonth: str | None = None  # 限月-年月
    TradeStart: int | None = None  # 取引開始日
    TradeEnd: int | None = None  # 取引終了日
    StrikePrice: float | None = None  # 権利行使価格
    PutOrCall: int | None = None  # プット/コール区分
    ClearingPrice: float | None = None  # 清算値


# /orders
class OrderDetail(BaseModel):
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


class Order(BaseModel):
    Id: str  # 注文番号
    State: str  # 状態
    OrderState: str  # 注文状態
    OrdType: int  # 執行条件
    RecvTime: str  # 受注日時
    Symbol: str  # 銘柄コード
    SymbolName: str  # 銘柄名
    Exchange: int  # 市場コード
    ExchangeName: str  # 市場名
    TimeInForce: int | None = None  # 有効期間条件
    Price: float  # 値段
    OrderQty: float  # 発注数量
    CumQty: float  # 約定数量
    Side: str  # 売買区分
    CashMargin: int  # 取引区分
    AccountType: int  # 口座種別
    DelivType: int  # 受渡区分
    ExpireDay: int  # 有効期限 (yyyyMMdd形式)
    MarginTradeType: int  # 信用取引区分
    MarginPremium: float | None = None  # プレミアム料
    Details: list[OrderDetail]  # 注文詳細


class OrdersApiResponse(RootModel[list[Order]]):
    pass


# /positions
class Position(BaseModel):
    ExecutionID: str | None = None  # 約定番号
    AccountType: int  # 口座種別
    Symbol: str  # 銘柄コード
    SymbolName: str  # 銘柄名
    Exchange: int  # 市場コード
    ExchangeName: str  # 市場名
    SecurityType: int  # 銘柄種別
    ExecutionDay: str | None = None  # 約定日（建玉日）

    Price: float  # 値段
    LeavesQty: float  # 残数量（保有数量）
    HoldQty: float  # 拘束数量（返済のために拘束されている数量）
    Side: str  # 売買区分
    Expenses: float | None = None  # 諸経費
    Commission: float | None = None  # 手数料
    CommissionTax: float | None = None  # 手数料消費税
    ExpireDay: int | None = None  # 返済期日
    MarginTradeType: int | None = None  # 信用取引区分
    CurrentPrice: float | None = None  # 現在値
    Valuation: float | None = None  # 評価金額
    ProfitLoss: float | None = None  # 評価損益額
    ProfitLossRate: float | None = None  # 評価損益率


class PositionsApiResponse(RootModel[list[Position]]):
    pass


# /symbolname/future
class SymbolnameFutureApiResponse(BaseModel):
    Symbol: str  # 銘柄コード
    SymbolName: str  # 銘柄名称


# /symbolname/option
class SymbolnameOptionApiResponse(BaseModel):
    Symbol: str  # 銘柄コード
    SymbolName: str  # 銘柄名称


# /symbolname/minioptionweekly
class SymbolnameMinioptionweeklyApiResponse(BaseModel):
    Symbol: str  # 銘柄コード
    SymbolName: str  # 銘柄名称


# /ranking
class RankTypeFor1To4(BaseModel):  # type: ignore
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


class RankTypeFor5(BaseModel):  # type: ignore
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


class RankTypeFor6(BaseModel):  # type: ignore
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


class RankTypeFor7(BaseModel):  # type: ignore
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


class RankTypeFor8To13(BaseModel):  # type: ignore
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


class RankTypeFor14To15(BaseModel):  # type: ignore
    No: Optional[int]  # 順位
    Trend: Literal["0", "1", "2", "3", "4", "5"]  # トレンド
    AverageRanking: float  # 平均順位
    Category: str  # 業種コード
    CategoryName: str  # 業種名
    CurrentPrice: float  # 現在値
    ChangeRatio: float  # 前日比
    CurrentPriceTime: str  # 時刻: HH:mm
    ChangePercentage: float  # 騰落率(%)


class RankingApiResponse(BaseModel):
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

    @model_validator(mode="before")
    @classmethod
    def _validate_ranking_type(cls, data: dict) -> dict:
        _ranking_type_map = {
            "1": RankTypeFor1To4,
            "2": RankTypeFor1To4,
            "3": RankTypeFor1To4,
            "4": RankTypeFor1To4,
            "5": RankTypeFor5,
            "6": RankTypeFor6,
            "7": RankTypeFor7,
            "8": RankTypeFor8To13,
            "9": RankTypeFor8To13,
            "10": RankTypeFor8To13,
            "11": RankTypeFor8To13,
            "12": RankTypeFor8To13,
            "13": RankTypeFor8To13,
            "14": RankTypeFor14To15,
            "15": RankTypeFor14To15,
        }

        if "Type" not in data or "Ranking" not in data or not isinstance(data["Ranking"], list):
            return data

        ranking_type_value = cast(str, data["Type"])
        ranking_data_list = cast(list[dict], data.get("Ranking"))

        expected_model: (
            RankTypeFor1To4 | RankTypeFor5 | RankTypeFor6 | RankTypeFor7 | RankTypeFor8To13 | RankTypeFor14To15
        ) = _ranking_type_map[ranking_type_value]

        validated_ranking_data_list = []
        for ranking_data in ranking_data_list:
            validated_ranking_data_list.append(expected_model.model_validate(ranking_data))

        data["Ranking"] = validated_ranking_data_list

        return data


# /exchange/{symbol}
class ExchangeBySymbolApiResponse(BaseModel):
    Symbol: str  # 通貨
    BidPrice: float  # BID
    Spread: float  # SP
    AskPrice: float  # ASK
    Change: float  # 前日比
    Time: str  # 時刻 (HH:mm:ss形式)


# /regulations/{symbol}
class RegulationsBySymbolApiResponse(BaseModel):
    class RegulationInfo(BaseModel):  # type: ignore
        Exchange: int  # 規制市場
        Product: int  # 規制取引区分
        Side: str  # 規制売買
        Reason: str  # 理由
        LimitStartDay: str | None = None  # 制限開始日 (yyyy/MM/dd HH:mm形式)
        LimitEndDay: str | None = None  # 制限終了日 (yyyy/MM/dd HH:mm形式)
        Level: int | None = None  # コンプライアンスレベル

    Symbol: str  # 銘柄コード
    RegulationsInfo: list[RegulationInfo]  # 規制情報


# /primaryexchange/{symbol}
class PrimaryexchangeBySymbolApiResponse(BaseModel):
    Symbol: str  # 銘柄コード
    PrimaryExchange: int  # 優先市場


# /apisoftlimit
class ApisoftlimitApiResponse(BaseModel):
    Stock: float  # 現物のワンショット上限 (万円)
    Margin: float  # 信用のワンショット上限 (万円)
    Future: float  # 先物のワンショット上限 (枚)
    FutureMini: float  # ミニ先物のワンショット上限 (枚)
    FutureMicro: float  # マイクロ先物のワンショット上限 (枚)

    Option: float  # オプションのワンショット上限 (枚)
    MiniOption: float  # ミニオプションのワンショット上限 (枚)
    kabuSVersion: str  # kabuステーションのバージョン


# /margin/marginpremium/{symbol}
class MarginMarginpremiumBySymbolApiResponse(BaseModel):
    class GeneralMarginDetail(BaseModel):
        MarginPremiumType: int | None = None  # プレミアム料入力区分
        MarginPremium: float | None = None  # 確定プレミアム料
        UpperMarginPremium: float | None = None  # 上限プレミアム料

        LowerMarginPremium: float | None = None  # 下限プレミアム料
        TickMarginPremium: float | None = None  # プレミアム料刻値

    class DayTradeDetail(BaseModel):
        MarginPremiumType: int | None = None  # プレミアム料入力区分

        MarginPremium: float | None = None  # 確定プレミアム料
        UpperMarginPremium: float | None = None  # 上限プレミアム料
        LowerMarginPremium: float | None = None  # 下限プレミアム料
        TickMarginPremium: float | None = None  # プレミアム料刻値

    Symbol: str  # 銘柄コード
    GeneralMargin: GeneralMarginDetail  # 一般信用(長期)
    DayTrade: DayTradeDetail  # 一般信用(デイトレ)


class RegistListItem(BaseModel):
    Symbol: str  # 銘柄コード
    Exchange: int  # 市場コード


class RegisterApiResponse(BaseModel):
    RegistList: list[RegistListItem]  # 現在登録されている銘柄のリスト


class UnregisterApiResponse(BaseModel):
    RegistList: list[RegistListItem]  # 現在登録されている銘柄のリスト


class UnregisterAllApiResponse(BaseModel):
    RegistList: list[RegistListItem]  # 現在登録されている銘柄のリスト


class WebSocketBidAsk(BaseModel):
    Price: float  # 価格
    Qty: int  # 数量


class WebSocketPushData(BaseModel):
    Symbol: str  # 銘柄コード
    SymbolName: str | None = None  # 銘柄名
    Exchange: int  # 市場コード
    ExchangeName: str | None = None  # 市場名
    CurrentPrice: float | None = None  # 現在値
    CurrentPriceTime: str | None = None  # 現在値時刻
    CurrentPriceChangeStatus: str | None = None  # 現在値前値比較
    CurrentPriceStatus: int | None = None  # 現在値ステータス
    CalcPrice: float | None = None  # 計算用現在値
    PreviousClose: float | None = None  # 前日終値
    PreviousCloseTime: str | None = None  # 前日終値日付
    ChangePreviousClose: float | None = None  # 前日比
    ChangePreviousClosePer: float | None = None  # 前日比（%）
    OpeningPrice: float | None = None  # 始値
    OpeningPriceTime: str | None = None  # 始値時刻
    HighPrice: float | None = None  # 高値
    HighPriceTime: str | None = None  # 高値時刻
    LowPrice: float | None = None  # 安値
    LowPriceTime: str | None = None  # 安値時刻
    TradingVolume: float | None = None  # 売買高
    TradingVolumeTime: str | None = None  # 売買高時刻
    VWAP: float | None = None  # VWAP
    TradingValue: float | None = None  # 売買代金
    BidQty: float | None = None  # 買い数量（最良気配）
    BidPrice: float | None = None  # 買い値段（最良気配）
    BidTime: str | None = None  # 買い時刻（最良気配）
    BidSign: str | None = None  # 買い気配値表示色
    MarketOrderSellQty: float | None = None  # 売り成行数量
    Sell1: WebSocketBidAsk | None = None  # 売気配数量1
    Sell2: WebSocketBidAsk | None = None  # 売気配数量2
    Sell3: WebSocketBidAsk | None = None  # 売気配数量3
    Sell4: WebSocketBidAsk | None = None  # 売気配数量4
    Sell5: WebSocketBidAsk | None = None  # 売気配数量5
    Sell6: WebSocketBidAsk | None = None  # 売気配数量6
    Sell7: WebSocketBidAsk | None = None  # 売気配数量7
    Sell8: WebSocketBidAsk | None = None  # 売気配数量8
    Sell9: WebSocketBidAsk | None = None  # 売気配数量9
    Sell10: WebSocketBidAsk | None = None  # 売気配数量10
    AskQty: float | None = None  # 売り数量（最良気配）
    AskPrice: float | None = None  # 売り値段（最良気配）
    AskTime: str | None = None  # 売り時刻（最良気配）
    AskSign: str | None = None  # 売り気配値表示色
    MarketOrderBuyQty: float | None = None  # 買い成行数量
    Buy1: WebSocketBidAsk | None = None  # 買気配数量1
    Buy2: WebSocketBidAsk | None = None  # 買気配数量2
    Buy3: WebSocketBidAsk | None = None  # 買気配数量3
    Buy4: WebSocketBidAsk | None = None  # 買気配数量4
    Buy5: WebSocketBidAsk | None = None  # 買気配数量5
    Buy6: WebSocketBidAsk | None = None  # 買気配数量6
    Buy7: WebSocketBidAsk | None = None  # 買気配数量7
    Buy8: WebSocketBidAsk | None = None  # 買気配数量8
    Buy9: WebSocketBidAsk | None = None  # 買気配数量9
    Buy10: WebSocketBidAsk | None = None  # 買気配数量10
    OverSellQty: float | None = None  # 売買高加重平均価格(VWAP)
    UnderBuyQty: float | None = None  # 売買高加重平均価格(VWAP)
    TotalMarketValue: float | None = None  # 時価総額
    SecurityType: int | None = None  # 商品種別
