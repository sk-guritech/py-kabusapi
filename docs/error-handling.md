# エラーハンドリング

py-kabuspapiでのエラーハンドリングの方法について説明します。

## レスポンスの種類

APIの呼び出し結果は以下の3種類のいずれかになります：

1. **ApiResultSuccess**: 成功
2. **ApiResultHttpError**: HTTPエラー
3. **ApiResultApiError**: APIエラー

## 基本的なエラーハンドリング

```python
from py_kabusapi import KabuStationAPI
from py_kabusapi.const import ApiResultCategory

api = KabuStationAPI(environment="test")

# 認証
response = api.token("your_password")

if response.api_result_category == ApiResultCategory.SUCCESS:
    print("認証成功")
    token_data = response.content
    print(f"トークン: {token_data.Token}")
    
elif response.api_result_category == ApiResultCategory.HTTP_ERROR:
    print("HTTPエラーが発生しました")
    error_data = response.content
    print(f"ステータスコード: {error_data.Code}")
    print(f"メッセージ: {error_data.Message}")
    
elif response.api_result_category == ApiResultCategory.API_ERROR:
    print("APIエラーが発生しました")
    error_data = response.content
    print(f"エラーコード: {error_data.Code}")
    print(f"メッセージ: {error_data.Message}")
```

## 具体的なエラーハンドリング例

### 注文時のエラーハンドリング

```python
def place_order_with_error_handling():
    try:
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
        
        if response.api_result_category == ApiResultCategory.SUCCESS:
            order_data = response.content
            print(f"注文成功 - 注文番号: {order_data.OrderId}")
            return order_data.OrderId
            
        elif response.api_result_category == ApiResultCategory.HTTP_ERROR:
            error_data = response.content
            print(f"HTTP接続エラー: {error_data.Code} - {error_data.Message}")
            
        elif response.api_result_category == ApiResultCategory.API_ERROR:
            error_data = response.content
            print(f"注文エラー: {error_data.Code} - {error_data.Message}")
            
            # 具体的なエラーコードに応じた処理
            if error_data.Code == "4001001":
                print("内部エラーが発生しました")
            elif error_data.Code == "4002001":
                print("銘柄コードエラーが発生しました")
            elif error_data.Code == "4003001":
                print("注文数量エラーが発生しました")
                
    except ValueError as e:
        print(f"パラメータエラー: {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")
        
    return None
```

### 口座情報取得時のエラーハンドリング

```python
def get_wallet_info_safely():
    try:
        response = api.wallet_cash()
        
        if response.api_result_category == ApiResultCategory.SUCCESS:
            wallet_data = response.content
            return {
                "stock_wallet": wallet_data.StockAccountWallet,
                "au_kc_wallet": wallet_data.AuKCStockAccountWallet,
                "au_jbn_wallet": wallet_data.AuJbnStockAccountWallet
            }
            
        else:
            print("口座情報の取得に失敗しました")
            if hasattr(response.content, 'Message'):
                print(f"エラーメッセージ: {response.content.Message}")
            return None
            
    except Exception as e:
        print(f"口座情報取得エラー: {e}")
        return None
```
