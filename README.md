# py-kabusapi

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**py-kabusapi**は、三菱UFJ eスマート証券が提供するKabu Station APIのPythonクライアントライブラリです。日本株式市場での取引、口座情報の取得、マーケットデータの取得を簡単に行うことができます。

## 特徴

- 🔐 **認証管理**: APIトークンの自動取得・管理
- 💰 **取引余力取得**: 現物・信用・先物・オプションの余力確認
- 📊 **マーケットデータ**: 板情報・銘柄情報・ランキング情報の取得
- 🔄 **注文管理**: 現物・先物・オプション注文の発注・取消
- 📈 **ポジション管理**: 建玉・注文履歴の確認
- 🐳 **Docker対応**: コンテナ環境での動作をサポート
- 🛡️ **エラーハンドリング**: 包括的なエラーコード管理

## インストール

### uvを使用する場合（推奨）

```bash
uv add py-kabusapi
```

### pipを使用する場合

```bash
pip install py-kabusapi
```

## クイックスタート

### 基本的な使用方法

```python
from py_kabusapi.api import KabuStationAPI

# APIクライアントの初期化
api = KabuStationAPI()

# 認証（APIパスワードが必要）
response = api.token("your_api_password")

if response.api_result_category == 0:  # 成功
    print("認証成功")
    
    # 現物取引余力の取得
    cash_response = api.wallet_cash()
    if cash_response.api_result_category == 0:
        cash_data = cash_response.content
        print(f"現物買付可能額: {cash_data.StockAccountWallet:,.0f}円")
    
    # 銘柄の板情報取得
    board_response = api.board_by_symbol("7203@1")  # トヨタ自動車
    if board_response.api_result_category == 0:
        board_data = board_response.content
        print(f"現在値: {board_data.CurrentPrice}円")
        print(f"前日比: {board_data.ChangePreviousClose:+.0f}円")
else:
    print("認証失敗")
```

### 環境設定

```python
# テスト環境（デフォルト）
api = KabuStationAPI(environment="test")

# 本番環境
api = KabuStationAPI(environment="production")

# Dockerコンテナ内での使用
api = KabuStationAPI(is_in_docker_container=True)

# カスタムホスト
api = KabuStationAPI(host_name="192.168.1.100")
```

## API リファレンス

### 認証

#### `token(api_password: str)`
APIトークンを発行します。発行したトークンは有効である限り使用でき、リクエストごとに発行する必要はありません。

```python
response = api.token("your_api_password")
```

**注意**: トークンは以下のタイミングで無効になります
- kabuステーションを終了した時
- kabuステーションからログアウトした時
- 別のトークンが新たに発行された時

### 取引余力

#### `wallet_cash()`
口座の取引余力（現物）を取得します。

```python
response = api.wallet_cash()
cash_data = response.content
print(f"現物買付可能額: {cash_data.StockAccountWallet}")
```

#### `wallet_cash_by_symbol(symbol: str)`
指定した銘柄の現物取引余力を取得します。

```python
response = api.wallet_cash_by_symbol("7203@1")
```

#### `wallet_margin()`
口座の取引余力（信用）を取得します。

```python
response = api.wallet_margin()
margin_data = response.content
print(f"信用新規可能額: {margin_data.MarginAccountWallet}")
print(f"保証金維持率: {margin_data.DepositkeepRate}%")
```

#### `wallet_margin_by_symbol(symbol: str)`
指定した銘柄の信用取引余力を取得します。

```python
response = api.wallet_margin_by_symbol("7203@1")
```

#### `wallet_future()`
口座の取引余力（先物）を取得します。

```python
response = api.wallet_future()
future_data = response.content
print(f"新規建玉可能額: {future_data.FutureTradeLimit}")
```

#### `wallet_future_by_symbol(symbol: str)`
指定した銘柄の先物取引余力を取得します。

```python
response = api.wallet_future_by_symbol("160060018@23")
```

#### `wallet_option()`
口座の取引余力（オプション）を取得します。

```python
response = api.wallet_option()
option_data = response.content
print(f"買新規建玉可能額: {option_data.OptionBuyTradeLimit}")
print(f"売新規建玉可能額: {option_data.OptionSellTradeLimit}")
```

#### `wallet_option_by_symbol(symbol: str)`
指定した銘柄のオプション取引余力を取得します。

```python
response = api.wallet_option_by_symbol("140248026@23")
```

### 注文管理

#### `sendorder()`
現物株式の注文を発注します。

```python
response = api.sendorder(
    symbol="7203@1",        # 銘柄コード（トヨタ自動車）
    exchange=1,             # 市場コード（東証）
    security_type=1,        # 商品種別（株式）
    side="2",               # 売買区分（買い）
    cash_margin=1,          # 信用区分（現物）
    deliv_type=2,           # 受渡区分（お預り金）
    account_type=4,         # 口座種別（特定）
    qty=100,                # 注文数量
    price=2500.0,           # 注文価格
    expire_day=20241231,    # 注文有効期限
    front_order_type=20     # 執行条件（成行）
)
```

#### `sendorder_future()`
先物銘柄の注文を発注します。

