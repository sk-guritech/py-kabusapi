# 口座情報

口座の取引余力や残高情報の取得方法について説明します。

## 現物取引余力

### 全体の取引余力

```python
# 現物取引余力を取得
response = api.wallet_cash()

if response.api_result_category == "SUCCESS":
    cash_info = response.content
    print(f"株式取引余力: {cash_info.StockAccountWallet}")
    print(f"auカブコム証券余力: {cash_info.AuKCStockAccountWallet}")
    print(f"auじぶん銀行余力: {cash_info.AuJbnStockAccountWallet}")
```

### 銘柄別取引余力

```python
# 特定銘柄の現物取引余力を取得
response = api.wallet_cash_by_symbol("7974@1")

if response.api_result_category == "SUCCESS":
    cash_info = response.content
    print(f"株式取引余力: {cash_info.StockAccountWallet}")
```

## 信用取引余力

### 全体の信用取引余力

```python
# 信用取引余力を取得
response = api.wallet_margin()

if response.api_result_category == "SUCCESS":
    margin_info = response.content
    print(f"信用取引余力: {margin_info.MarginAccountWallet}")
    print(f"保証金維持率: {margin_info.DepositkeepRate}")
```

### 銘柄別信用新規可能額

```python
# 特定銘柄の信用新規可能額を取得
response = api.wallet_margin_by_symbol("5905@27")

if response.api_result_category == "SUCCESS":
    margin_info = response.content
    print(f"信用新規可能額: {margin_info.MarginAccountWallet}")
```

## 先物取引余力

### 全体の先物取引余力

```python
# 先物取引余力を取得
response = api.wallet_future()

if response.api_result_category == "SUCCESS":
    future_info = response.content
    # 先物取引余力の詳細情報を表示
    print(future_info)
```

### 銘柄別先物取引余力

```python
# 特定銘柄の先物取引余力を取得
response = api.wallet_future_by_symbol("160060018@23")

if response.api_result_category == "SUCCESS":
    future_info = response.content
    print(future_info)
```

## オプション取引余力

### 全体のオプション取引余力

```python
# オプション取引余力を取得
response = api.wallet_option()

if response.api_result_category == "SUCCESS":
    option_info = response.content
    print(option_info)
```

### 銘柄別オプション取引余力

```python
# 特定銘柄のオプション取引余力を取得  
response = api.wallet_option_by_symbol("140248026@23")

if response.api_result_category == "SUCCESS":
    option_info = response.content
    print(option_info)
```

## 建玉一覧

### 全建玉の取得

```python
# 全建玉を取得
response = api.positions()

if response.api_result_category == "SUCCESS":
    positions = response.content
    for position in positions:
        print(f"銘柄: {position.Symbol}")
        print(f"数量: {position.LeavesQty}")
        print(f"損益: {position.ProfitLoss}")
```

### 条件を指定した建玉取得

```python
# 現物のみ取得
positions = api.positions(product="1")

# 特定銘柄の建玉を取得
positions = api.positions(symbol="1000")

# 買建玉のみ取得
positions = api.positions(side="2")

# 追加情報付きで取得
positions = api.positions(addinfo="true")
```

## エラーハンドリング

```python
try:
    response = api.wallet_cash()
    
    if response.api_result_category == "SUCCESS":
        cash_info = response.content
        print(f"取引余力: {cash_info.StockAccountWallet}")
    else:
        print(f"エラー: {response.content}")
        
except Exception as e:
    print(f"API呼び出しエラー: {e}")
```
