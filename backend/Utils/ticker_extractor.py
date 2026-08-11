from Utils.ticker_mapping import TICKER_MAP


def extract_tickers(query: str):

    query = query.lower()

    tickers = []

    for company, ticker in TICKER_MAP.items():

        if company in query:

            tickers.append(ticker)

    return list(set(tickers))
