# py-kabusapi

Python wrapper for kabuステーション API

## インストール

### GitHubから直接インストール

```bash
pip install git+https://github.com/sk-guritech/py-kabusapi.git
```

### ローカルでの開発用インストール

```bash
git clone https://github.com/sk-guritech/py-kabusapi.git
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

テスト実行方法、環境設定、トラブルシューティングについては **[tests/README_TESTS.md](./tests/README_TESTS.md)** を参照してください。

## 関連リンク

- **[📚 詳細ドキュメント](./docs/)** - 使い方の詳細ガイド
- **[🔗 kabuステーション API仕様](https://kabucom.github.io/kabusapi/ptal/index.html)** - 公式API仕様書

## ライセンス

このプロジェクトは [MIT License](./LICENSE) の下で公開されています。

Copyright (c) 2025 Sakaguchi Ryo <sakaguchi@sk-techfirm.com>