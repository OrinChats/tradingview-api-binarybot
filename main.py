from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # coloque no .env se estiver localmente

@app.post("/predict")
async def predict(request: Request):
    body = await request.json()
    candles = body.get("candles", [])

    if not candles:
        return {"error": "No candles provided"}

    prompt = f"""
Você é um analista técnico de opções binárias. Com base nos candles a seguir do par BTC/USDT ou ETH/USDT (timeframe 1 minuto), diga se a próxima vela será de alta (verde) ou baixa (vermelha), e a confiança da previsão de 0 a 100%.

Candles:
{candles}

Responda apenas no formato JSON:
{{
  "direcao": "alta" ou "baixa",
  "confianca": 0 a 100
}}
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
        )

        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return {"resposta": reply}
