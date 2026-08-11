from services.Market_Service import MarketService

market = MarketService()

history = market.get_history("AAPL")

print(history.head())

print("Current Price - > ")
print(market.get_current_price("AAPL"))

info = market.get_company_info("AAPL")
print("Company Info -> ")
print(info["longName"])
print(info["sector"])
print(info["industry"])

print("Volatility - > ")
print(market.calculate_volatility("AAPL"))


symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "BTC-USD"]

for symbol in symbols:

    print(symbol, "->", market.calculate_volatility(symbol))

market = MarketService()

# symbols = extract_tickers(query)

market.compare_assets(symbols)
