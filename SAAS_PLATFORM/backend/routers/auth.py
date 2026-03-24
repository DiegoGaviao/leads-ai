from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from AGENTS.agent_scout.facebook_client import FacebookClient
from database import get_supabase_client
import logging
from datetime import datetime
import os
import json
import resend
from services import AICouncilService
from email_templates import get_professional_strategy_email
from market_insights import build_full_insights_block

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
    plan: Optional[str] = None
    email: Optional[str] = ""
    instagram: Optional[str] = ""
    whatsapp: Optional[str] = None
    mission: Optional[str] = ""
    enemy: Optional[str] = ""
    pain: Optional[str] = ""
    dream: Optional[str] = ""
    dreamClient: Optional[str] = ""
    method: Optional[str] = ""
    toneVoice: Optional[str] = None
    brandValues: Optional[str] = None
    offerDetails: Optional[str] = None
    differentiation: Optional[str] = None
    facebook_token: Optional[str] = "manual_entry" 
    instagram_id: Optional[str] = "manual_entry"
    manual_posts: Optional[List[PostEntry]] = None


# Contas internas de teste: bypass da trava de plano gratuito
FREE_PLAN_LIMIT_BYPASS_EMAILS = {
    "drmgaviao@gmail.com",
}
FREE_PLAN_LIMIT_BYPASS_INSTAGRAMS = {
    "strike3_br",
}


def _normalize_plan(plan: Optional[str]) -> str:
    return (plan or "").strip().lower()


def _is_free_or_starter(plan: Optional[str]) -> bool:
    p = _normalize_plan(plan)
    return p in {"free", "starter"}


def _safe_int(value: Optional[str]) -> int:
    try:
        if value is None:
            return 0
        cleaned = str(value).strip()
        return int(cleaned) if cleaned.isdigit() else 0
    except Exception:
        return 0


def _summarize_onboarding(data: OnboardingCompleteRequest) -> dict:
    required_fields = {
        "email": data.email,
        "instagram": data.instagram,
        "mission": data.mission,
        "enemy": data.enemy,
        "pain": data.pain,
        "dream": data.dream,
        "dreamClient": data.dreamClient,
        "method": data.method,
        "toneVoice": data.toneVoice,
        "brandValues": data.brandValues,
        "offerDetails": data.offerDetails,
        "differentiation": data.differentiation,
    }
    missing = []
    for key, value in required_fields.items():
        if value is None:
            missing.append(key)
            continue
        if isinstance(value, str) and not value.strip():
            missing.append(key)

    total_required = len(required_fields)
    filled = total_required - len(missing)
    completion_pct = int((filled / total_required) * 100) if total_required else 0

    posts = data.manual_posts or []
    top_views = max((_safe_int(p.views) for p in posts), default=0)
    top_likes = max((_safe_int(p.likes) for p in posts), default=0)
    links = [p.link for p in posts if p.link][:5]

    return {
        "filled_fields": filled,
        "total_fields": total_required,
        "missing_fields": missing,
        "completion_pct": completion_pct,
        "posts_count": len(posts),
        "top_views": top_views,
        "top_likes": top_likes,
        "post_links": links,
    }


def append_lead_event(
    *,
    brand_id: Optional[str],
    event_type: str,
    email: Optional[str],
    instagram: Optional[str],
    plan: Optional[str],
    payload: Optional[dict] = None,
):
    """
    Append-only log de eventos de lead para monitoramento/RMKT.
    Nunca pode quebrar o fluxo principal.
    """
    try:
        supabase = get_supabase_client()
        event_payload = payload or {}
        supabase.table("leads_ai_lead_events").insert(
            {
                "brand_id": brand_id,
                "event_type": event_type,
                "email": (email or "").strip().lower() or None,
                "instagram_handle": (instagram or "").strip().lower() or None,
                "plan": _normalize_plan(plan) or None,
                "event_payload": event_payload,
            }
        ).execute()
    except Exception:
        logging.warning(
            "lead_events append falhou (nao bloqueante). Verifique se a tabela leads_ai_lead_events existe."
        )


