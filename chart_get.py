import yfinance as yf
import mplfinance as mpf

ticker = "7203.T"  # トヨタ
data = yf.Ticker(ticker).history(period="3mo", interval="1d")

data.index.name = 'Date'
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

mpf.plot(
    data,
    type='candle',
    style='yahoo',
    volume=True,
    title=f"{ticker} 日足ローソク足チャート",
    ylabel='株価 (JPY)',
    ylabel_lower='出来高',
    mav=(5, 25),
    figratio=(16, 9),
    figscale=1.2
)
