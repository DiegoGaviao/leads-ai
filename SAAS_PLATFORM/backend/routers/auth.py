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
    access_token: str  # MVP: o frontend envia o `code` aqui (nome mantido por compatibilidade)
    redirect_uri: Optional[str] = None

class MasterNotifyRequest(BaseModel):
    contactMethod: str
    contactValue: str
    fbEmail: str

class PostEntry(BaseModel):
    link: str
    views: str
    likes: str
    comments: Optional[str] = "0"
    shares: Optional[str] = "0"
    saves: Optional[str] = "0"
    conversions: Optional[str] = "0"

class OnboardingCompleteRequest(BaseModel):
    email: Optional[str] = ""
    instagram: Optional[str] = ""
    whatsapp: Optional[str] = None
    mission: Optional[str] = ""
    enemy: Optional[str] = ""
    pain: Optional[str] = ""
    dream: Optional[str] = ""
    dreamClient: Optional[str] = ""
    method: Optional[str] = ""
    toneVoice: Optional[str] = ""
    brandValues: Optional[str] = ""
    offerDetails: Optional[str] = ""
    differentiation: Optional[str] = ""
    facebook_token: Optional[str] = "manual_entry" 
    instagram_id: Optional[str] = "manual_entry"
    manual_posts: Optional[List[PostEntry]] = None

class RefreshPostsRequest(BaseModel):
    instagram_handle: str
    limit: Optional[int] = 12
    regen_strategy: Optional[bool] = True

