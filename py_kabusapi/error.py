from enum import Enum


class RequestCheckError(Enum):
    INTERNAL_ERROR = (
        4001001,
        "内部エラー",
        "kabuSログファイルを確認してください。",
    )
    TRIGGER_KEY_GENERATION_ERROR = (
        4001002,
        "トリガキー生成エラー",
        "kabuSログファイルを確認してください。",
    )
    ERROR_U_TURN = (
        4001003,
        "エラー：Uターン",
        "kabuSログファイルを確認してください。",
    )
    TRIGGER_GENERATION_ERROR = (
        4001004,
        "トリガ生成エラー",
        "kabuSログファイルを確認してください。",
    )
    PARAMETER_CONVERSION_ERROR = (
        4001005,
        "パラメータ変換エラー",
        "設定したパラメータはkabuステーション「システム設定」「注文１」の設定内容と相違がないかを確認してください。",
    )
    API_EXECUTION_COUNT_ERROR = (
        4001006,
        "API実行回数エラー",
        "",
    )
    LOGIN_AUTHENTICATION_ERROR = (
        4001007,
        "ログイン認証エラー",
        "kabuステーションにログインしているかを確認してください。",
    )
    API_UNAVAILABLE = (
        4001008,
        "API利用不可",
        "API利用設定が完了しているかを確認してください。",
    )
    API_KEY_MISMATCH = (
        4001009,
        "APIキー不一致",
        "",
    )
    INVALID_QUERY_STRING = (
        4001010,
        "クエリ文字列不正",
        "",
    )
    INVALID_REQUEST_STRING = (
        4001011,
        "リクエスト文字列不正",
        "",
    )
    INVALID_REQUEST = (
        4001012,
        "リクエスト不正",
        "",
    )
    TOKEN_ACQUISITION_FAILED_INVALID_API_PASSWORD = (
        4001013,
        "トークン取得失敗：kabuステーションがログインしている状態で、APIパスワードが不正",
        "",
    )
    UNAUTHORIZED_HTTP_METHOD = (
        4001014,
        "許可されていないHTTPメソッド",
        "",
    )
    CONTENT_LENGTH_EXCEEDS = (
        4001015,
        "ContentLength超過",
        "",
    )
    UNSUPPORTED_MEDIA_TYPE = (
        4001016,
        "サポートされていないメディアタイプ",
        "",
    )
    LOGIN_AUTHENTICATION_ERROR_NOT_LOGGED_IN = (
        4001017,
        "ログイン認証エラー：kabuSステーション未ログイン状態。",
        "",
    )
    SYMBOL_REGISTRATION_FAILED = (
        4001018,
        "銘柄が登録できませんでした",
        "登録銘柄上限数（50銘柄）以上の銘柄をリクエストしていないかを確認してください。",
    )
    SOME_SYMBOLS_REGISTRATION_FAILED = (
        4001019,
        "一部の銘柄が登録できませんでした",
        "登録銘柄上限数（50銘柄）以上の銘柄をリクエストしていないかを確認してください。",
    )
    SYMBOL_CANCELLATION_FAILED = (
        4001020,
        "銘柄が解除できませんでした",
        "銘柄が登録されているかを確認してください。",
    )
    SOME_SYMBOLS_CANCELLATION_FAILED = (
        4001021,
        "一部の銘柄が解除できませんでした",
        "登録銘柄上限数（50銘柄）以上の銘柄をリクエストしていないかを確認してください。",
    )
    SYMBOL_NOT_FOUND = (
        4002001,
        "銘柄が見つからない",
        "",
    )
    EXECUTION_CONDITION_ERROR_1 = (
        4002002,
        "執行条件エラー",
        "FrontOrderTypeを確認してください。",
    )
    EXECUTION_CONDITION_ERROR_2 = (
        4002003,
        "執行条件エラー",
        "FrontOrderTypeを確認してください。",
    )
    TRIGGER_CHECK_ERROR = (
        4002004,
        "トリガチェックエラー - 詳細はkabuSログファイルを確認してください",
        "",
    )
    PRODUCT_ERROR = (
        4002005,
        "商品エラー",
        "",
    )
    REGISTER_COUNT_ERROR = (
        4002006,
        "レジスト数エラー",
        "登録銘柄上限数（50銘柄）以上の銘柄をリクエストしていないかを確認してください。",
    )
    INVALID_PARAMETER_ACCOUNT_TYPE = (
        4002007,
        "パラメータ不正：AccountType",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_SIDE = (
        4002008,
        "パラメータ不正：Side",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_CASH_MARGIN = (
        4002009,
        "パラメータ不正：CashMargin",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_DELIV_TYPE = (
        4002010,
        "パラメータ不正：DelivType",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_FUND_TYPE = (
        4002011,
        "パラメータ不正：FundType",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_FRONT_ORDER_TYPE = (
        4002012,
        "パラメータ不正：FrontOrderType",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_MARGIN_TRADE_TYPE = (
        4002013,
        "パラメータ不正：MarginTradeType",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_TIME_IN_FORCE = (
        4002014,
        "パラメータ不正：TimeInForce",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_REPAYMENT_ORDER_AND_DESIGNATION_MUTUALLY_EXCLUSIVE = (
        4002015,
        "パラメータ不正：返済順指定と返済指定は同時に設定できない",
        "",
    )
    INVALID_PARAMETER_DELIV_TYPE_2 = (
        4002016,
        "パラメータ不正：DelivType",
        "詳細はkabuSログファイルを確認してください",
    )
    INVALID_PARAMETER_PRICE_DESIGNATION_ERROR = (
        4002017,
        "パラメータ不正：値段指定エラー",
        "",
    )
    INVALID_PARAMETER_NOT_IOC_ELIGIBLE_SYMBOL = (
        4002018,
        "パラメータ不正：IOC対象銘柄ではない",
        "詳細はkabuSログファイルを確認してください",
    )
    TRANSACTION_DATE_EXCEEDED_OR_INVALID_SYMBOL = (
        4002021,
        "取引期日を過ぎた取引であるか、有効な銘柄ではないため取引できません",
        "",
    )
    ONE_SHOT_AMOUNT_ERROR = (
        4003001,
        "ワンショット：金額エラー",
        "",
    )
    ONE_SHOT_QUANTITY_ERROR = (
        4003002,
        "ワンショット：数量エラー",
        "",
    )
    NO_MATCHING_ORDER_ERROR = (
        4004001,
        "該当注文なしエラー",
        "",
    )
    CANCELLATION_NOT_POSSIBLE = (
        4004002,
        "取消不可",
        "",
    )
    RANKING_ACQUISITION_ERROR = (
        4005001,
        "ランキング取得エラー",
        "",
    )
    EXCHANGE_RATE_INFO_ACQUISITION_ERROR = (
        4005002,
        "為替情報取得エラー",
        "",
    )
    REGULATION_INFO_ACQUISITION_ERROR = (
        4005003,
        "規制情報取得エラー",
        "",
    )

    def __init__(self, code: int, message: str, description: str):
        self.code = code
        self.message = message
        self.description = description

    def __str__(self):
        return f"Code: {self.code}, Message: {self.message}, Description: {self.description}"

    @classmethod
    def from_code(cls, code: int):
        for member in cls:
            if member.code == code:
                return member

        raise ValueError(
            f"No RequestCheckError found for code: {code}",
        )


class OrderPlacementError(Enum):
    NORMAL_TERMINATION = (
        0,
        "正常終了コード",
        "システム上正常終了コード",
    )
    ABNORMAL_TERMINATION = (
        -1,
        "異常終了コード",
        "システム上異常終了コード",
    )
    ACCOUNT_NUMBER_NOT_EXIST = (
        2,
        "口座番号未存在エラー",
        "口座番号が未設定の場合、口座マスタに該当口座情報が存在しない場合",
    )
    ORDER_EXPIRATION_INVALID = (
        5,
        "注文有効期限不正エラー",
        "指定した注文有効期限が有効な日付でない場合、場の切り替わりにより取引日付が変更された場合",
    )
    REPAYMENT_POSITION_INFO_INVALID = (
        8,
        "返済建玉情報不正エラー",
        "返済時の建玉情報(数量、売買区分)に誤りがある場合",
    )
    SYMBOL_INFO_INVALID = (
        11,
        "銘柄情報不正エラー",
        "銘柄マスタに未存在、もしくは銘柄に対する有効期限、取引期限が有効でない場合。現物商品で、銘柄コードが4桁、もしくは5桁で末尾が「5or9」の銘柄でない場合",
    )
    FUTURES_EVENING_SESSION_DATE_ERROR = (
        12,
        "先物夕場取引日付エラー",
        "派生商品の夕場取引日付が有効でない場合",
    )
    TRADE_QUANTITY_UNIT_ERROR = (
        15,
        "取引数量単位エラー",
        "各市場における銘柄の取引数量単位に誤りがある場合",
    )
    TRADE_QUANTITY_INVALID = (
        16,
        "取引数量不正エラー",
        "指定取引数量が0以下の場合、Uターン子注文で親注文と数量が不一致の場合",
    )
    QUOTE_INVALID = (
        17,
        "呼値不正エラー",
        "指定された値段の呼値が不正である場合",
    )
    PRICE_RANGE_ERROR = (
        18,
        "制限値幅エラー",
        "値幅の上限又は下限が制限値幅を超えている場合",
    )
    TRADE_PRICE_INVALID = (
        19,
        "取引値段不正エラー",
        "指定取引値段が0より小さい、不成注文で0を指定した場合。先物取引の値段種別を指値指定に関わらず値段が指定されていない場合",
    )
    AVAILABLE_AMOUNT_INVALID = (
        21,
        "可能額不正エラー",
        "各商品発注時における余力に不足がある場合",
    )
    MARGIN_TRADE_INFO_INVALID = (
        26,
        "信用取引情報不正エラー",
        "信用取引の設定値に誤りがある場合。一般信用、制度信用時に銘柄における売買規制がある場合",
    )
    ACCOUNT_TYPE_INVALID = (
        32,
        "口座種別不正エラー",
        "一般、特定、総合課税のみの種別以外を指定した場合。法人口座、もしくは先物取引で総合課税以外を指定した場合",
    )
    EXCHANGE_DUPLICATE_TELEGRAM_ERROR = (
        38,
        "取引所重複電文エラー",
        "取引所から重複する電文を受信した場合",
    )
    SPECIFIED_ORDER_NOT_EXIST = (
        41,
        "指定注文未存在エラー",
        "存在しない注文を指定した場合",
    )
    SPECIFIED_ORDER_EXPIRED = (
        42,
        "指定注文有効期限切れエラー",
        "有効期限が過ぎた注文を指定した場合",
    )
    SPECIFIED_ORDER_EXECUTED = (
        43,
        "指定注文約定済エラー",
        "約定済の注文を指定した場合",
    )
    SPECIFIED_ORDER_DETAIL_NOT_EXIST = (
        44,
        "指定注文明細未存在エラー",
        "存在しない注文明細を指定した場合",
    )
    POSITION_REPAYMENT_DATE_EXCEEDED = (
        45,
        "建玉返済期日超過エラー",
        "建玉の返済期日が超過している場合",
    )
    SPECIFIED_ORDER_FINISHED = (
        47,
        "指定注文終了済エラー",
        "終了済の注文を指定した場合",
    )
    CORRECTION_CONTENT_INVALID = (
        49,
        "訂正内容不正エラー",
        "訂正項目がない場合、削減数量が注文数量を上回っている場合、寄成、引成を指値に訂正しようとした場合、寄指、引指、不成を成行に訂正しようとした場合、派生商品で値段種別と値段が合致していない訂正をしようとした場合、派生商品で執行条件の訂正をしようとした場合、時間指定Ｗ指値、Uターン注文、リレー注文で数量を削減しようとした場合、動的値段の値段を指値に訂正しようとした場合、IOC注文を訂正しようとした場合",
    )
    TRIGGER_CORRECTION_ERROR = (
        50,
        "トリガ訂正エラー",
        "ヒット済のトリガを訂正しようとした場合",
    )
    CANCELLATION_REQUESTED_ERROR = (
        60,
        "取消依頼済エラー",
        "取消依頼済の注文に対して再度取消依頼をしようとした場合",
    )
    CHILD_ORDER_ACCEPTANCE_ERROR = (
        105,
        "子注文受付エラー",
        "リレー注文、Uターン注文で親注文終了済の場合の子注文受付時。Uターン注文で親注文が一部出来していた場合の子注文受付時",
    )
    SHORT_SELLING_ERROR = (
        108,
        "空売りエラー",
        "成行、不成、動的値段における51単元以上の発注受付時",
    )
    TRADE_CATEGORY_ERROR = (
        109,
        "売買区分エラー",
        "売もしくは買以外の売買区分を指定した場合",
    )
    SELF_BROKERAGE_CATEGORY_ERROR = (
        110,
        "自己委託区分エラー",
        "自己もしくは委託以外の自己委託区分を指定した場合",
    )
    ORDER_ATTRIBUTE_CATEGORY_ERROR = (
        111,
        "注文属性区分エラー",
        "手動もしくは自動以外の注文属性区分を指定した場合",
    )
    EXECUTION_CONDITION_ERROR_3 = (
        112,
        "執行条件エラー",
        "派生商品でザラバ、対当指値以外を選択した場合。IOC注文で株式以外を選択した場合",
    )
    MORNING_SESSION_SPECIFICATION_ERROR = (
        113,
        "前場指定エラー",
        "前場引けで本日前場を指定した場合。後場で本日前場を指定した場合",
    )
    PRICE_RANGE_AUTO_ADJUSTMENT_ERROR = (
        114,
        "値幅自動調整エラー",
        "成行注文時に値幅自動調整を指定した場合。トレーリングストップ、時間指定注文時に値幅自動調整を指定した場合",
    )
    CABU_CALL_ID_INVALID = (
        115,
        "カブコールID不正エラー",
        "存在しないカブコールIDが指定された場合",
    )
    VALIDITY_PERIOD_TYPE_INVALID = (
        116,
        "有効期間種別不正",
        "派生MO注文でFOK、FAK以外の指定をした場合。指値注文でFOK、FAK、FAS以外の指定をした場合",
    )
    PRICE_INVALID = (
        117,
        "値段不正エラー",
        "対当指値注文で0以外の値段を指定した場合。成行値段種別で0以外の値段を指定した場合",
    )
    VALID_SESSION_INVALID = (
        118,
        "有効セッション不正",
        "派生注文の日中注文で1と指定されていない場合。派生注文の夕場注文で2と指定されていない場合。派生注文の日通し注文で0と指定されていない場合",
    )
    PRICE_TYPE_INVALID = (
        119,
        "値段種別不正",
        "値段が成行で成行値段種別が指定されていない場合。値段が指値で指値値段種別が指定されていない場合",
    )
    DYNAMIC_PRICE_SETTING_INVALID = (
        120,
        "動的値段設定不正",
        "動的値段発注時、値段が未決定であった場合",
    )
    MARKET_ORDER_PLACEMENT_INVALID = (
        121,
        "成行発注不正",
        "基準値不定の場合に成行指定をした場合",
    )
    CORRECTION_QUANTITY_CHECK_ERROR = (
        122,
        "訂正数量チェックエラー",
        "訂正時の残数量と取引所の残数量が一致しない場合",
    )
    AUTO_ORDER_NOT_POSSIBLE = (
        123,
        "自動注文不可エラー",
        "市場に「SOR」を指定し、自動注文を行った場合",
    )
    AUTHENTICATION_UPDATE_FAILED = (
        10016,
        "認証更新失敗エラー",
        "認証更新に失敗しました。ネットワークの状態を確認の上、再接続してください。",
    )
    AVAILABLE_AMOUNT_RETURN_VALUE_ERROR = (
        10017,
        "可能額戻り値エラー",
        "可能額の戻り値が異常終了だった場合",
    )
    PLACEMENT_OUTSIDE_ZARABA_ERROR = (
        10020,
        "ザラバ以外での発注エラー",
        "個別株OPの成行をザラバ以外で発注しようとした場合。派生のFOK、対当指値をザラバ以外で発注しようとした場合",
    )
    DELIVERY_METHOD_INVALID = (
        100001,
        "受渡方法不正エラー",
        "現物買で受渡区分が指定されていない場合。信用・派生新規注文で受渡区分が指定されている場合。信用・派生返済注文で受渡区分が指定されていない場合",
    )
    AUTO_DEBIT_SELECTION_ERROR_1 = (
        100002,
        "自動引落選択エラー",
        "現物・信用代用指定注文で受渡方法を自動と選択していた場合",
    )
    AUTO_DEBIT_SELECTION_ERROR_2 = (
        100003,
        "自動引落選択エラー",
        "現物・証拠金代用指定注文で受渡方法を自動と選択していた場合",
    )
    AUTO_DEBIT_SELECTION_ERROR_3 = (
        100004,
        "自動引落選択エラー",
        "自動引き落とし未設定で自動引落を選択した場合",
    )
    FEE_CODE_INVALID = (
        100029,
        "手数料コード不正エラー",
        "発注時に存在しない手数料コードを設定した場合",
    )
    DEPOSIT_CATEGORY_ERROR = (
        100031,
        "預り区分エラー",
        "現物取引で保護、信用代用、証拠金代用以外の預り区分を選択した場合。信用取引で信用取引以外の預り区分を選択した場合。先物取引で預り区分を選択した場合",
    )
    COMPLIANCE_ERROR = (
        100033,
        "コンプライアンスエラー",
        "コンプライアンス制限のある銘柄を発注した場合。コンプライアンス制限のある口座で発注した場合",
    )
    HARD_LIMIT_ERROR = (
        100051,
        "ハードリミットエラー",
        "ハードリミット制限を越える発注をした場合",
    )
    DERIVATIVE_POSITION_LIMIT_EXCEEDED = (
        100052,
        "派生建玉枚数制限エラー",
        "派生商品で建玉枚数上限を超える発注を行った場合",
    )
    MARGIN_POSITION_LIMIT_EXCEEDED = (
        100053,
        "信用建玉枚数制限エラー",
        "信用取引で建玉枚数上限を超える発注を行った場合",
    )
    AGREEMENT_NOT_READ_ERROR = (
        100202,
        "約諾書未読エラー",
        "現物取引時、最良執行市場同意書の手続きをしていない場合、現物取引時、上場有価証券同意書の手続きをしていない場合、信用取引時、再担保同意書の手続きをしていない場合、信用取引時、信用契約締結同意書の手続きをしていない場合、派生取引時、派生契約締結同意書の手続きをしていない場合",
    )
    SPECIFIC_ACCOUNT_DESIGNATION_ERROR = (
        100203,
        "特定口座指定エラー",
        "特定口座の申し込みをしていない場合に特定口座を選択した場合",
    )
    MARGIN_TRADE_DESIGNATION_ERROR = (
        100204,
        "信用取引指定エラー",
        "現物取引時、信用取引手続きをしておらず、信用代用預り区分選択した場合。信用取引時、信用取引手続きをしておらず、信用代用預り区分選択した場合",
    )
    DERIVATIVE_TRADE_DESIGNATION_ERROR = (
        100205,
        "派生取引指定エラー",
        "現物取引時、派生取引手続きをしておらず、証拠金代用預り区分選択した場合。派生取引時、派生口座同意書の手続きをしていない場合",
    )
    INSIDER_ERROR = (
        100206,
        "インサイダエラー",
        "内部者取引を行う場合",
    )
    ADVANCE_PAYMENT_OCCURRED_ERROR = (
        100207,
        "立替金発生エラー",
        "新規取引時、立替金が発生している場合",
    )
    ADDITIONAL_MARGIN_OCCURRED_ERROR = (
        100208,
        "追証発生エラー",
        "信用新規取引時、追証が発生している場合",
    )
    MARGIN_SHORTAGE_OCCURRED_ERROR = (
        100209,
        "保証金不足発生エラー",
        "新規取引時、保証金不足が発生している場合",
    )
    SAME_DAY_CASH_STOCK_TRADE_CATEGORY_ERROR = (
        100211,
        "即金銘柄取引区分エラー",
        "即日現金預託規制銘柄取引で信用代用、証拠金代用を選択した場合。即日現金預託規制銘柄取引で自動引落を選択した場合",
    )
    PTS_LENDING_STOCK_TRADE_ERROR = (
        100212,
        "PTS貸株取引エラー",
        "貸株がある場合の16:00以降のPTS取引を行おうとした場合",
    )
    MAX_SETTLEMENT_COUNT_ERROR = (
        100213,
        "最大決済件数エラー",
        "返済注文時最大決済件数を超えた取引を行おうとした場合",
    )
    SAME_DAY_CASH_STOCK_CORRECTION_ERROR = (
        100215,
        "即金銘柄訂正エラー",
        "即日現金預託規制銘柄への訂正を行おうとした場合",
    )
    ONE_SHOT_LIMIT_ERROR = (
        100216,
        "ワンショット制限エラー",
        "ワンショット制限枚数を超えた発注を行おうとした場合",
    )
    INSTANT_BINGO_ERROR = (
        100217,
        "即ビンゴエラー",
        "値段トリガ注文で即座に発注する条件の発注を行おうとした場合",
    )
    W_LIMIT_CONDITION_DESIGNATION_ERROR = (
        100218,
        "W指値条件指定エラー",
        "W指値買注文で「以下」が指定されていた場合。W指値買注文で「以上」が指定されていた場合",
    )
    RELAY_CONDITION_INVALID = (
        100220,
        "リレー条件不正エラー",
        "親注文が時間指定注文のリレー子注文の場合",
    )
    PLUS_MINUS_LIMIT_CORRECTION_ERROR = (
        100221,
        "±指値訂正エラー",
        "親注文もしくは該当注文が±指値で訂正を行おうとした場合",
    )
    U_TURN_CHILD_ORDER_MULTIPLE_ERROR = (
        100222,
        "Uターン子注文複数エラー",
        "Uターン親注文に２つ以上の子注文をつけようとした場合",
    )
    STOCK_OPTION_AGREEMENT_ERROR = (
        100223,
        "新株予約権証券同意書エラー",
        "新株予約権証券同意書を未読のまま新規上場銘柄の発注を行おうとした場合",
    )
    PTS_AGREEMENT_ERROR = (
        100224,
        "PTS同意書エラー",
        "PTS同意書を未読のままPTSの発注を行おうとした場合",
    )
    MARGIN_TRADE_REGULATION_ERROR = (
        100225,
        "信用取引規制エラー",
        "信用取引規制中に信用新規発注を行おうとした場合。信用取引規制中に先物新規発注を行おうとした場合。一般信用売建取引においてnMarginSellCapFlagが指定されていない場合",
    )
    FOREIGN_SECURITIES_TRADE_REGULATION_ERROR = (
        100226,
        "外国証券取引規制エラー",
        "外国証券取引規制口座で外国株発注を行おうとした場合",
    )
    TRAILING_STOP_REGULATION_ERROR_1 = (
        100230,
        "トレーリングストップ規制エラー",
        "PTSへトレーリングストップ注文を行おうとした場合",
    )
    TRAILING_STOP_REGULATION_ERROR_2 = (
        100231,
        "トレーリングストップ規制エラー",
        "権利落日にトレーリングストップ注文を発注した際、始値未決定の場合",
    )
    TRAILING_STOP_CONDITION_ERROR = (
        100232,
        "トレーリングストップ条件エラー",
        "トレーリングストップ買注文で安値が決まっていない場合、トレーリングストップ買注文で「トリガ値段 < 現値 - 安値 + 呼値×2」を満たす発注の場合、トレーリングストップ売注文で高値が決まっていない場合、トレーリングストップ売注文で「絶対値(トリガ値段) < 高値 - 現値 + 呼値×2」を満たす発注の場合",
    )
    REQUIRED_MARGIN_NOT_CALCULATED_ERROR = (
        100233,
        "必要証拠金未算出エラー",
        "必要証拠金が算出されていない銘柄に対する発注を行おうとした場合",
    )
    CORRECTION_MAX_SETTLEMENT_COUNT_ERROR = (
        100234,
        "訂正時最大決済件数エラー",
        "返済注文訂正時最大決済件数を超えた取引を行おうとした場合",
    )
    TIME_DESIGNATED_ORDER_OUT_OF_TRADE_HOURS_1 = (
        100240,
        "時間指定注文取引時間外エラー",
        "時間指定注文を取引時間外で発注した場合",
    )
    MARKET_CLOSE_ERROR = (
        100244,
        "場引けエラー",
        "発注時に場が引けてしまった場合",
    )
    PLACEMENT_OUTSIDE_ZARABA_ERROR_2 = (
        100246,
        "ザラバ以外での発注エラー",
        "IOC取引で立会い中以外で発注を行おうとした場合",
    )
    OMX_TRANSITION_TRADE_REGULATION_ERROR = (
        100247,
        "OMX移行時取引規制エラー",
        "OMX移行時に制限された有効期限以上の発注を行おうとした場合",
    )
    TIME_DESIGNATED_ORDER_OUT_OF_TRADE_HOURS_2 = (
        100250,
        "時間指定注文取引時間外エラー",
        "相対時間指定注文を営業日以外に発注した場合",
    )
    TIME_DESIGNATED_ORDER_OUT_OF_TRADE_HOURS_3 = (
        100251,
        "時間指定注文取引時間外エラー",
        "時間指定指値・成行注文が「引け後-30分」～「引け時刻」範囲外の指定であった場合",
    )
    TIME_DESIGNATED_ORDER_TIME_ERROR_1 = (
        100252,
        "時間指定注文指定時刻エラー",
        "時間指定指値・成行注文で現在時刻より小さい時間を指定した場合",
    )
    TIME_DESIGNATED_ORDER_TIME_ERROR_2 = (
        100253,
        "時間指定注文指定時刻エラー",
        "時間指定指値・成行注文で現在時刻から10分より小さい時間を指定した場合",
    )
    TIME_DESIGNATED_ORDER_TIME_ERROR_3 = (
        100254,
        "時間指定注文指定時刻エラー",
        "時間指定指値・成行注文の指定時刻で立会い終了前30分から終了までの時間を指定した場合",
    )
    TIME_DESIGNATED_ORDER_TIME_ERROR_4 = (
        100255,
        "時間指定注文指定時刻エラー",
        "時間指定指値・成行注文の指定時刻で引け後の時間を指定した場合",
    )
    TIME_DESIGNATED_ORDER_TIME_ERROR_5 = (
        100256,
        "時間指定注文指定時刻エラー",
        "時間指定指値・成行注文の指定時刻が立会開始から10分の間の時間を指定した場合",
    )
    TIME_DESIGNATED_CORRECTION_LIMIT_ORDER_TIME_ERROR_1 = (
        100257,
        "時間指定訂正付き指値注文指定時刻エラー",
        "時間指定訂正付き指値注文が「引け後-30分」～「引け時刻」範囲外の指定であった場合",
    )
    TIME_DESIGNATED_CORRECTION_LIMIT_ORDER_TIME_ERROR_2 = (
        100258,
        "時間指定訂正付き指値注文指定時刻エラー",
        "時間指定訂正付き指値注文が引け後の指定であった場合",
    )
    TIME_DESIGNATED_CANCELLATION_LIMIT_ORDER_TIME_ERROR_1 = (
        100259,
        "時間指定取消付き指値注文指定時刻エラー",
        "時間指定取消付き指値注文が「引け後-30分」～「引け時刻」範囲外の指定であった場合",
    )
    TIME_DESIGNATED_CANCELLATION_LIMIT_ORDER_TIME_ERROR_2 = (
        100260,
        "時間指定取消付き指値注文指定時刻エラー",
        "時間指定取消付き指値注文が引け後の指定であった場合",
    )
    TIME_DESIGNATED_W_LIMIT_ORDER_TIME_ERROR_1 = (
        100261,
        "時間指定W指値注文指定時刻エラー",
        "時間指定W指値注文が「引け後-30分」～「引け時刻」範囲外の指定であった場合",
    )
    TIME_DESIGNATED_W_LIMIT_ORDER_TIME_ERROR_2 = (
        100262,
        "時間指定W指値注文指定時刻エラー",
        "時間指定W指値注文が引け後の指定であった場合",
    )
    GENERAL_MARGIN_CAP_EXCEEDED_ERROR = (
        100263,
        "一般信用キャップ付き残数超過エラー",
        "一般信用キャップ付き残数を超える発注を行った場合",
    )
    GENERAL_MARGIN_CAP_VALIDITY_PERIOD_ERROR = (
        100265,
        "一般信用キャップ付き有効期限エラー",
        "一般信用キャップ付き発注で当日より先の有効期限を設定した場合",
    )
    SHORT_SELLING_REGULATION_SYMBOL_MARGIN_NEW_SELL_ORDER_UNIT_EXCEEDED_ERROR = (
        100266,
        "空売り規制銘柄信用新規売注文単元超過エラー",
        "信用新規売発注で空売り最大単元数を超過した場合",
    )
    INELIGIBLE_SUBSTITUTION_SYMBOL_ORDER_ERROR = (
        100267,
        "代用不適格銘柄発注エラー",
        "代用不適格銘柄の代用指定注文を行おうとした場合",
    )
    SAME_DAY_CASH_SYMBOL_VALIDITY_PERIOD_ERROR = (
        100268,
        "即金銘柄有効期限エラー",
        "即日現金預託規制銘柄へ当日より先の有効期限を設定して発注を行った場合",
    )
    SAME_DAY_CASH_SYMBOL_PRICE_TYPE_ERROR = (
        100269,
        "即金銘柄値段種別エラー",
        "即日現金預託規制銘柄へ成行の値段種別を設定して発注を行った場合",
    )
    NIKKEI_VI_FUTURES_ORDER_MARKET_ERROR = (
        100270,
        "日経VI先物発注場エラー",
        "日経VI先物発注を日中以外の場を指定して発注を行った場合",
    )
    GENERAL_MARGIN_DATE_DESIGNATION_ERROR = (
        100271,
        "一般信用期日指定エラー",
        "一般信用銘柄が長期である場合に短期で発注した場合。一般信用銘柄が短期である場合に長期で発注した場合",
    )
    ORGANIZED_STOCK_NEW_ORDER_ERROR = (
        100272,
        "整理銘柄新規発注エラー",
        "整理銘柄を新規取引として発注した場合",
    )
    RIGHTS_ADJUSTMENT_DAY_OR_LATER_ORDER_ERROR = (
        100273,
        "権利修正前日以降発注エラー",
        "権利修正前日以降の有効期限を指定して発注した場合",
    )
    OUT_OF_ACCEPTANCE_TIME_LOTTERY_SYMBOL = (
        100274,
        "受付時間外(抽選銘柄)",
        "信用抽選銘柄を受付時間外に発注した場合",
    )
    FRONT_CHANNEL_ID_INVALID = (
        100282,
        "FrontChannelID不正",
        "NISA発注不可チャネルからのNISAの発注",
    )
    ORDER_LIMIT_ERROR = (
        100294,
        "注文上限エラー",
        "注文内容が当社所定の注文上限を超えている",
    )
    INSIDER_REGISTERED_SYMBOL_ERROR = (
        100295,
        "内部者登録銘柄エラー",
        "内部者登録銘柄の発注",
    )
    DAY_TRADE_MARGIN_EXECUTION_CONDITION_ERROR = (
        100301,
        "デイトレ信用の執行条件エラー",
        "デイトレ信用では、この執行条件は指定できません",
    )
    SELL_RESTRICTED_SYMBOL_ERROR = (
        100302,
        "売建規制銘柄エラー",
        "売建規制銘柄の為、受付することができません",
    )
    PREMIUM_FEE_ERROR_1 = (
        100303,
        "プレミアム料エラー",
        "一般信用売り建のプレミアム料が変更になりました。再度、発注をお願いいたします",
    )
    PREMIUM_FEE_ERROR_2 = (
        100304,
        "プレミアム料エラー",
        "一般信用売り建のプレミアム料が変更になりました。再度、発注をお願いいたします",
    )
    PREMIUM_FEE_ERROR_3 = (
        100305,
        "プレミアム料エラー",
        "プレミアム料の金額をご確認ください",
    )
    PREMIUM_FEE_TICK_ERROR = (
        100306,
        "プレミアム料エラー",
        "プレミアム料の刻値が不正です",
    )
    MARGIN_BUY_CORRECTION_ORDER_ACCEPTANCE_ERROR = (
        100307,
        "信用買の訂正注文受付エラー",
        "現在、信用取引の買い新規の注文に対して注文価格を上げる訂正注文の受付を停止しております。注文価格を上げたい場合は、注文を一度取り消していただき、新規のご注文として発注をお願いします",
    )
    MARGIN_BUY_TIME_DESIGNATED_W_LIMIT_ORDER_ACCEPTANCE_ERROR_1 = (
        100308,
        "信用買の時間指定注文・W指値注文受付エラー",
        "現在、信用取引の買い新規の注文では時間指定注文ならびにW指値注文の受付を停止しております。時間指定注文ならびにW指値注文以外の注文は通常通り受付しておりますので時間指定注文ならびにW指値注文以外での発注をお願いします",
    )
    MARGIN_BUY_TIME_DESIGNATED_W_LIMIT_ORDER_ACCEPTANCE_ERROR_2 = (
        100309,
        "信用買の時間指定注文・W指値注文受付エラー",
        "現在、信用取引の買い新規の時間指定注文ならびにW指値注文は、新規・訂正ともに受付を停止しております。時間指定注文ならびにW指値注文の内容を訂正したい場合は、注文を一度取り消していただき、新規のご注文として発注をお願いします",
    )
    MARGIN_BUY_AFTERNOON_SESSION_MARKET_ORDER_ERROR = (
        100310,
        "信用買の後場不成注文エラー",
        "現在、信用取引の買い新規の注文に関して、前場終了までに後場を指定した不成注文の受付を停止しております。不成のご注文の際は前場終了までは前場不成、前場終了後以降後場終了までは後場不成として発注をお願いします",
    )
    FEE_COURSE_CHANGE_ORDER_EXPIRATION_ERROR = (
        100311,
        "手数料コース変更による注文期限エラー",
        "本日、手数料コース変更を申込みされているため、注文期限が翌日以降の注文を受付できません。注文をご希望の際は、注文期限を「当日」にしていただくか、もしくは「手数料コース変更申込」を取消した上で注文をお願いいたします",
    )
    FEE_COURSE_CHANGE_ORDER_TIME_ERROR = (
        100312,
        "手数料コース変更による注文時間エラー",
        "手数料コース変更を申込みされているため、15:00-15:30は注文を受付できません。恐れ入りますが、15:30以降にあらためて注文をお願いいたします。",
    )
    CROSS_TRADE_ORDER_ERROR = (
        100313,
        "クロス取引発注エラー",
        "同一銘柄の買い注文と売り注文を同時に行うご注文は、取引時間中における不公正取引の仮装売買（クロス）に該当する可能性があるため、未約定の反対注文の状況をご確認のうえ、執行条件を変更してください。",
    )
    CROSS_TRADE_CORRECTION_ERROR = (
        100314,
        "クロス取引訂正エラー",
        "同一銘柄の買い注文と売り注文を同時に行うご注文は、取引時間中における不公正取引の仮装売買（クロス）に該当する可能性があるため、未約定の反対注文の状況をご確認のうえ、執行条件を変更してください。",
    )
    QUALIFIED_INSTITUTIONAL_INVESTOR_SHORT_SELLING_ORDER_ERROR = (
        100315,
        "適格機関投資家での空売り注文エラー",
        "適格機関投資家に該当するお客さまは1単位の信用新規売り（空売り）から価格規制が適用されます。空売りの価格規制違反を未然に防止する観点から、成行または成行を含む執行条件でのご注文はお受けできません。",
    )
    QUALIFIED_INSTITUTIONAL_INVESTOR_SHORT_SELLING_CORRECTION_ERROR = (
        100316,
        "適格機関投資家での空売り訂正注文エラー",
        "適格機関投資家に該当するお客さまは1単位の信用新規売り（空売り）から価格規制が適用されます。空売りの価格規制違反を未然に防止する観点から、成行または成行を含む執行条件への訂正はお受けできません。",
    )
    CUMULATIVE_51_UNITS_OR_MORE_SHORT_SELLING_MORNING_SESSION_ERROR = (
        100317,
        "累計51単元以上(前場)の空売り発注エラー",
        "同一銘柄の信用新規売り（空売り）の注文数量合計が50単位を超えるため、空売りの価格規制違反を未然に防止する観点から、成行または成行を含む執行条件でのご注文はお受けできません。",
    )
    CUMULATIVE_51_UNITS_OR_MORE_SHORT_SELLING_AFTERNOON_SESSION_ERROR = (
        100318,
        "累計51単元以上(後場)の空売り発注エラー",
        "同一銘柄の信用新規売り（空売り）の注文数量合計が50単位を超えるため、空売りの価格規制違反を未然に防止する観点から、成行または成行を含む執行条件でのご注文はお受けできません。",
    )
    CUMULATIVE_51_UNITS_OR_MORE_SHORT_SELLING_MORNING_SESSION_CORRECTION_ERROR = (
        100319,
        "累計51単元以上(前場)の空売り訂正エラー",
        "同一銘柄の信用新規売り（空売り）の注文数量合計が50単位を超えるため、空売り価格規制違反を未然に防止する観点から、成行または成行を含む執行条件への訂正はお受けできません。",
    )
    CUMULATIVE_51_UNITS_OR_MORE_SHORT_SELLING_AFTERNOON_SESSION_CORRECTION_ERROR = (
        100320,
        "累計51単元以上(後場)の空売り訂正エラー",
        "同一銘柄の信用新規売り（空売り）の注文数量合計が50単位を超えるため、空売り価格規制違反を未然に防止する観点から、成行または成行を含む執行条件への訂正はお受けできません。",
    )
    ONE_SHOT_51_UNITS_OR_MORE_SHORT_SELLING_ORDER_ERROR = (
        100321,
        "ワンショット51単元以上の空売り発注エラー",
        "適格機関投資家に該当しないお客さまは50単位を超える信用新規売り（空売り）から価格規制が適用されます。空売りの価格規制違反を未然に防止する観点から、成行または成行を含む執行条件でのご注文はお受けできません。",
    )
    ONE_SHOT_51_UNITS_OR_MORE_SHORT_SELLING_CORRECTION_ERROR = (
        100322,
        "ワンショット51単元以上の空売り訂正エラー",
        "適格機関投資家に該当しないお客さまは50単位を超える信用新規売り（空売り）から価格規制が適用されます。空売りの価格規制違反を未然に防止する観点から、成行または成行を含む執行条件への訂正はお受けできません。",
    )
    PREMIUM_FEE_DESIGNATION_RANGE_ERROR = (
        100323,
        "プレミアム料指定範囲エラー",
        "入札プレミアム料は、下限～上限の範囲内で指定してください。",
    )
    PREMIUM_FEE_TICK_RANGE_ERROR = (
        100324,
        "プレミアム料刻値範囲エラー",
        "入札プレミアム料の単位が正しくありません。指定の単位で入力してください。",
    )
    PREMIUM_FEE_TIME_DESIGNATION_ERROR = (
        100325,
        "プレミアム料時間指定エラー",
        "入札受付時間外(19:30～20:30)のため、一般信用売り建のプレミアム料の訂正を受付することができません。",
    )
    ORDER_EXPIRATION_DATE_DESIGNATION_ERROR = (
        100326,
        "注文期限指定エラー",
        "注文期限指定が返済期日を超過しています。",
    )
    ORDER_EXPIRATION_DATE_DESIGNATION_ERROR_AU_MONEY_CONNECT_1 = (
        100330,
        "注文期限指定エラー",
        "auマネーコネクト自動入金サービスの受付時間外です。三菱UFJ eスマート証券買付可能額の範囲で注文いただくか、auマネーコネクト自動入金サービスの受付時間内に再度注文内容をご入力ください。",
    )
    ORDER_EXPIRATION_DATE_DESIGNATION_ERROR_AU_MONEY_CONNECT_2 = (
        100331,
        "注文期限指定エラー",
        "お客さまのauじぶん銀行口座からの引落が失敗したため、注文できませんでした。再度注文内容をご入力ください。",
    )
    ORDER_EXPIRATION_DATE_DESIGNATION_ERROR_AU_MONEY_CONNECT_3 = (
        100332,
        "注文期限指定エラー",
        "お客さまのauじぶん銀行口座からの引落が失敗したため、注文ができませんでした。しばらくたってから再度注文内容をご入力ください。",
    )
    ORDER_EXPIRATION_DATE_DESIGNATION_ERROR_AU_MONEY_CONNECT_4 = (
        100333,
        "注文期限指定エラー",
        "お客さまのauじぶん銀行口座からの引落が失敗したため、注文ができませんでした。しばらくたってから再度注文内容をご入力ください。",
    )
    ORDER_EXPIRATION_DATE_DESIGNATION_ERROR_AU_MONEY_CONNECT_5 = (
        100334,
        "注文期限指定エラー",
        "お客さまのauじぶん銀行口座からの引落が失敗したため、注文ができませんでした。しばらくたってから再度注文内容をご入力ください。",
    )
    ORDER_EXPIRATION_DATE_DESIGNATION_ERROR_AU_MONEY_CONNECT_6 = (
        100335,
        "注文期限指定エラー",
        "auマネーコネクト自動入金サービスはご利用いただけません。kabuステーションを再起動いただくか、受渡方法を他の方法にご変更ください。",
    )
    ORDER_EXPIRATION_DATE_DESIGNATION_ERROR_AU_MONEY_CONNECT_7 = (
        100337,
        "注文期限指定エラー",
        "auマネーコネクト自動入金サービスはご利用いただけません。お客さまサポートセンターまでご連絡ください。",
    )

    def __init__(self, code: int, message: str, description: str):
        self.code = code
        self.message = message
        self.description = description

    def __str__(self):
        return f"Code: {self.code}, Message: {self.message}, Description: {self.description}"

    @classmethod
    def from_code(cls, code: int):
        for member in cls:
            if member.code == code:
                return member

        raise ValueError(
            f"No OrderPlacementError found for code: {code}",
        )
