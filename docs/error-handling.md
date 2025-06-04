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

## 共通エラーコード

### 認証関連エラー

- **4001001**: 内部エラー
- **4001002**: APIパスワードエラー

### 注文関連エラー

- **4002001**: 銘柄コードエラー
- **4003001**: 注文数量エラー  
- **4004001**: 注文価格エラー
- **4005001**: 執行条件エラー
- **4006001**: 市場コードエラー
- **4007001**: 取引余力不足

### ネットワーク関連エラー

```python
import requests

try:
    response = api.wallet_cash()
    # レスポンス処理
    
except requests.exceptions.ConnectTimeout:
    print("接続タイムアウトが発生しました")
    
except requests.exceptions.ConnectionError:
    print("kabuステーションに接続できません")
    print("kabuステーションが起動しているか確認してください")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTPエラー: {e}")
    
except requests.exceptions.RequestException as e:
    print(f"リクエストエラー: {e}")
```

## リトライ処理

```python
import time
from typing import Optional

def api_call_with_retry(api_func, max_retries: int = 3, delay: float = 1.0):
    """APIコールをリトライ付きで実行"""
    
    for attempt in range(max_retries):
        try:
            response = api_func()
            
            if response.api_result_category == ApiResultCategory.SUCCESS:
                return response
                
            elif response.api_result_category == ApiResultCategory.HTTP_ERROR:
                # HTTPエラーの場合はリトライ
                if attempt < max_retries - 1:
                    print(f"HTTPエラー発生、{delay}秒後にリトライします...")
                    time.sleep(delay)
                    continue
                else:
                    return response
                    
            else:
                # APIエラーの場合はリトライしない
                return response
                
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"例外が発生しました: {e}")
                print(f"{delay}秒後にリトライします...")
                time.sleep(delay)
            else:
                raise
                
    return None

# 使用例
response = api_call_with_retry(lambda: api.wallet_cash())
```

## ログ出力

```python
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def logged_api_call(api_func, operation_name: str):
    """ログ付きAPIコール"""
    
    logger.info(f"{operation_name}を開始します")
    
    try:
        response = api_func()
        
        if response.api_result_category == ApiResultCategory.SUCCESS:
            logger.info(f"{operation_name}が成功しました")
            return response
            
        else:
            logger.error(f"{operation_name}が失敗しました: {response.content}")
            return response
            
    except Exception as e:
        logger.error(f"{operation_name}で例外が発生しました: {e}")
        raise

# 使用例
response = logged_api_call(
    lambda: api.sendorder(...),
    "注文発注"
)
```

## ベストプラクティス

1. **必ず api_result_category をチェック**する
2. **具体的なエラーメッセージを表示**する
3. **ネットワークエラーに対してはリトライ**を実装する
4. **APIエラーに対してはリトライしない**（設定ミス等のため）
5. **ログを出力**して問題の追跡を容易にする
6. **認証エラーの場合は再認証**を試行する

```python
def robust_api_operation():
    """堅牢なAPI操作の例"""
    
    # 認証状態をチェック
    if not api.x_api_key:
        auth_response = api.token("your_password")
        if auth_response.api_result_category != ApiResultCategory.SUCCESS:
            raise Exception("認証に失敗しました")
    
    # リトライ付きでAPI呼び出し
    response = api_call_with_retry(lambda: api.wallet_cash())
    
    if response and response.api_result_category == ApiResultCategory.SUCCESS:
        return response.content
    else:
        raise Exception("API呼び出しに失敗しました")
```