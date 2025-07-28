from fastapi import FastAPI, Request
import ccxt
import datetime

app = FastAPI()

@app.post("/obter-candles")
async def obter_candles(request: Request):
    body = await request.json()
    pair = body["pair"].replace("/", "")  # Ex: BTC/USDT → BTCUSDT
    timeframe = body["timeframe"]

    # Define o intervalo do gráfico
    timeframe_map = {
        "1": "1m",
        "5": "5m"
    }

    exchange = ccxt.binance()
    candles_raw = exchange.fetch_ohlcv(pair, timeframe=timeframe_map[timeframe], limit=20)

    candles = []
    for c in candles_raw:
        candles.append({
            "time": datetime.datetime.utcfromtimestamp(c[0] / 1000).isoformat(),
            "open": c[1],
            "high": c[2],
            "low": c[3],
            "close": c[4]
        })

    return {
        "pair": body["pair"],
        "timeframe": timeframe,
        "candles": candles
    }