```python
response = api.sendorder_future(
    symbol="160060018@23",  # 日経225先物
    exchange=23,            # 大証
    trade_type=1,           # 新規
    time_in_force=1,        # 当日限り
    side="2",               # 買い
    qty=1,                  # 1枚
    price=28000.0,          # 価格
    expire_day=20241231,    # 有効期限
    front_order_type=20     # 成行
)
```

#### `sendorder_option()`
オプション銘柄の注文を発注します。

```python
response = api.sendorder_option(
    symbol="140248026@23",  # 日経225オプション
    exchange=23,            # 大証
    trade_type=1,           # 新規
    time_in_force=1,        # 当日限り
    side="2",               # 買い
    qty=1,                  # 1枚
    price=100.0,            # 価格
    expire_day=20241231,    # 有効期限
    front_order_type=20     # 成行
)
```

#### `cancelorder(order_id: str)`
注文を取消します。

```python
response = api.cancelorder("20241201-001")
```

### マーケットデータ

#### `board_by_symbol(symbol: str)`
指定した銘柄の時価情報・板情報を取得します。

```python
response = api.board_by_symbol("7203@1")
board_data = response.content
print(f"銘柄名: {board_data.SymbolName}")
print(f"現在値: {board_data.CurrentPrice}円")
print(f"前日比: {board_data.ChangePreviousClose:+.0f}円")
print(f"売買高: {board_data.TradingVolume:,.0f}株")
```

#### `symbol_by_symbol(symbol: str, addinfo: bool = True)`
指定した銘柄の詳細情報を取得します。

```python
response = api.symbol_by_symbol("7203@1", True)
symbol_data = response.content
print(f"銘柄名: {symbol_data.SymbolName}")
print(f"時価総額: {symbol_data.TotalMarketValue:,.0f}円")
print(f"発行済み株式数: {symbol_data.TotalStocks:,.0f}千株")
```

#### `orders()`
注文一覧を取得します。

```python
response = api.orders(
    product="0",           # 全商品
    state="1",            # 待機中
    details="true"        # 詳細情報を含む
)
```

**パラメータ**:
- `product`: 取得する商品 (0: すべて, 1: 現物, 2: 信用, 3: 先物, 4: OP)
- `id`: 注文番号
- `updtime`: 更新日時(yyyyMMddHHmmss)
- `details`: 注文詳細抑止
- `symbol`: 銘柄コード
- `state`: 状態 (1〜5)
- `side`: 売買区分 (1: 売, 2: 買)
- `cashmargin`: 取引区分 (2: 新規, 3: 返済)

#### `positions()`
残高一覧を取得します。

```python
response = api.positions(
    product="0",          # 全商品
    addinfo="true"       # 追加情報を含む
)
```

**パラメータ**:
- `product`: 取得する商品 (0: すべて, 1: 現物, 2: 信用, 3: 先物, 4: OP)
- `symbol`: 銘柄コード
- `side`: 売買区分 (1: 売, 2: 買)
- `addinfo`: 追加情報出力フラグ

#### `ranking(type: str, exchange_division: str)`
各種ランキング情報を取得します。

```python
# 売買高上位ランキング
response = api.ranking("3", "ALL")
```

**ランキング種別**:
- "1": 値上がり率
- "2": 値下がり率  
- "3": 売買高上位
- "4": 売買代金上位
- "5": TICK回数
- "6": 売買高急増
- "7": 売買代金急増
- "8": 信用買残増
- "9": 信用買残減
- "10": 信用売残増
- "11": 信用売残減
- "12": 信用倍率
- "13": 信用貸借倍率
- "14": 業種別値上がり率
- "15": 業種別値下がり率

**市場区分**:
- "ALL": 全市場
- "T": 東証
- "TP": 東証プライム
- "TS": 東証スタンダード
- "TG": 東証グロース
- "M": 名証
- "FK": 福証
- "S": 札証

#### `exchange_by_symbol(symbol: str)`
マネービューの情報（為替レート）を取得します。

```python
response = api.exchange_by_symbol("usdjpy")
```

**対応通貨ペア**:
- "usdjpy", "eurjpy", "gbpjpy", "audjpy", "chfjpy", "cadjpy", "nzdjpy", "zarjpy", "eurusd", "gbpusd", "audusd"

#### `regulations_by_symbol(symbol: str)`
規制情報＋空売り規制情報を取得します。

```python
response = api.regulations_by_symbol("7203@1")
```

#### `primaryexchange_by_symbol(symbol: str)`
株式の優先市場を取得します。

```python
response = api.primaryexchange_by_symbol("7203")
```

#### `apisoftlimit()`
kabuステーションAPIのソフトリミット値を取得します。

```python
response = api.apisoftlimit()
```

#### `margin_marginpremium_by_symbol(symbol: str)`
指定した銘柄のプレミアム料を取得します。

```python
response = api.margin_marginpremium_by_symbol("7203@1")
```

### 先物・オプション銘柄コード取得

#### `symbolname_future(future_code: str, deriv_month: int)`
先物銘柄コードを取得します。

```python
response = api.symbolname_future("NK225", 0)
```

