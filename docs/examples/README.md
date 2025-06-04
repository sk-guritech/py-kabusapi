# サンプルコード

実際の使用例を示すサンプルコードです。

## 基本的な使用例

### [basic_example.py](basic_example.py)
APIクライアントの基本的な使い方

### [order_example.py](order_example.py)
注文の発注と管理

### [wallet_monitoring.py](wallet_monitoring.py)
口座情報の監視

### [market_data_fetcher.py](market_data_fetcher.py)
市場データの取得と処理

## 実用的な例

### [trading_bot_example.py](trading_bot_example.py)
シンプルな取引ボットの実装例

### [error_handling_example.py](error_handling_example.py)
堅牢なエラーハンドリングの実装

### [docker_example/](docker_example/)
Dockerコンテナでの実行例

## 実行方法

```bash
# プロジェクトルートから実行
PYTHONPATH=. python docs/examples/basic_example.py
```

## 注意事項

- サンプルコードはテスト環境での使用を前提としています
- 本番環境で使用する場合は、適切にAPIパスワードや設定を変更してください
- 実際の注文は行わないよう、コメントアウトされている部分があります