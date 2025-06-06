# py-kabusapi ドキュメント

Python wrapper for kabuステーション API

> 💡 **初めての方は**: [プロジェクトのREADME](../README.md)もご確認ください

## 📚 ドキュメント目次

### 🚀 入門ガイド
- **[基本的な使い方](basic-usage.md)** - APIクライアントの初期化と基本設定
- **[認証](authentication.md)** - APIトークンの取得と管理

### 💼 機能別ガイド
- **[注文機能](orders.md)** - 現物・先物・オプション注文の発注方法
- **[口座情報](wallet.md)** - 取引余力と建玉情報の取得
- **[市場情報](market-data.md)** - 株価・板情報・ランキングの取得

### 🔧 高度な使い方
- **[エラーハンドリング](error-handling.md)** - 堅牢なエラー処理の実装
- **[設定](configuration.md)** - 環境設定とDocker対応

## ⚡ クイックスタート

```python
from py_kabusapi import KabuStationAPI

# APIクライアントの初期化
api = KabuStationAPI(environment="test")

# 認証
response = api.token("your_api_password")
if response.api_result_category == "SUCCESS":
    print("認証成功")
    
    # 口座情報の取得
    cash_info = api.wallet_cash()
    if cash_info.api_result_category == "SUCCESS":
        print(f"取引余力: {cash_info.content.StockAccountWallet}円")
```

## 🎯 主な特徴

- **型安全性**: 完全な型ヒント対応でIDEの自動補完をサポート
- **包括的なドキュメント**: 実用的なコード例を含む詳細ガイド
- **エラーハンドリング**: 堅牢なエラー処理パターンの提供

## 📖 関連リンク

- [プロジェクトREADME](../README.md) - インストール方法とテスト実行手順
- [kabuステーション API仕様](https://kabucom.github.io/kabusapi/ptal/index.html) - 公式API仕様書

---

各ページには実際に動作するコード例が含まれています。順番に読み進めるか、必要な機能のページに直接ジャンプしてください。