#### `symbolname_option(deriv_month: int, put_or_call: str, strike_price: int, option_code: str)`
オプション銘柄コードを取得します。

```python
response = api.symbolname_option(0, "C", 0, "NK225miniop")
```

#### `symbolname_minioptionweekly(deriv_month: int, deriv_weekly: int, put_or_call: str, strike_price: int)`
ミニオプション（限週）銘柄コードを取得します。

```python
response = api.symbolname_minioptionweekly(0, 0, "C", 0)
```

## エラーハンドリング

py-kabusapiは包括的なエラーハンドリングシステムを提供しています。

### エラーレスポンスの確認

```python
response = api.wallet_cash()

if response.api_result_category == 0:
    # 成功
    data = response.content
    print("取得成功")
elif response.api_result_category == 1:
    # HTTPエラー
    error = response.content
    print(f"HTTPエラー: {error.Code} - {error.Message}")
elif response.api_result_category == 2:
    # APIエラー
    error = response.content
    print(f"APIエラー: {error.ResultCode}")
```

### エラーコードの詳細取得

```python
from py_kabusapi.error import RequestCheckError, OrderPlacementError

# リクエストチェックエラーの詳細
try:
    error_detail = RequestCheckError.from_code(4001007)
    print(f"エラー: {error_detail.message}")
    print(f"対処法: {error_detail.description}")
except ValueError:
    print("未知のエラーコードです")

# 注文エラーの詳細
try:
    error_detail = OrderPlacementError.from_code(21)
    print(f"エラー: {error_detail.message}")
    print(f"対処法: {error_detail.description}")
except ValueError:
    print("未知のエラーコードです")
```

### 主要なエラーコード

**認証関連**:
- `4001007`: ログイン認証エラー
- `4001008`: API利用不可
- `4001009`: APIキー不一致

**注文関連**:
- `21`: 可能額不正エラー（余力不足）
- `11`: 銘柄情報不正エラー
- `17`: 呼値不正エラー

## 開発環境

### 必要な環境

- Python 3.12
- kabuステーション（三菱UFJ eスマート証券）
- APIパスワードの設定

### 開発用セットアップ

```bash
# リポジトリのクローン
git clone https://github.com/sk-guritech/py-kabusapi.git
cd py-kabusapi

# 依存関係のインストール
uv sync

# リンターの実行
uv run ruff check . --fix
uv run ruff format .
```

### Dockerでの開発

```bash
# devcontainerを使用
code .  # VS Codeで開く
# "Reopen in Container"を選択
```

## 使用例

### 日次の取引余力チェック

```python
from py_kabusapi.api import KabuStationAPI

def check_daily_balance():
    api = KabuStationAPI()
    
    # 認証
    auth_response = api.token("your_password")
    if auth_response.api_result_category != 0:
        print("認証に失敗しました")
        return
    
    # 各種余力の確認
    cash_response = api.wallet_cash()
    margin_response = api.wallet_margin()
    
    if cash_response.api_result_category == 0:
        cash_data = cash_response.content
        print(f"現物買付可能額: {cash_data.StockAccountWallet:,.0f}円")
    
    if margin_response.api_result_category == 0:
        margin_data = margin_response.content
        print(f"信用新規可能額: {margin_data.MarginAccountWallet:,.0f}円")
        print(f"保証金維持率: {margin_data.DepositkeepRate:.2f}%")

if __name__ == "__main__":
    check_daily_balance()
```

### 銘柄監視システム

```python
import time
from py_kabusapi.api import KabuStationAPI

def monitor_stock(symbol: str, target_price: float):
    api = KabuStationAPI()
    api.token("your_password")
    
    while True:
        response = api.board_by_symbol(symbol)
        if response.api_result_category == 0:
            board_data = response.content
            current_price = board_data.CurrentPrice
            
            print(f"{board_data.SymbolName}: {current_price}円")
            
            if current_price >= target_price:
                print(f"目標価格 {target_price}円 に到達しました！")
                break
        
        time.sleep(30)  # 30秒間隔で監視

# 使用例
monitor_stock("7203@1", 2600.0)  # トヨタ自動車を2600円で監視
```

### ランキング情報の取得

```python
from py_kabusapi.api import KabuStationAPI

def get_market_ranking():
    api = KabuStationAPI()
    api.token("your_password")
    
    # 売買高上位ランキング
    response = api.ranking("3", "ALL")
    if response.api_result_category == 0:
        ranking_data = response.content
        print("売買高上位ランキング:")
        for i, stock in enumerate(ranking_data[:10], 1):
            print(f"{i}. {stock.SymbolName} ({stock.Symbol}): {stock.TradingVolume:,.0f}株")

if __name__ == "__main__":
    get_market_ranking()
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 注意事項

- このライブラリは三菱UFJ eスマート証券のKabu Station APIを使用します
- 実際の取引を行う前に、必ずテスト環境で動作確認を行ってください
- APIの利用には、三菱UFJ eスマート証券での口座開設とAPIパスワードの設定が必要です
- 取引は自己責任で行ってください

## サポート

バグ報告や機能要望は、[GitHub Issues](https://github.com/sk-guritech/py-kabusapi/issues)までお願いします。
