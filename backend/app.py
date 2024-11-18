from fastapi import FastAPI
from backend.api.trading import trading_router

app = FastAPI()

# Inclui as rotas da API de trading
app.include_router(trading_router, prefix="/api/trading")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



