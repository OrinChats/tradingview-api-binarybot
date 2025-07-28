from fastapi import FastAPI
import os
import httpx

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.get("/")
def root():
    return {"status": "API rodando com sucesso 🎉"}

@app.get("/analisar")
async def analisar():
    prompt = """
    Você é um analista financeiro. Me diga o sentimento atual do mercado com base nos dados de análise técnica do gráfico de BTC/USDT no TradingView. 
    Considere padrões de velas, RSI, MACD, volume e tendências.
    """

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "Você é um analista técnico especialista em criptomoedas."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 600
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        data = response.json()
        resposta = data["choices"][0]["message"]["content"]
        return {"analise": resposta}
    else:
        return {
            "erro": f"Erro ao consultar a Groq API",
            "detalhes": response.text
        }
