# 設定

py-kabuspapiの各種設定について説明します。

## 基本設定

### 環境設定

```python
from py_kabusapi import KabuStationAPI

# テスト環境（デフォルト）
api = KabuStationAPI(environment="test")

# 本番環境
api = KabuStationAPI(environment="production")
```

### 接続先設定

| 環境 | ポート | 用途 |
|------|--------|------|
| test | 18081 | 検証・開発用 |
| production | 18080 | 本番取引用 |

### ホスト設定

```python
# デフォルト（localhost）
api = KabuStationAPI(host_name="localhost")

# 他のホストを指定
api = KabuStationAPI(host_name="192.168.1.100")
```

## Docker環境での設定

### Docker内からの接続

```python
# Docker コンテナ内から kabuステーション に接続する場合
api = KabuStationAPI(
    environment="test",
    is_in_docker_container=True  # host.docker.internal を使用
)
```

## 環境変数

### 環境変数を使用したコード例

```python
import os
from py_kabusapi import KabuStationAPI

# 環境変数から設定を取得
api_password = os.getenv("KABU_API_PASSWORD")
environment = os.getenv("KABU_ENVIRONMENT", "test")
host_name = os.getenv("KABU_HOST", "localhost") # 必要に応じて

# APIクライアントの初期化
api = KabuStationAPI(
    host_name=host_name,
    environment=environment
)

# 認証
if api_password:
    api.token(api_password)
else:
    raise ValueError("KABU_API_PASSWORD環境変数が設定されていません")
```

## ネットワーク設定

### タイムアウト設定

py-kabuspapiはデフォルトで2分のタイムアウトを設定していますが、必要に応じてrequestsレベルでカスタマイズできます：

```python
import requests
from py_kabusapi import KabuStationAPI

# セッションを作成してタイムアウトを設定
session = requests.Session()
session.timeout = 30  # 30秒のタイムアウト

# APIクライアント内でセッションを使用する場合は
# 現在の実装では直接設定できないため、
# requests.requestメソッドをモンキーパッチする方法があります
```

### プロキシ設定

```python
import requests
import os

# プロキシ設定
proxies = {
    'http': os.getenv('HTTP_PROXY'),
    'https': os.getenv('HTTPS_PROXY')
}

# requests.Session にプロキシを設定
session = requests.Session()
session.proxies.update(proxies)
```
