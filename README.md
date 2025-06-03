# py-kabusapi

Python wrapper for kabuステーション API

## インストール

### GitHubから直接インストール

```bash
pip install git+https://github.com/yourusername/py-kabusapi.git
```

### ローカルでの開発用インストール

```bash
git clone https://github.com/yourusername/py-kabusapi.git
cd py-kabusapi
pip install -e .
```

## 使い方

```python
from py_kabusapi import KabuStationAPI

# APIクライアントの初期化
api = KabuStationAPI()

# 使用例
# TODO: 実際のAPIの使用方法を記載
```

## 必要なパッケージ

- requests
- pydantic

## テスト

### APIテストの実行

```bash
python tests/test_api.py
```

注意: テストを実行するには、localhost:18081でkabuステーション APIサーバーが動作している必要があります。

### インポートテスト

Python 3.10～3.12でのインポートテストを実行:

```bash
# 単一バージョンでテスト
python tests/test_import.py

# 複数バージョンでテスト (toxを使用)
pip install tox
tox
```

### CI/CD

GitHub Actionsで自動的にPython 3.10, 3.11, 3.12でのインポートテストが実行されます。

## ライセンス

MIT License