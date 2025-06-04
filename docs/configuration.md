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

### Docker Compose設定例

```yaml
version: '3.8'
services:
  trading-bot:
    build: .
    environment:
      - KABU_API_PASSWORD=your_password
      - KABU_ENVIRONMENT=test
    extra_hosts:
      - "host.docker.internal:host-gateway"  # Linux の場合
```

## 環境変数

### 推奨環境変数

```bash
# APIパスワード
export KABU_API_PASSWORD="your_api_password"

# 環境設定
export KABU_ENVIRONMENT="test"  # または "production"

# ホスト設定（必要に応じて）
export KABU_HOST="localhost"
```

### 環境変数を使用したコード例

```python
import os
from py_kabusapi import KabuStationAPI

# 環境変数から設定を取得
api_password = os.getenv("KABU_API_PASSWORD")
environment = os.getenv("KABU_ENVIRONMENT", "test")
host_name = os.getenv("KABU_HOST", "localhost")

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

## 設定クラス

### 設定管理クラスの例

```python
from dataclasses import dataclass
from typing import Literal
import os

@dataclass
class KabuApiConfig:
    """kabuステーションAPI設定"""
    
    environment: Literal["test", "production"] = "test"
    host_name: str = "localhost"
    api_password: str = ""
    is_in_docker_container: bool = False
    
    @classmethod
    def from_env(cls) -> "KabuApiConfig":
        """環境変数から設定を読み込み"""
        return cls(
            environment=os.getenv("KABU_ENVIRONMENT", "test"),
            host_name=os.getenv("KABU_HOST", "localhost"),
            api_password=os.getenv("KABU_API_PASSWORD", ""),
            is_in_docker_container=os.getenv("KABU_IN_DOCKER", "false").lower() == "true"
        )
    
    def create_api_client(self) -> KabuStationAPI:
        """設定からAPIクライアントを作成"""
        return KabuStationAPI(
            host_name=self.host_name,
            environment=self.environment,
            is_in_docker_container=self.is_in_docker_container
        )

# 使用例
config = KabuApiConfig.from_env()
api = config.create_api_client()

if config.api_password:
    api.token(config.api_password)
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

## セキュリティ設定

### APIパスワードの安全な管理

```python
import os
from pathlib import Path

def get_api_password():
    """安全にAPIパスワードを取得"""
    
    # 1. 環境変数から取得
    password = os.getenv("KABU_API_PASSWORD")
    if password:
        return password
    
    # 2. ファイルから取得
    password_file = Path.home() / ".kabu_api_password"
    if password_file.exists():
        return password_file.read_text().strip()
    
    # 3. 入力を求める
    import getpass
    return getpass.getpass("kabuステーション APIパスワード: ")

# 使用例
api = KabuStationAPI(environment="production")
password = get_api_password()
api.token(password)
```

### APIキーの保護

```python
class SecureKabuStationAPI(KabuStationAPI):
    """セキュアなAPIクライアント"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api_key_set = False
    
    def token(self, api_password: str):
        """トークン取得後にパスワードをクリア"""
        response = super().token(api_password)
        
        # パスワード変数をクリア
        api_password = None
        del api_password
        
        if response.api_result_category == "SUCCESS":
            self._api_key_set = True
        
        return response
    
    def is_authenticated(self) -> bool:
        """認証状態を確認"""
        return self._api_key_set and self.x_api_key is not None
```

## ログ設定

### ログレベル設定

```python
import logging

# kabuステーションAPI用のログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kabu_api.log'),
        logging.StreamHandler()
    ]
)

# 特定のライブラリのログレベルを調整
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
```

## 開発・本番環境の切り替え

### 環境別設定ファイル

```python
# config.py
import os
from typing import Dict, Any

ENVIRONMENTS = {
    "development": {
        "environment": "test",
        "host_name": "localhost",
        "debug": True,
        "log_level": "DEBUG"
    },
    "staging": {
        "environment": "test", 
        "host_name": "staging-server",
        "debug": False,
        "log_level": "INFO"
    },
    "production": {
        "environment": "production",
        "host_name": "localhost",
        "debug": False,
        "log_level": "WARNING"
    }
}

def get_config() -> Dict[str, Any]:
    """現在の環境設定を取得"""
    env = os.getenv("APP_ENV", "development")
    return ENVIRONMENTS.get(env, ENVIRONMENTS["development"])

# 使用例
config = get_config()
api = KabuStationAPI(
    host_name=config["host_name"],
    environment=config["environment"]
)
```

この設定により、環境に応じた適切なAPI接続が可能になります。