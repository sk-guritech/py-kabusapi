# 注文機能

注文の発注、取消、一覧取得の機能について説明します。

## 現物注文 (sendorder)

### 基本的な注文

```python
# 買い注文の例
response = api.sendorder(
    symbol="1000",           # 銘柄コード
    exchange="1",            # 市場コード
    security_type="1",       # 商品種別
    side="2",                # 売買区分
    cash_margin="1",         # 信用区分
    deliv_type="2",          # 受渡区分
    account_type="2",        # 口座種別
    qty=100,                 # 注文数量
    price=1000.0,            # 注文価格
    expire_day=20241231,     # 注文有効期限 (yyyyMMdd形式)
    front_order_type="10"    # 執行条件
)
```

### 信用取引

```python
# 信用買い注文
response = api.sendorder(
    symbol="1000",
    exchange="1",
    security_type="1",
    side="2",                 # 売買区分
    cash_margin="2",          # 信用区分
    deliv_type="0",
    account_type="2",
    qty=100,
    price=1000.0,
    expire_day=20241231,
    front_order_type="17",    # 執行条件
    margin_trade_type="1"     # 信用取引区分
)
```

### 返済注文

```python
# 返済売り注文
response = api.sendorder(
    symbol="1000",
    exchange="1", 
    security_type="1",
    side="1",                 # 売買区分
    cash_margin="3",          # 信用区分
    deliv_type="0",
    account_type="2",
    qty=100,
    price=1100.0,
    expire_day=20241231,
    front_order_type="17",
    close_position_order="0"  # 決済順序
)
```

## 先物注文 (sendorder_future)

```python
response = api.sendorder_future(
    symbol="167060018",       # 銘柄コード
    exchange="2",             # 市場コード
    trade_type="1",           # 取引区分
    time_in_force="1",        # 有効期間条件
    side="2",                 # 売買区分
    qty=1,                    # 注文数量
    price=29000.0,            # 注文価格
    expire_day=20241231,      # 注文有効期限
    front_order_type="120"    # 執行条件
)
```

## オプション注文 (sendorder_option)

```python
response = api.sendorder_option(
    symbol="140248026",       # 銘柄コード
    exchange="2",             # 市場コード
    trade_type="1",           # 取引区分
    time_in_force="1",        # 有効期間条件
    side="2",                 # 売買区分
    qty=1,                    # 注文数量
    price=100.0,              # 注文価格
    expire_day=20241231,      # 注文有効期限
    front_order_type="120"    # 執行条件
)
```

## 注文取消 (cancelorder)

```python
# 注文取消
response = api.cancelorder("order_id_here")

if response.api_result_category == "SUCCESS":
    print("注文取消成功")
else:
    print("注文取消失敗")
```

## 注文一覧取得 (orders)

### 全注文の取得

```python
# 全注文を取得
orders = api.orders()
```

### 条件を指定した注文取得

```python
# 現物の未約定注文のみ取得
orders = api.orders(
    product="1",    # 取得する商品
    state="1"       # 状態
)

# 特定銘柄の注文を取得
orders = api.orders(
    symbol="1000",
    side="2"        # 売買区分
)
```

## レスポンスの確認

```python
response = api.sendorder(
    symbol="1000",
    exchange="1",
    security_type="1",
    side="2",
    cash_margin="1",
    deliv_type="2",
    account_type="2",
    qty=100,
    price=1000.0,
    expire_day=20241231,
    front_order_type="17"
)

if response.api_result_category == "SUCCESS":
    print(f"注文番号: {response.content.OrderId}")
    print("注文成功")
else:
    print(f"注文失敗: {response.content}")
```

## 型ヒントの活用

Literal型パラメータによりIDEでの自動補完がサポートされています：

```python
# IDEで候補が表示される
api.sendorder(
    exchange="1",      # 市場コード
    side="2",          # 売買区分
    cash_margin="1",   # 信用区分
    # ...
)
```