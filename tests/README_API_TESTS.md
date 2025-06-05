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
| `KABUS_PASSWORD` | `testpassword` | APIパスワード |

## 注意事項

- API統合テストは実際のkabuステーションAPIに接続します
- 発注APIは production 環境では自動的にスキップされます
- レート制限を遵守してテストが実行されます（発注API: 5件/秒、その他: 10件/秒）