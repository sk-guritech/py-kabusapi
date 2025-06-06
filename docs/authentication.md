# 認証

kabuステーションAPIを使用するには、まず認証を行いトークンを取得する必要があります。

## 基本的な認証

```python
from py_kabusapi import KabuStationAPI

api = KabuStationAPI(environment="test")

# 認証
response = api.token("your_api_password")

# 認証結果の確認
if response.api_result_category == "SUCCESS":
    print("認証成功")
    print(f"トークン: {response.content.Token}")
else:
    print("認証失敗")
    print(f"エラー: {response.content}")
```

## レスポンス

認証が成功すると、以下の情報が取得できます：

```python
{
    "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

## 注意事項

### トークンの有効性

発行されたAPIトークンは以下のタイミングで無効となります：

- kabuステーションを終了した時
- kabuステーションからログアウトした時  
- 別のトークンが新たに発行された時

### 自動ログアウト

kabuステーションは早朝、強制的にログアウトします。定期的にトークンの再取得が必要です。

## トークンの自動設定

認証が成功すると、取得したトークンは自動的にAPIクライアントに設定されます。以降のAPI呼び出しでは、このトークンが自動的に使用されます。

```python
# 認証
api.token("your_api_password")

# 以降のAPI呼び出しでは認証情報が自動的に使用される
cash_info = api.wallet_cash()
```

## エラーハンドリング

```python
try:
    response = api.token("your_api_password")
    if response.api_result_category != "SUCCESS":
        print(f"認証失敗: {response.content}")
except Exception as e:
    print(f"リクエストエラー: {e}")
```