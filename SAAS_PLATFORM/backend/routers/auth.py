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

class MasterNotifyRequest(BaseModel):
    contactMethod: str
    contactValue: str
    fbEmail: str

class PostEntry(BaseModel):
    link: str
    views: str
    likes: str
    comments: Optional[str] = None

class OnboardingCompleteRequest(BaseModel):
    email: str
    instagram: str
    whatsapp: Optional[str] = None
    mission: str
    enemy: str
    pain: str
    dream: Optional[str] = None
    dreamClient: Optional[str] = None
    method: Optional[str] = None
    facebook_token: str 
    instagram_id: str
    manual_posts: Optional[List[PostEntry]] = None

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

@router.post("/master/notify")
async def notify_master(data: MasterNotifyRequest):
    """
    Notifica o admin sobre um novo interesse no plano Master.
    """
    msg = f"💎 NOVO LEAD MASTER DATA!\nContato: {data.contactValue} ({data.contactMethod})\nFB Login Email: {data.fbEmail}"
    logging.info(msg)
    
    # No futuro, integrar com Slack ou Bot de WhatsApp aqui
    print(f"\n📢 AVISO PARA DIEGO: {msg}\n")
    
    return {"success": True}

@router.post("/onboarding/complete")
async def complete_onboarding(data: OnboardingCompleteRequest, background_tasks: BackgroundTasks):
    """
    Salva a marca no Supabase e os posts manuais se existirem.
    """
    logging.info(f"🚀 Criando marca (Modo Fluxo PDF): {data.instagram}")
    supabase = get_supabase_client()
    
    try:
        # 1. Preparar dados para leads_ai_brands
        brand_data = {
            "email": data.email,
            "instagram_handle": data.instagram,
            "mission": data.mission,
            "enemy": data.enemy,
            "dor_cliente": data.pain,
            "method_name": data.method,
            "tone_voice_matrix": {
                "dream": data.dream,
                "dreamClient": data.dreamClient
            }
        }
        
        # Upsert brand
        clean_brand_data = {k: v for k, v in brand_data.items() if v is not None}
        brand_res = supabase.table("leads_ai_brands").upsert(clean_brand_data, on_conflict="instagram_handle").execute()
        
        if brand_res.data:
            brand_id = brand_res.data[0]['id']
            
            # 2. Salvar Posts Manuais se houver
            if data.manual_posts:
                db_posts = []
                for p in data.manual_posts:
                    db_posts.append({
                        "brand_id": brand_id,
                        "permalink": p.link,
                        "views": int(p.views) if p.views.isdigit() else 0,
                        "likes": int(p.likes) if p.likes.isdigit() else 0,
                        "comments": int(p.comments) if p.comments and p.comments.isdigit() else 0,
                        "external_id": f"manual_{datetime.now().timestamp()}_{p.link[:20]}"
                    })
                
                if db_posts:
                    supabase.table("leads_ai_posts").upsert(db_posts, on_conflict="external_id").execute()
                    logging.info(f"✅ {len(db_posts)} posts manuais salvos.")

        # 3. Disparar Scan em Background (Opcional se for manual_entry, mas enviamos para consistência)
        if data.instagram_id != "manual_entry":
            background_tasks.add_task(run_initial_scan, data.instagram_id, data.facebook_token)
        
        return {"success": True, "message": "Onboarding completo!"}
        
    except Exception as e:
        logging.error(f"❌ Erro Onboarding: {e}")
        raise HTTPException(status_code=500, detail=str(e))
async def run_initial_scan(account_id: str, token: str):
    """
    Função Background: Baixa posts e salva na tabela de posts.
    """
    if account_id == "manual_skip":
        logging.info("⏩ Scan pulado (Modo Manual)")
        return

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
