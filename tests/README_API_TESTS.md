# API統合テストについて

## 概要
`test_api_sequential.py`には実際のkabuステーションAPIを呼び出す統合テストが含まれています。
これらのテストは`@pytest.mark.api_integration`マーカーが付けられており、通常のCI/CDでは実行されません。

## 実行方法

### 通常のテスト（API統合テストを除外）
```bash
pytest tests/ -v -m "not api_integration"
```

### API統合テストのみ実行
```bash
# 環境変数を設定
export KABUS_HOST=localhost
export KABUS_ENV=production
export KABUS_DOCKER=true
export KABUS_PASSWORD=testpassword

# API統合テストを実行
pytest tests/ -v -m "api_integration"
```

### 全てのテストを実行
```bash
pytest tests/ -v
```

## 環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| `KABUS_HOST` | `localhost` | kabuステーションのホスト |
| `KABUS_ENV` | `production` | 環境（`test` or `production`） |
| `KABUS_DOCKER` | `true` | Docker環境フラグ |
| `KABUS_PASSWORD` | `CHANGE_ME_FOR_TESTING` | APIパスワード（テスト専用を設定） |

## 注意事項

### セキュリティ
⚠️ **重要: パスワード管理**
- **本番用パスワードをテストに使用しない**でください
- テスト専用のAPIパスワードを設定することを強く推奨します
- パスワードは環境変数で設定し、ソースコードに含めないでください
- 共有環境でのテスト実行時は、パスワードの漏洩に注意してください

### API実行
- API統合テストは実際のkabuステーションAPIに接続します
- 発注APIは production 環境では自動的にスキップされます
- レート制限を遵守してテストが実行されます（発注API: 5件/秒、その他: 10件/秒）

### 推奨設定
```bash
# テスト専用の設定を使用
export KABUS_ENV=test  # test環境を推奨
export KABUS_PASSWORD=test_password_only  # テスト専用パスワード
```