@router.post("/facebook/exchange")
async def exchange_token(req: AuthExchangeRequest):
    """
    Simula a troca do CODE por Token (No MVP, o front manda o token direto ou o code)
    Para produção real, aqui usaríamos APP_ID + APP_SECRET para trocar o code por token seguro.
    Como estamos em MVP e o front já está mandando o code, vamos assumir que:
    1. Se vier code, trocamos (TODO).
    2. Se vier token, validamos.
    """
    logging.info(f"🔄 Trocando OAuth code... {req.access_token[:5]}***")

    if not req.redirect_uri:
        return {
            "success": False,
            "message": "redirect_uri é obrigatório para trocar o code por access_token.",
        }

    # Troca code -> access_token (OAuth real)
    try:
        token = fb_client.exchange_code_for_access_token(req.access_token, req.redirect_uri)
    except Exception as e:
        logging.error(f"❌ Erro ao trocar code por token: {e}")
        return {"success": False, "message": str(e)}
    
    # Busca contas para validar o token
    try:
        # Se o token for válido, retorna as contas
        accounts = fb_client.get_instagram_accounts(token)
        if not accounts:
            return {"success": False, "message": "Nenhuma conta Instagram Business encontrada."}
            
        return {
            "success": True, 
            "token": token,
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
    logging.info(f"🚀 Recebendo Onboarding: {data.instagram} | Posts: {len(data.manual_posts) if data.manual_posts else 0}")
    logging.info(f"Payload: {data.dict()}")
    supabase = get_supabase_client()
    
    try:
        # 1. Preparar dados para leads_ai_brands
        brand_data = {
            "email": data.email,
            "instagram_handle": data.instagram,
            # Persistimos para permitir refresh sem precisar reautorizar o cliente.
            # Se ela já conectou antes, esse campo pode estar vazio e será necessário reconectar 1x.
            "facebook_access_token": data.facebook_token,
            "instagram_business_id": data.instagram_id,
            "mission": data.mission,
            "enemy": data.enemy,
            "dor_cliente": data.pain,
            "method_name": data.method,
            "dream_point": data.dream,
            "dream_client": data.dreamClient,
            "tone_voice": data.toneVoice,
            "tone_voice_matrix": {
                "dream": data.dream,
                "dreamClient": data.dreamClient,
                "toneVoice": data.toneVoice,
                "brandValues": data.brandValues,
                "offerDetails": data.offerDetails,
                "differentiation": data.differentiation
            }
        }
        
        # Upsert brand
        clean_brand_data = {k: v for k, v in brand_data.items() if v is not None}
        brand_res = supabase.table("leads_ai_brands").upsert(clean_brand_data, on_conflict="instagram_handle").execute()
        
        logging.info(f"Brand Res: {brand_res.data}")
        
        brand_id = None
        if brand_res.data:
            brand_id = brand_res.data[0]['id']
        else:
            # Fallback: Se o upsert não retornou dados, tenta buscar pelo handle
            fallback_res = supabase.table("leads_ai_brands").select("id").eq("instagram_handle", data.instagram).execute()
            if fallback_res.data:
                brand_id = fallback_res.data[0]['id']

        if brand_id:
            
            # 2. Salvar Posts Manuais se houver
            if data.manual_posts:
                db_posts = []
                for p in data.manual_posts:
                    db_posts.append({
                        "brand_id": brand_id,
                        "permalink": p.link,
                        "views": int(p.views) if p.views and p.views.isdigit() else 0,
                        "likes": int(p.likes) if p.likes and p.likes.isdigit() else 0,
                        "comments": int(p.comments) if p.comments and p.comments.isdigit() else 0,
                        "shares": int(p.shares) if p.shares and p.shares.isdigit() else 0,
                        "saves": int(p.saves) if p.saves and p.saves.isdigit() else 0,
                        "conversions": int(p.conversions) if p.conversions and p.conversions.isdigit() else 0,
                        "external_id": f"manual_{datetime.now().timestamp()}_{p.link[:20]}"
                    })
                
                if db_posts:
                    post_res = supabase.table("leads_ai_posts").upsert(db_posts, on_conflict="external_id").execute()
                    logging.info(f"✅ Posts Res: {len(post_res.data)} posts salvos.")

            # 3. Limpar estratégia antiga (se existir) para forçar o worker a gerar uma nova
            # Isso resolve o problema de preencher 2x e o worker ignorar a segunda vez.
            supabase.table("leads_ai_strategies").delete().eq("brand_id", brand_id).execute()
            logging.info(f"♻️ Estratégias antigas limpas para {data.instagram}. Worker será acionado.")

        # 3. Disparar Scan em Background (Opcional se for manual_entry, mas enviamos para consistência)
        if data.instagram_id != "manual_entry":
            background_tasks.add_task(run_initial_scan, data.instagram_id, data.facebook_token)
        
        return {"success": True, "message": "Onboarding completo!"}
        
    except Exception as e:
        logging.error(f"❌ Erro Crítico Onboarding: {str(e)}")
        # Se for erro do Supabase, o e pode ter detalhes
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")
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


@router.post("/posts/refresh")
async def refresh_posts(req: RefreshPostsRequest):
    """
    Re-roda o Scout para atualizar a base de posts do cliente.
    - Usa token/account_id persistidos em `leads_ai_brands` (após re-conexão 1x).
    - Opcional: apaga a estratégia atual para forçar reprocessamento pelo worker.
    """
    supabase = get_supabase_client()

    try:
        # Selecionamos todas as colunas para não quebrar em ambientes com schema antigo.
        # Se os campos de token/id não existirem, tratamos com erro 400 mais claro abaixo.
        brand_res = (
            supabase.table("leads_ai_brands")
            .select("*")
            .eq("instagram_handle", req.instagram_handle)
            .execute()
        )
    except Exception as e:
        logging.error(f"❌ Erro ao buscar marca para refresh: {e}")
        raise HTTPException(
            status_code=500,
            detail="Falha ao consultar leads_ai_brands. Verifique se a migration de auth foi aplicada.",
        )

    if not brand_res.data:
        raise HTTPException(status_code=404, detail="Marca não encontrada para este instagram_handle.")

    brand = brand_res.data[0]
    brand_id = brand.get("id")
    account_id = brand.get("instagram_business_id")
    token = brand.get("facebook_access_token")

    if "instagram_business_id" not in brand or "facebook_access_token" not in brand:
        raise HTTPException(
            status_code=400,
            detail="Schema desatualizado: faltam colunas instagram_business_id/facebook_access_token em leads_ai_brands. Rode a migration 02_auth_migration.sql.",
        )

    if not account_id or account_id == "manual_entry":
        raise HTTPException(
            status_code=400,
            detail="instagram_business_id está vazio. A marca precisa se conectar novamente no onboarding.",
        )

    if not token or token == "manual_entry":
        raise HTTPException(
            status_code=400,
            detail="facebook_access_token está vazio. A marca precisa se conectar novamente no onboarding.",
        )

    try:
        # 1) Re-scan dos posts e upsert na tabela leads_ai_posts.
        posts = fb_client.get_posts_data(account_id, token, limit=req.limit or 12)
        logging.info(f"🕵️ Re-scan iniciado ({req.instagram_handle}) - {len(posts)} posts")

        db_posts = []
        for p in posts:
            db_posts.append({
                "brand_id": brand_id,
                "external_id": p["external_id"],
                "media_type": p.get("type", ""),
                "caption": p.get("full_caption", ""),
                "permalink": p.get("link", ""),
                "timestamp": p.get("date"),
                "likes": p.get("likes", 0),
                "comments": p.get("comments", 0),
                "shares": p.get("shares", 0),
                "saves": p.get("saves", 0),
                "views": p.get("views", 0),
                "engagement_score": p.get("interactions", 0),
            })

        if db_posts:
            supabase.table("leads_ai_posts").upsert(db_posts, on_conflict="external_id").execute()

        # 2) Opcional: regen estratégia (apaga estratégia atual para o worker refazer)
        if req.regen_strategy and brand_id:
            supabase.table("leads_ai_strategies").delete().eq("brand_id", brand_id).execute()

    except Exception as e:
        logging.error(f"❌ Falha no refresh_posts ({req.instagram_handle}): {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Falha ao atualizar posts/estratégia. Verifique schema/tokens da marca. Erro: {str(e)}",
        )

    return {"success": True, "brand_id": brand_id, "posts_upserted": len(db_posts or [])}
