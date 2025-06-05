# テスト実行ガイド

## テスト概要

py-kabusapiでは、WebSocketを含む包括的なAPIテストを提供しています：
- **基本テスト** - API接続不要のユニットテスト
- **API統合テスト** - 実際のkabuステーションAPIを使用した統合テスト
- **WebSocketテスト** - リアルタイム市場データ受信機能のテスト

## クイックスタート

### 実行例

```bash
# 基本テストのみ（3個）
$ pytest -m "not api_integration and not websocket"

# WebSocketテストのみ（9個）
$ KABUS_PASSWORD="password" KABUS_ENV="test" KABUS_DOCKER="true" pytest -m websocket -v

# test環境で利用可能なテストのみ（21個）
$ KABUS_PASSWORD="password" KABUS_ENV="test"  KABUS_DOCKER="true" pytest -m test_env -v

# production環境で利用可能なテストのみ(36個)
$ KABUS_PASSWORD="testpassword" KABUS_ENV="production"  KABUS_DOCKER="true" pytest -m "prod_env"
```

## テスト種別詳細

### 基本テスト（API接続不要）
- **WebSocketデータモデルテスト** - WebSocketPushDataの型安全性確認
- **インポートテスト** - パッケージの正常インポート確認

### API統合テスト（kabuステーション接続必要）

#### 認証API（1個）
- トークン取得・管理

#### 情報取得API（22個）
- 板情報、銘柄情報、注文一覧、残高一覧
- ランキング、規制情報、先物・オプション銘柄名取得
- ウォレット情報（現物・信用・先物・オプション）
- 為替情報、API制限情報

#### 銘柄登録API（3個）
- PUSH配信用銘柄の登録・解除
- 全銘柄解除

#### WebSocketテスト（9個 + 1個スキップ）
- 接続状態管理、コールバック機能
- エラーハンドリング、メッセージ送信
- ヘッダー設定（通常環境・Docker環境）
- リアルタイム市場データ受信機能
- 実際の接続テスト（時間依存のため通常スキップ）

#### データモデルテスト（2個）
- WebSocketPushDataの型安全性確認

## テストマーカー

### 利用可能なマーカー
- `api_integration` - API統合テスト（kabuステーション接続必要）
- `websocket` - WebSocket機能テスト
- `websocket_model` - WebSocketデータモデルテスト
- `prod_env` - production環境で動作するテスト
- `test_env` - test環境で動作するテスト
- `order_api` - 注文API（危険な操作のため通常はスキップ）

## 環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| `KABUS_HOST` | `localhost` | kabuステーションのホスト<br>Docker環境では`host.docker.internal` |
| `KABUS_ENV` | `production` | 環境（`test` or `production`） |
| `KABUS_DOCKER` | `true` | Docker環境フラグ |
| `KABUS_PASSWORD` | `CHANGE_ME_FOR_TESTING` | APIパスワード（テスト専用を設定） |

## 要件

API統合テストの実行には以下が必要です：

### kabuステーションの起動
- **Production環境**: `localhost:18080`
- **Test環境**: `localhost:18081`
- **Docker環境**: `host.docker.internal:18080/18081`

### APIパスワード
- テスト専用パスワードの使用を推奨
- 環境変数`KABUS_PASSWORD`で設定

## CI/CD

GitHub Actionsで自動的にPython 3.10, 3.11, 3.12での基本テストが実行されます（API統合テストは除外）。