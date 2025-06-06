# 市場情報

株価、板情報、ランキングなどの市場データの取得方法について説明します。

## 時価情報・板情報

### 基本的な時価情報取得

```python
# 指定銘柄の時価情報・板情報を取得
response = api.board_by_symbol("8697@1")

if response.api_result_category == "SUCCESS":
    board_info = response.content
    print(f"現在値: {board_info.CurrentPrice}")
    print(f"前日比: {board_info.ChangePreviousDay}")
    print(f"出来高: {board_info.TradingVolume}")
```

### 銘柄詳細情報

```python
# 銘柄の詳細情報を取得
response = api.symbol_by_symbol("8697@1", addinfo=True)

if response.api_result_category == "SUCCESS":
    symbol_info = response.content
    print(f"銘柄名: {symbol_info.SymbolName}")
    print(f"市場名: {symbol_info.ExchangeName}")
    print(f"業種: {symbol_info.Sector33Name}")
```

## 銘柄コード取得

### 先物銘柄コード

```python
# 先物銘柄コード取得
response = api.symbolname_future(future_code="NK225", deriv_month=0)

if response.api_result_category == "SUCCESS":
    future_symbols = response.content
    for symbol in future_symbols:
        print(f"銘柄コード: {symbol.Symbol}")
        print(f"銘柄名: {symbol.SymbolName}")
```

### オプション銘柄コード

```python
# オプション銘柄コード取得
response = api.symbolname_option(
    deriv_month=202412,      # 限月
    put_or_call="C",         # コール
    strike_price=29000,      # 権利行使価格
    option_code="NK225op"    # オプションコード
)

if response.api_result_category == "SUCCESS":
    option_symbols = response.content
    for symbol in option_symbols:
        print(f"銘柄コード: {symbol.Symbol}")
        print(f"銘柄名: {symbol.SymbolName}")
```

### ミニオプション（限週）銘柄コード

```python
# ミニオプション（限週）銘柄コード取得
response = api.symbolname_minioptionweekly(
    deriv_month=202412,      # 限月
    deriv_weekly=1,          # 限週
    put_or_call="P",         # プット
    strike_price=29000       # 権利行使価格
)
```

## ランキング情報

### 基本的なランキング取得

```python
# 値上がり率ランキング（全市場）
response = api.ranking(
    type="3",               # ランキング種別 (1-15)
    exchange_division="ALL" # 市場 (ALL, T, TP, TS, TG, M, FK, S)
)

if response.api_result_category == "SUCCESS":
    ranking = response.content
    for rank in ranking.Ranking:
        print(f"{rank.No}位: {rank.Symbol} {rank.SymbolName}")
        print(f"値上がり率: {rank.RatioOfChange}%")
```

### ランキング種別

```python
# 売買代金上位を取得
response = api.ranking(type="4", exchange_division="T")
```

## 為替情報

```python
# 為替レート取得
response = api.exchange_by_symbol("usdjpy")

if response.api_result_category == "SUCCESS":
    exchange_info = response.content
    print(f"USD/JPY: {exchange_info.BidPrice} - {exchange_info.AskPrice}")
```

### 対応通貨ペア

usdjpy, eurjpy, gbpjpy, audjpy, chfjpy, cadjpy, nzdjpy, zarjpy, eurusd, gbpusd, audusd

## 規制情報

### 銘柄の規制情報

```python
# 規制情報＋空売り規制情報を取得
response = api.regulations_by_symbol("8697@1")

if response.api_result_category == "SUCCESS":
    regulations = response.content
    print(f"規制情報: {regulations}")
```

### 優先市場情報

```python
# 株式の優先市場を取得
response = api.primaryexchange_by_symbol("8697")

if response.api_result_category == "SUCCESS":
    primary_exchange = response.content
    print(f"優先市場: {primary_exchange}")
```

## プレミアム料

```python
# 信用取引のプレミアム料を取得
response = api.margin_marginpremium_by_symbol("8697")

if response.api_result_category == "SUCCESS":
    premium = response.content
    print(f"プレミアム料: {premium}")
```

## APIソフトリミット

```python
# APIのソフトリミット値を取得
response = api.apisoftlimit()

if response.api_result_category == "SUCCESS":
    soft_limit = response.content
    print(f"ソフトリミット: {soft_limit}")
```