def _build_owner_lead_alert_html(
    *,
    plan: Optional[str],
    email: Optional[str],
    instagram: Optional[str],
    whatsapp: Optional[str],
    posts_count: int,
    top_views: int,
    top_likes: int,
    completion_pct: int,
    filled_fields: int,
    total_fields: int,
    missing_fields: List[str],
    post_links: List[str],
) -> str:
    plan_label = (plan or "nao informado").strip().lower() or "nao informado"
    return f"""
    <html>
      <body style="font-family:Inter,Arial,sans-serif;background:#f8fafc;color:#0f172a;">
        <div style="max-width:640px;margin:0 auto;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;">
          <h2 style="margin:0 0 12px 0;">🔔 Novo onboarding no Leads AI</h2>
          <p style="margin:0 0 16px 0;color:#475569;">
            Um novo lead concluiu o envio de dados no fluxo.
          </p>
          <table style="width:100%;border-collapse:collapse;">
            <tr><td style="padding:6px 0;color:#64748b;">Plano</td><td style="padding:6px 0;"><strong>{plan_label}</strong></td></tr>
            <tr><td style="padding:6px 0;color:#64748b;">Instagram</td><td style="padding:6px 0;"><strong>{instagram or '-'}</strong></td></tr>
            <tr><td style="padding:6px 0;color:#64748b;">E-mail</td><td style="padding:6px 0;"><strong>{email or '-'}</strong></td></tr>
            <tr><td style="padding:6px 0;color:#64748b;">WhatsApp</td><td style="padding:6px 0;"><strong>{whatsapp or '-'}</strong></td></tr>
            <tr><td style="padding:6px 0;color:#64748b;">Checklist preenchido</td><td style="padding:6px 0;"><strong>{filled_fields}/{total_fields} ({completion_pct}%)</strong></td></tr>
            <tr><td style="padding:6px 0;color:#64748b;">Qtd posts enviados</td><td style="padding:6px 0;"><strong>{posts_count}</strong></td></tr>
            <tr><td style="padding:6px 0;color:#64748b;">Melhor view enviada</td><td style="padding:6px 0;"><strong>{top_views}</strong></td></tr>
            <tr><td style="padding:6px 0;color:#64748b;">Melhor like enviado</td><td style="padding:6px 0;"><strong>{top_likes}</strong></td></tr>
          </table>
          <div style="margin-top:14px;padding:12px;border-radius:8px;background:#f8fafc;border:1px solid #e2e8f0;">
            <div style="font-size:12px;color:#64748b;margin-bottom:6px;">Campos faltantes</div>
            <div style="font-size:13px;color:#0f172a;"><strong>{", ".join(missing_fields) if missing_fields else "Nenhum"}</strong></div>
          </div>
          <div style="margin-top:14px;padding:12px;border-radius:8px;background:#f8fafc;border:1px solid #e2e8f0;">
            <div style="font-size:12px;color:#64748b;margin-bottom:6px;">Links de posts enviados</div>
            <div style="font-size:13px;color:#0f172a;line-height:1.5;">
              {"<br>".join(_html.escape(link) for link in post_links) if post_links else "Nenhum link informado"}
            </div>
          </div>
        </div>
      </body>
    </html>
    """


