from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union
import json
import logging

from database import get_supabase_client
from services import AICouncilService

# Includes
from routers import auth

app = FastAPI(
    title="Leads AI V2 - Backend (Supabase Integrated)",
    description="Motor de Inteligência do Conselho de IAs com Banco SQL",
    version="2.1.0"
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "2.1.2",
        "api": "Leads AI V2 Backend"
    }

# Includes Router do Auth
app.include_router(auth.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_strategy(req: OnboardingRequest, authorization: Optional[str] = Header(None)):
    """
    Endpoint LEGADO/MANUAL.
    Aceita posts enviados diretamente pelo Front (Upload de CSV ou Manual).
    Ainda útil para testes rápidos sem conexão real.
    """
    logging.info(f"🚀 Iniciando Análise Manual para: {req.instagram}")
    
    try:
        # 1. Transformar posts em CSV para o Analista DeepSeek
        csv_data = "Tema,Views,Likes,Saves,Comments\n"
        for p in req.posts:
            # Higienização básica
            v = str(p.views).replace(".", "").replace(",", "")
            l = str(p.likes).replace(".", "").replace(",", "")
            s = str(p.saves).replace(".", "").replace(",", "")
            c = str(p.comments).replace(".", "").replace(",", "")
            csv_data += f"{p.tema},{v},{l},{s},{c}\n"
        
        # 2. Insights Numéricos (Agente 04 - Analista)
        logging.info("🤖 Chamando Agente 04 (Analista)...")
        insights = AICouncilService.analyze_data(csv_data)
        
        # 3. Geração de Estratégia (Agente 05 - Conselho)
        logging.info("🧠 Chamando Agente 05 (Conselho Criativo)...")
        briefing = {
            "missao": req.missao,
            "inimigo": req.inimigo,
            "dor_cliente": req.dor_cliente,
            "metodo_nome": req.metodo_nome,
            "instagram": req.instagram
        }
        
        strategy_result = AICouncilService.generate_strategy(briefing, insights, csv_data)
               
        return {
            "success": True,
            "data": strategy_result
        }
        
    except Exception as e:
        logging.error(f"❌ Erro no Processamento: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# Novo Endpoint para rodar o Scout via Agendamento/Manual
@app.get("/agents/scout/scan")
async def manual_scan(account_id: str, token: str):
    from routers.auth import run_initial_scan
    await run_initial_scan(account_id, token)
    return {"status": "Scan started in background"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
