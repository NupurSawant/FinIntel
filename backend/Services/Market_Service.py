import numpy as np
import yfinance as yf


class MarketService:

    def get_history(self, symbol, period="1y"):
        stock = yf.Ticker(symbol)
        return stock.history(period=period)

    def get_current_price(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.fast_info["lastPrice"]

    def get_company_info(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.info

    def calculate_volatility(self, symbol, period="1y"):

        history = self.get_history(symbol, period)

        returns = history["Close"].pct_change()

        volatility = returns.std() * np.sqrt(252)

        return round(volatility * 100, 2)

    def compare_assets(self, symbols):

        results = []

        for symbol in symbols:

            try:

                volatility = self.calculate_volatility(symbol)

                current_price = self.get_current_price(symbol)

                results.append(
                    {
                        "symbol": symbol,
                        "price": round(current_price, 2),
                        "volatility": volatility,
                    }
                )
            except Exception as e:

                results.append({"symbol": symbol, "error": str(e)})

        return results