def send_owner_new_lead_alert(
    *,
    plan: Optional[str],
    email: Optional[str],
    instagram: Optional[str],
    whatsapp: Optional[str],
    manual_posts: Optional[List[PostEntry]],
    completion_pct: int,
    filled_fields: int,
    total_fields: int,
    missing_fields: List[str],
):
    """
    Alerta operacional para dono do produto quando um novo onboarding chega.
    Não pode quebrar o fluxo principal: sempre roda em background com fail-safe.
    """
    try:
        owner_email = os.getenv("OWNER_ALERT_EMAIL", "").strip()
        if not owner_email:
            logging.info("OWNER_ALERT_EMAIL não configurado; alerta de lead ignorado.")
            return

        resend.api_key = os.getenv("RESEND_API_KEY") or ""
        if not resend.api_key:
            logging.warning("RESEND_API_KEY ausente; alerta de lead ignorado.")
            return

        from_addr = os.getenv("EMAIL_FROM", "Leads AI <onboarding@resend.dev>")
        posts = manual_posts or []
        top_views = max((_safe_int(p.views) for p in posts), default=0)
        top_likes = max((_safe_int(p.likes) for p in posts), default=0)
        html_body = _build_owner_lead_alert_html(
            plan=plan,
            email=email,
            instagram=instagram,
            whatsapp=whatsapp,
            posts_count=len(posts),
            top_views=top_views,
            top_likes=top_likes,
            completion_pct=completion_pct,
            filled_fields=filled_fields,
            total_fields=total_fields,
            missing_fields=missing_fields,
            post_links=[p.link for p in posts if p.link][:5],
        )
        resp = resend.Emails.send(
            {
                "from": from_addr,
                "to": owner_email,
                "subject": f"🔔 Novo lead: @{instagram or 'sem_handle'} · {completion_pct}% preenchido · {len(posts)} posts",
                "html": html_body,
            }
        )
        logging.info("✅ Alerta de novo lead enviado para %s (%s)", owner_email, resp)
    except Exception:
        logging.exception("❌ Falha ao enviar alerta de novo lead (não bloqueante)")

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
        # Não sobrescrevemos tokens/IDs existentes quando vierem como "manual_entry".
        # Isso evita que o frontend (que às vezes finaliza com manual_entry) apague um OAuth válido.
        la_facebook_access_token = None
        if data.facebook_token and data.facebook_token != "manual_entry":
            la_facebook_access_token = data.facebook_token

        la_instagram_business_id = None
        if data.instagram_id and data.instagram_id != "manual_entry":
            la_instagram_business_id = data.instagram_id

        # Evita quebrar onboarding quando a base não possui colunas de tone/voice.
        tone_voice_value = None
        if data.toneVoice and isinstance(data.toneVoice, str) and data.toneVoice.strip():
            tone_voice_value = data.toneVoice.strip()

        tone_voice_matrix_value = None
        if tone_voice_value:
            tone_voice_matrix_value = {
                "dream": data.dream,
                "dreamClient": data.dreamClient,
                "toneVoice": data.toneVoice,
                "brandValues": data.brandValues,
                "offerDetails": data.offerDetails,
                "differentiation": data.differentiation,
            }

        # 1. Preparar dados para leads_ai_brands
        brand_data = {
            "email": data.email,
            "instagram_handle": data.instagram,
            # Padrão do projeto no Supabase compartilhado: prefixo `la_`.
            # Mantemos semântica igual: persistir token/id para permitir refresh sem reconectar toda vez.
            "la_facebook_access_token": la_facebook_access_token,
            "la_instagram_business_id": la_instagram_business_id,
            "mission": data.mission,
            "enemy": data.enemy,
            "dor_cliente": data.pain,
            "method_name": data.method,
            "dream_point": data.dream,
            "dream_client": data.dreamClient,
            "tone_voice": tone_voice_value,
            "tone_voice_matrix": tone_voice_matrix_value,
        }
        
        # Upsert brand
        # Também removemos campos que podem existir no schema legado, mas que recebam string vazia.
        clean_brand_data = {}
        for k, v in brand_data.items():
            if v is None:
                continue
            if isinstance(v, str) and not v.strip():
                continue
            if k == "tone_voice" and tone_voice_value is None:
                continue
            clean_brand_data[k] = v
        try:
            brand_res = (
                supabase.table("leads_ai_brands")
                .upsert(clean_brand_data, on_conflict="instagram_handle")
                .execute()
            )
        except Exception as upsert_err:
            error_text = str(upsert_err)
            missing_tone_columns = (
                "tone_voice" in error_text
                or "tone_voice_matrix" in error_text
                or "schema cache" in error_text
            )
            if not missing_tone_columns:
                raise

            # Fallback de compatibilidade para bancos ainda sem as colunas novas de tom de voz.
            logging.warning(
                "Schema sem tone_voice/tone_voice_matrix; repetindo upsert sem colunas opcionais. Erro: %s",
                error_text,
            )
            fallback_brand_data = {
                k: v for k, v in clean_brand_data.items()
                if k not in ("tone_voice", "tone_voice_matrix")
            }
            brand_res = (
                supabase.table("leads_ai_brands")
                .upsert(fallback_brand_data, on_conflict="instagram_handle")
                .execute()
            )
        
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
            summary = _summarize_onboarding(data)
            append_lead_event(
                brand_id=brand_id,
                event_type="onboarding_received",
                email=data.email,
                instagram=data.instagram,
                plan=data.plan,
                payload=summary,
            )

            # Alerta operacional de novo lead (não bloqueante, em background).
            background_tasks.add_task(
                send_owner_new_lead_alert,
                plan=data.plan,
                email=data.email,
                instagram=data.instagram,
                whatsapp=data.whatsapp,
                manual_posts=data.manual_posts,
                completion_pct=summary["completion_pct"],
                filled_fields=summary["filled_fields"],
                total_fields=summary["total_fields"],
                missing_fields=summary["missing_fields"],
            )

            # Limite de uso no plano gratuito: 1 geração por conta.
            # Regra não se aplica para contas de teste internas (bypass).
            is_bypass_account = (
                (data.email or "").strip().lower() in FREE_PLAN_LIMIT_BYPASS_EMAILS
                or (data.instagram or "").strip().lower() in FREE_PLAN_LIMIT_BYPASS_INSTAGRAMS
            )
            if _is_free_or_starter(data.plan) and not is_bypass_account:
                existing_strategy = (
                    supabase.table("leads_ai_strategies")
                    .select("id")
                    .eq("brand_id", brand_id)
                    .limit(1)
                    .execute()
                )
                if existing_strategy.data:
                    logging.info(
                        "⛔ Free limit: bloqueado segundo teste para brand_id=%s email=%s instagram=%s",
                        brand_id,
                        data.email,
                        data.instagram,
                    )
                    raise HTTPException(
                        status_code=403,
                        detail=(
                            "Seu periodo de teste gratuito acabou. "
                            "Para continuar evoluindo seus posts com estrategia orientada por dados, "
                            "monitoramento continuo da pagina e novas recomendacoes do conselho de IAs, "
                            "ative um plano pago. "
                            "Com o plano Master voce libera volume maior de roteiros, "
                            "prioridade de processamento e acompanhamento mais profundo de performance."
                        ),
                    )
            
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
            # Dispara geração de estratégia imediatamente no backend para não depender
            # exclusivamente do worker em produção.
            background_tasks.add_task(run_strategy_pipeline, brand_id)
        else:
            logging.error(
                "❌ Onboarding: brand_id ficou None após upsert — pipeline de estratégia/e-mail NÃO foi agendado. "
                "instagram=%s email=%s",
                data.instagram,
                data.email,
            )

        # 3. Disparar Scan em Background (Opcional se for manual_entry, mas enviamos para consistência)
        if data.instagram_id != "manual_entry":
            background_tasks.add_task(run_initial_scan, data.instagram_id, data.facebook_token)
        
        return {
            "success": True,
            "message": "Onboarding completo!",
            "brand_id": brand_id,
            "pipeline_scheduled": bool(brand_id),
        }
        
    except Exception as e:
        logging.error(f"❌ Erro Crítico Onboarding: {str(e)}")
        # Se for erro do Supabase, o e pode ter detalhes
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

