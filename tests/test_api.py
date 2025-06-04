"""API tests for py-kabusapi."""

from py_kabusapi import KabuStationAPI


def test_api():
    """Test basic API functionality."""
    api = KabuStationAPI(is_in_docker_container=True, environment="test")

    # AUTHENTICATION
    try:
        api.token("password")
        print("✓ Authentication test passed")
    except Exception as e:
        print(f"✗ Authentication test failed: {e}")

    # TRADING_CAPACITY
    try:
        api.wallet_cash()
        print("✓ wallet_cash test passed")
    except Exception as e:
        print(f"✗ wallet_cash test failed: {e}")

    try:
        api.wallet_cash_by_symbol("7974@1")
        print("✓ wallet_cash_by_symbol test passed")
    except Exception as e:
        print(f"✗ wallet_cash_by_symbol test failed: {e}")

    try:
        api.wallet_margin()
        print("✓ wallet_margin test passed")
    except Exception as e:
        print(f"✗ wallet_margin test failed: {e}")

    try:
        api.wallet_margin_by_symbol("5905@27")
        print("✓ wallet_margin_by_symbol test passed")
    except Exception as e:
        print(f"✗ wallet_margin_by_symbol test failed: {e}")


def test_commented_features():
    """Test features that are currently commented out."""
    api = KabuStationAPI(is_in_docker_container=True, environment="production")

    # ORDER_PLACEMENT
    # api.sendorder()
    # api.sendorder_future()
    # api.sendorder_option()
    # api.cancelorder()

    # TRADING_CAPACITY (additional)
    # api.wallet_future()
    # api.wallet_future_by_symbol("160060018@23")
    # api.wallet_option()
    # api.wallet_option_by_symbol("140248026@23")

    # INFORMATION
    # api.board_by_symbol("8697@1")
    # api.symbol_by_symbol("8697@1", True)
    # api.orders("0", "1234", "20210101000000", "true", "8697", "5", "2", "2")
    # api.positions("0", "8697", "2", "true")
    # api.symbolname_future("NK225", 0)
    # api.symbolname_option(0, "C", 0, "NK225miniop")
    # api.symbolname_minioptionweekly(0, 0, "C", 0)
    # api.ranking("3", "ALL")
    # api.exchange_by_symbol("usdjpy")
    # api.regulations_by_symbol("8697@1")
    # api.primaryexchange_by_symbol("8697")
    # api.margin_marginpremium_by_symbol("8697")
    # api.apisoftlimit()
    pass


if __name__ == "__main__":
    print("Running API tests...")
    test_api()
    print("\nCommented features are available in test_commented_features()")
