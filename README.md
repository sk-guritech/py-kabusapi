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

### テスト実行方法

開発環境でのテスト実行は以下の方法を推奨します：

```bash
# プロジェクトルートディレクトリから実行
PYTHONPATH=. python tests/test_api.py
PYTHONPATH=. python tests/test_import.py
```

### APIテストの実行

```bash
# 基本的なAPIテスト
PYTHONPATH=. python tests/test_api.py
```

注意: テストを実行するには、localhost:18080 (production) または localhost:18081 (test) でkabuステーション APIサーバーが動作している必要があります。

### インポートテスト

Python 3.10～3.12でのインポートテストを実行:

```bash
# インポートテスト
PYTHONPATH=. python tests/test_import.py

# 複数バージョンでテスト (toxを使用)
pip install tox
tox
```


### CI/CD

GitHub Actionsで自動的にPython 3.10, 3.11, 3.12でのインポートテストが実行されます。

## ライセンス

MIT License