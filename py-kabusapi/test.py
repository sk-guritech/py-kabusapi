from api import KabuStationAPI

api = KabuStationAPI()

# AUTHENTICATION
api.token("password")

# ORDER_PLACEMENT
# api.sendorder()
# api.sendorder_future()
# api.sendorder_option()
# api.cancelorder()

# TRADING_CAPACITY
api.wallet_cash()
api.wallet_cash_by_symbol("7974@1")
api.wallet_margin()
api.wallet_margin_by_symbol("5905@27")
api.wallet_future()
api.wallet_future_by_symbol("160060018@23")
api.wallet_option()
api.wallet_option_by_symbol("140248026@23")

# INFORMATION
api.board_by_symbol("8697@1")
api.symbol_by_symbol("8697@1", True)
api.orders("0", "1234", "20210101000000", "true", "8697", "5", "2", "2")
api.positions("0", "8697", "2", "true")
api.symbolname_future("NK225", 0)
api.symbolname_option(0, "C", 0, "NK225miniop")
api.symbolname_minioptionweekly(0, 0, "C", 0)
# api.ranking("3", "ALL")
api.exchange_by_symbol("usdjpy")
api.regulations_by_symbol("8697@1")
api.primaryexchange_by_symbol("8697")
api.margin_marginpremium_by_symbol("8697")
api.apisoftlimit()