async def run_strategy_pipeline(brand_id: str):
    """
    Gera estratégia e envia e-mail em background logo após onboarding.
    Reduz dependência de worker para o cliente receber resposta rápida.
    """
    logging.info("▶ run_strategy_pipeline INICIADO brand_id=%s", brand_id)
    supabase = get_supabase_client()
    resend.api_key = os.getenv("RESEND_API_KEY") or ""
    from_addr = os.getenv("EMAIL_FROM", "Leads AI <onboarding@resend.dev>")

    try:
        brand_res = (
            supabase.table("leads_ai_brands")
            .select("*")
            .eq("id", brand_id)
            .limit(1)
            .execute()
        )
        if not brand_res.data:
            logging.error("❌ run_strategy_pipeline: brand_id não encontrado: %s", brand_id)
            return

        brand = brand_res.data[0]
        email = brand.get("email")

        posts_res = supabase.table("leads_ai_posts").select("*").eq("brand_id", brand_id).execute()
        posts = posts_res.data or []
        posts_context = "Sem histórico de posts disponível."
        if posts:
            posts_context = "\n".join([
                f"- {p.get('permalink')} | Views: {p.get('views')} | Likes: {p.get('likes')} | Comments: {p.get('comments')} | Shares: {p.get('shares')} | Saves: {p.get('saves')}"
                for p in posts
            ])

        tone_matrix = brand.get("tone_voice_matrix", {}) or {}
        if isinstance(tone_matrix, str):
            try:
                tone_matrix = json.loads(tone_matrix)
            except Exception:
                tone_matrix = {}

        briefing_dict = {
            "mission": brand.get("mission") or brand.get("missao", ""),
            "tone_voice": brand.get("tone_voice", tone_matrix.get("toneVoice", "Profissional")),
            "authority": brand.get("authority_proof") or "Especialista",
            "big_promise": brand.get("big_promise", "Transformação"),
            "enemy": brand.get("enemy", ""),
            "pain_point": brand.get("pain_point", brand.get("dor_cliente", "")),
            "desire_point": brand.get("desire_point", tone_matrix.get("dream", "")),
            "method_name": brand.get("method_name", ""),
            "dream_client": brand.get("dream_client") or tone_matrix.get("dreamClient", ""),
            "brand_values": tone_matrix.get("brandValues", ""),
            "offer_details": tone_matrix.get("offerDetails", ""),
            "differentiation": tone_matrix.get("differentiation", ""),
        }

        insights_block = build_full_insights_block(supabase, posts, brand_id)
        logging.info("🧠 run_strategy_pipeline: gerando estratégia para %s", email or brand_id)
        strategy_json = AICouncilService.generate_strategy(briefing_dict, insights_block, posts_context)

        save_payload = {
            "brand_id": brand_id,
            "persona_markdown": strategy_json.get("persona", ""),
            "strategy_markdown": strategy_json.get("estrategia", ""),
            "scripts_json": strategy_json.get("roteiros", []),
        }
        supabase.table("leads_ai_strategies").insert(save_payload).execute()
        append_lead_event(
            brand_id=brand_id,
            event_type="strategy_generated",
            email=email,
            instagram=brand.get("instagram_handle"),
            plan=brand.get("plan"),
            payload={"roteiros_count": len(strategy_json.get("roteiros", []) or [])},
        )

        if not email:
            logging.warning("⚠️ run_strategy_pipeline: sem e-mail para brand_id=%s", brand_id)
            return
        if not resend.api_key:
            logging.error("❌ run_strategy_pipeline: RESEND_API_KEY ausente")
            return

        html_body = get_professional_strategy_email(
            strategy_json.get("persona", ""),
            strategy_json.get("estrategia", ""),
            strategy_json.get("roteiros", []),
        )
        send_res = resend.Emails.send({
            "from": from_addr,
            "to": email,
            "subject": "🎉 Sua Estratégia Leads AI está Pronta!",
            "html": html_body,
        })
        append_lead_event(
            brand_id=brand_id,
            event_type="strategy_email_sent",
            email=email,
            instagram=brand.get("instagram_handle"),
            plan=brand.get("plan"),
            payload={"resend_response": send_res},
        )
        logging.info("✅ run_strategy_pipeline: e-mail enviado (%s) resposta_resend=%s", email, send_res)
    except Exception as e:
        append_lead_event(
            brand_id=brand_id,
            event_type="strategy_pipeline_failed",
            email=None,
            instagram=None,
            plan=None,
            payload={"error": str(e)},
        )
        logging.exception("❌ run_strategy_pipeline falhou para %s", brand_id)

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
        
        # Prepara payload para leads_ai_posts
        # Precisamos do brand_id. Primeiro tentamos colunas com prefixo `la_`.
        brand_res = (
            supabase.table("leads_ai_brands")
            .select("id")
            .eq("la_instagram_business_id", account_id)
            .execute()
        )
        
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
    # Prioriza padrão novo `la_`, com fallback para legado sem prefixo.
    account_id = brand.get("la_instagram_business_id") or brand.get("instagram_business_id")
    token = brand.get("la_facebook_access_token") or brand.get("facebook_access_token")

    if (
        ("la_instagram_business_id" not in brand and "instagram_business_id" not in brand)
        or ("la_facebook_access_token" not in brand and "facebook_access_token" not in brand)
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Schema desatualizado: faltam colunas de auth em leads_ai_brands. "
                "Esperado: la_instagram_business_id/la_facebook_access_token (ou legado sem prefixo)."
            ),
        )

    if not account_id or account_id == "manual_entry":
        raise HTTPException(
            status_code=400,
            detail="instagram_business_id (la_) está vazio. A marca precisa se conectar novamente no onboarding.",
        )

    if not token or token == "manual_entry":
        raise HTTPException(
            status_code=400,
            detail="facebook_access_token (la_) está vazio. A marca precisa se conectar novamente no onboarding.",
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
