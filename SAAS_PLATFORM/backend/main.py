from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union
import json
import logging
import sys

# Render / Docker: sem isso, logging.info do routers/auth não aparece nos logs (nível padrão WARNING).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    stream=sys.stdout,
    force=True,
)

from database import get_supabase_client
from services import AICouncilService
from services_artisan import apply_strategy_creatives

# Includes
from routers import auth

app = FastAPI(
    title="Leads AI - Backend (Supabase Integrated)",
    description="Motor de Inteligência do Conselho de IAs com Banco SQL",
    version="3.0.0"
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "2.1.2",
        "api": "Leads AI V2 Backend"
    }

@app.head("/")
async def root_head():
    return


@app.get("/health/ready")
@app.get("/ready")  # alias curto (mesma resposta)
async def health_ready():
    """
    Diagnóstico seguro: só indica se variáveis críticas estão definidas (sem expor valores).
    Use para checar Render antes do teste ponta a ponta.
    """
    import os

    has_supabase = bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"))
    has_resend = bool(os.getenv("RESEND_API_KEY"))
    has_email_from = bool(os.getenv("EMAIL_FROM"))
    has_deepseek = bool(os.getenv("DEEPSEEK_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    can_generate = has_deepseek or has_openai
    creatives_on = (os.getenv("LEADS_AI_GENERATE_CREATIVES") or "true").strip().lower() in (
        "1", "true", "yes", "on",
    )
    creatives_possible = bool(has_openai and creatives_on)

    return {
        "status": "ok",
        "checks": {
            "supabase": has_supabase,
            "resend": has_resend,
            "email_from_configured": has_email_from,
            "deepseek": has_deepseek,
            "openai": has_openai,
            "strategy_generation_possible": can_generate,
            "image_creatives_possible": creatives_possible,
            "creatives_bucket": (os.getenv("LEADS_AI_CREATIVES_BUCKET") or "leads-ai-creatives").strip(),
        },
        "email_delivery_possible": has_resend and has_email_from,
        "ready_for_onboarding_e2e": has_supabase and can_generate and has_resend and has_email_from,
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

# Modelos Pydantic (Entrada de Dados)
class ToneOfVoice(BaseModel):
    nao_sou: str
    sou: str

class PostData(BaseModel):
    tema: str
    views: Union[str, int]
    likes: Union[str, int] = 0
    saves: Union[str, int] = 0
    comments: Union[str, int] = 0

class OnboardingRequest(BaseModel):
    instagram: str
    email: str
    missao: str
    inimigo: str
    dor_cliente: str
    metodo_nome: str
    posts: List[PostData]

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
        ig = (req.instagram or "").strip().lstrip("@")
        briefing = {
            "mission": req.missao,
            "tone_voice": "Profissional",
            "authority": "Criador de conteúdo",
            "big_promise": "Resultados com conteúdo estratégico",
            "enemy": req.inimigo,
            "pain_point": req.dor_cliente,
            "desire_point": "",
            "method_name": req.metodo_nome,
            "dream_client": f"Seguidores e leads do @{ig}" if ig else "Público no Instagram",
        }

        strategy_result = AICouncilService.generate_strategy(briefing, insights, csv_data)
        strategy_result = apply_strategy_creatives(
            strategy_result, briefing, storage_slug=ig or req.email or "manual"
        )

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
