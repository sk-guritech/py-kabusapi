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

### クイックスタート

```python
from py_kabusapi import KabuStationAPI

# APIクライアントの初期化
api = KabuStationAPI(environment="test")

# 認証
api.token("your_api_password")

# 口座情報の取得
cash_info = api.wallet_cash()
```

### 詳細なドキュメント

詳細な使い方については、[docsフォルダ](./docs/)のドキュメントを参照してください：

- **[基本的な使い方](./docs/basic-usage.md)** - APIクライアントの初期化と基本設定
- **[認証](./docs/authentication.md)** - APIトークンの取得と管理
- **[注文機能](./docs/orders.md)** - 現物・先物・オプション注文の発注方法
- **[口座情報](./docs/wallet.md)** - 取引余力と建玉情報の取得
- **[市場情報](./docs/market-data.md)** - 株価・板情報・ランキングの取得
- **[エラーハンドリング](./docs/error-handling.md)** - 堅牢なエラー処理の実装
- **[設定](./docs/configuration.md)** - 環境設定とDocker対応

## 必要なパッケージ

- requests
- pydantic

## 機能

### 対応API

- ✅ **認証** - APIトークンの取得
- ✅ **注文** - 現物・先物・オプション注文の発注・取消
- ✅ **口座情報** - 取引余力・建玉情報の取得
- ✅ **市場情報** - 時価・板情報・ランキングの取得
- ✅ **銘柄情報** - 銘柄詳細・銘柄コード検索
- ✅ **為替情報** - 主要通貨ペアのレート取得

### 特徴

- 🔧 **型安全性** - 完全な型ヒント対応
- 🚀 **使いやすさ** - Literal型でIDEの自動補完をサポート
- 🛡️ **エラーハンドリング** - 包括的なエラー処理機能
- 🐳 **Docker対応** - コンテナ環境での実行をサポート
- 📚 **豊富なドキュメント** - 実用的なコード例を含む詳細ドキュメント

## テスト

### テスト実行方法

#### 基本テスト（推奨）
```bash
# インポートテストのみ実行（API接続不要）
pytest tests/ -v -m "not api_integration"
```

#### 包括的API統合テスト
```bash
# 環境変数を設定
export KABUS_HOST=localhost
export KABUS_ENV=production
export KABUS_DOCKER=true
export KABUS_PASSWORD=your_api_password

# API統合テストを実行（25のAPIエンドポイントをテスト）
pytest tests/ -v -m "api_integration"
```

#### 全テスト実行
```bash
# 全てのテストを実行
pytest tests/ -v
```

### テスト種別

#### インポートテスト
- パッケージのインポート可能性をテスト
- CI/CDで自動実行
- API接続不要

#### API統合テスト
- 25のAPIエンドポイントを包括的にテスト
- 適切なレート制限を実装（発注API: 5件/秒、その他: 10件/秒）
- production環境では発注APIを自動スキップ
- 実際のkabuステーション接続が必要

### 要件

API統合テストの実行には以下が必要です：
- kabuステーションの起動（localhost:18080 for production / localhost:18081 for test）
- 有効なAPIパスワード

詳細な情報は [tests/README_API_TESTS.md](./tests/README_API_TESTS.md) を参照してください。

### CI/CD

GitHub Actionsで自動的にPython 3.10, 3.11, 3.12でのインポートテストが実行されます（API統合テストは除外）。

## 関連リンク

- **[📚 詳細ドキュメント](./docs/)** - 使い方の詳細ガイド
- **[🔗 kabuステーション API仕様](https://kabucom.github.io/kabusapi/)** - 公式API仕様書

## ライセンス

このプロジェクトは [MIT License](./LICENSE) の下で公開されています。

Copyright (c) 2025 Sakaguchi Ryo <sakaguchi@sk-techfirm.com>