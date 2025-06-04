# 基本的な使い方

## インストール

```bash
git clone https://github.com/sk-guritech/py-kabusapi.git
cd py-kabusapi
pip install -e .
```

## 初期化

```python
from py_kabusapi import KabuStationAPI

# テスト環境での初期化
api = KabuStationAPI(environment="test")

# 本番環境での初期化
api = KabuStationAPI(environment="production")

# Dockerコンテナ内から使用する場合
api = KabuStationAPI(
    environment="test",
    is_in_docker_container=True
)
```

## 環境設定

### 接続先

- **test環境**: localhost:18081
- **production環境**: localhost:18080

### Dockerコンテナからの接続

Dockerコンテナ内からkabuステーションAPIに接続する場合は、`is_in_docker_container=True`を設定してください。

```python
api = KabuStationAPI(
    environment="test",
    is_in_docker_container=True
)
```

## 基本的なワークフロー

1. APIクライアントの初期化
2. 認証（トークン取得）
3. API呼び出し

```python
from py_kabusapi import KabuStationAPI

# 1. 初期化
api = KabuStationAPI(environment="test")

# 2. 認証
response = api.token("your_api_password")
if response.api_result_category == "SUCCESS":
    print("認証成功")
else:
    print("認証失敗")

# 3. API呼び出し
cash_info = api.wallet_cash()
```