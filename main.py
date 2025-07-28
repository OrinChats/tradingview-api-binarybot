from fastapi import FastAPI, Request
from tvDatafeed import TvDatafeed, Interval

app = FastAPI()
tv = TvDatafeed()  # sem login

@app.post("/obter-candles")
async def obter_candles(request: Request):
    body = await request.json()
    symbol = body['pair'].replace("/", "")
    timeframe = body['timeframe']

    map_tf = {
        "1": Interval.in_1_minute,
        "5": Interval.in_5_minute
    }

    df = tv.get_hist(symbol=symbol, exchange='BINANCE', interval=map_tf[timeframe], n_bars=20)
    candles = df.reset_index()[['open', 'high', 'low', 'close']].to_dict(orient='records')

    return {
        "pair": body['pair'],
        "timeframe": timeframe,
        "candles": candles
    }
