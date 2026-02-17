from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from AGENTS.agent_scout.facebook_client import FacebookClient
from database import get_supabase_client
import logging
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])
fb_client = FacebookClient()

class AuthExchangeRequest(BaseModel):
    access_token: str # Aqui recebemos o CODE do frontend

class OnboardingCompleteRequest(BaseModel):
    email: str
    instagram: str
    whatsapp: Optional[str] = None
    mission: str
    enemy: str
    pain: str
    method: Optional[str] = None
    facebook_token: str # Token Long-Lived já trocado (ou Code, se quisermos trocar aqui)
    instagram_id: str

@router.post("/facebook/exchange")
async def exchange_token(req: AuthExchangeRequest):
    """
    Simula a troca do CODE por Token (No MVP, o front manda o token direto ou o code)
    Para produção real, aqui usaríamos APP_ID + APP_SECRET para trocar o code por token seguro.
    Como estamos em MVP e o front já está mandando o code, vamos assumir que:
    1. Se vier code, trocamos (TODO).
    2. Se vier token, validamos.
    """
    logging.info(f"🔄 Trocando token... {req.access_token[:5]}***")
    
    # Busca contas para validar o token
    try:
        # Se o token for válido, retorna as contas
        accounts = fb_client.get_instagram_accounts(req.access_token)
        if not accounts:
            return {"success": False, "message": "Nenhuma conta Instagram Business encontrada."}
            
        return {
            "success": True, 
            "token": req.access_token, # Retorna o mesmo token (MVP)
            "accounts": accounts
        }
    except Exception as e:
        logging.error(f"❌ Erro Auth: {e}")
        return {"success": False, "message": str(e)}

@router.post("/onboarding/complete")
async def complete_onboarding(data: OnboardingCompleteRequest, background_tasks: BackgroundTasks):
    """
    Salva a marca no Supabase e dispara o background scan.
    """
    logging.info(f"🚀 Criando marca: {data.instagram}")
    supabase = get_supabase_client()
    
    try:
        # 1. Upsert da Marca (Usa email ou instagram como chave, idealmente email)
        brand_data = {
            "email": data.email,
            "instagram_username": data.instagram, # Ajuste nome coluna
            "whatsapp": data.whatsapp,
            "missao": data.mission,
            "inimigo_publico": data.enemy, # Ajuste nome coluna
            "dor_cliente": data.pain,
            "metodo_proprio": data.method, # Ajuste nome coluna
            "facebook_access_token": data.facebook_token,
            "instagram_business_id": data.instagram_id
            # "created_at": datetime.now().isoformat()
        }
        
        # Tenta inserir. Se der conflito no User ID (que não temos), usamos service role.
        # No MVP sem Auth, a tabela deve permitir public insert ou usamos a service_role key no backend.
        # Vamos assumir que a tabela permite anon insert por enquanto para teste.
        
        res = supabase.table("leads_ai_brands").upsert(brand_data, on_conflict="instagram_username").execute()
        
        # 2. Disparar Scan em Background (Agente 01)
        background_tasks.add_task(run_initial_scan, data.instagram_id, data.facebook_token)
        
        return {"success": True, "message": "Marca criada e scan iniciado."}
        
    except Exception as e:
        logging.error(f"❌ Erro Onboarding: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_initial_scan(account_id: str, token: str):
    """
    Função Background: Baixa posts e salva na tabela de posts.
    """
    logging.info(f"🕵️ Agente 01 (Scout): Iniciando scan para {account_id}")
    supabase = get_supabase_client()
    
    try:
        posts = fb_client.get_posts_data(account_id, token, limit=12)
        logging.info(f"📸 {len(posts)} posts baixados. Salvando no banco...")
        
        # Prepara Payload para leads_ai_posts
        # Precisamos do brand_id. Vamos buscar pelo instagram_business_id
        brand_res = supabase.table("leads_ai_brands").select("id").eq("instagram_business_id", account_id).execute()
        
        if not brand_res.data:
            logging.error("❌ Marca não encontrada para salvar posts.")
            return
            
        brand_id = brand_res.data[0]['id']
        
        db_posts = []
        for p in posts:
            db_posts.append({
                "brand_id": brand_id,
                "external_id": p['external_id'],
                "media_type": p['type'],
                "caption": p['full_caption'],
                "permalink": p['link'],
                "timestamp": p['date'],
                "likes": p['likes'],
                "comments": p['comments'],
                "shares": p['shares'],
                "saves": p['saves'],
                "views": p['views'],
                "engagement_score": p['interactions'] # Simples soma
            })
            
        # Bulk Insert
        if db_posts:
            supabase.table("leads_ai_posts").upsert(db_posts, on_conflict="external_id").execute()
            logging.info("✅ Posts salvos com sucesso!")
            
    except Exception as e:
        logging.error(f"❌ Falha no Scan Background: {e}")
