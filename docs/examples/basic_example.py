#!/usr/bin/env python3
"""
py-kabusapi 基本的な使用例

このサンプルではAPIクライアントの基本的な使い方を示します。
"""

import os

from py_kabusapi import KabuStationAPI
from py_kabusapi.const import ApiResultCategory


def main():
    """基本的なAPI使用例"""

    # APIクライアントの初期化
    print("=== py-kabusapi 基本例 ===")

    # 本番環境で初期化（Dockerコンテナ内から）
    api = KabuStationAPI(environment="production", is_in_docker_container=True)
    print("APIクライアントを初期化しました (production環境, Docker内)")

    # 環境変数からAPIパスワードを取得
    api_password = os.getenv("KABU_API_PASSWORD")
    if not api_password:
        print("KABU_API_PASSWORD環境変数を設定してください")
        return

    # 認証
    print("\n--- 認証 ---")
    auth_response = api.token(api_password)

    if auth_response.api_result_category == ApiResultCategory.SUCCESS:
        print("✅ 認証成功")
        print(f"トークン: {auth_response.content.Token[:10]}...")
    else:
        print("❌ 認証失敗")
        print(f"エラー: {auth_response.content}")
        return

    # 口座情報の取得
    print("\n--- 口座情報取得 ---")
    try:
        cash_response = api.wallet_cash()

        if cash_response.api_result_category == ApiResultCategory.SUCCESS:
            cash_info = cash_response.content
            print("✅ 口座情報取得成功")
            print(f"株式取引余力: {cash_info.StockAccountWallet:,.0f}円")
            print(f"auカブコム証券余力: {cash_info.AuKCStockAccountWallet:,.0f}円")
            print(f"auじぶん銀行余力: {cash_info.AuJbnStockAccountWallet:,.0f}円")
        else:
            print("❌ 口座情報取得失敗")
            print(f"エラー: {cash_response.content}")

    except Exception as e:
        print(f"❌ 例外が発生しました: {e}")
        print("💡 これはkabuステーションAPIのレスポンスにNullが含まれているためです")

    # 注文一覧の取得（よりシンプルなAPI）
    print("\n--- 注文一覧取得 ---")
    try:
        orders_response = api.orders()

        if orders_response.api_result_category == ApiResultCategory.SUCCESS:
            print("✅ 注文一覧取得成功")
            print(f"レスポンス型: {type(orders_response.content)}")
            # ordersは配列として返される可能性があるため、直接チェック
            if hasattr(orders_response.content, "__len__"):
                orders = orders_response.content
                print(f"注文件数: {len(orders)}件")
            else:
                print("注文データ構造を確認中...")
        else:
            print("❌ 注文一覧取得失敗")
            print(f"エラー: {orders_response.content}")

    except Exception as e:
        print(f"❌ 例外が発生しました: {e}")

    # 建玉一覧の取得
    print("\n--- 建玉一覧取得 ---")
    try:
        positions_response = api.positions()

        if positions_response.api_result_category == ApiResultCategory.SUCCESS:
            print("✅ 建玉一覧取得成功")
            print(f"レスポンス型: {type(positions_response.content)}")
            # positionsも同様にチェック
            if hasattr(positions_response.content, "__len__"):
                positions = positions_response.content
                print(f"建玉件数: {len(positions)}件")
            else:
                print("建玉データ構造を確認中...")
        else:
            print("❌ 建玉一覧取得失敗")
            print(f"エラー: {positions_response.content}")

    except Exception as e:
        print(f"❌ 例外が発生しました: {e}")

    print("\n=== 基本例終了 ===")


if __name__ == "__main__":
    main()
