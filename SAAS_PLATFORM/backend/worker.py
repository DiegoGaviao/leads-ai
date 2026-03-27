
import os
import time
import json
import logging
import html as _html
from datetime import datetime
from dotenv import load_dotenv

# Database & Services
from database import get_supabase_client
from services import AICouncilService, align_post_themes, expected_roteiros_for_plan
from services_artisan import apply_strategy_creatives
from market_insights import (
    build_full_insights_block,
    build_client_posts_summary,
    build_anonymous_market_suggestions,
)
import resend
from email_templates import get_professional_strategy_email

# Load Env
load_dotenv()

# Config Resend
resend.api_key = os.getenv("RESEND_API_KEY") or "re_your_api_key_placeholder"
# Usamos onboarding@resend.dev como fallback seguro para testes
from_addr = os.getenv("EMAIL_FROM", "Leads AI <onboarding@resend.dev>")

print("🚀 INICIANDO WORKER LEADS AI (Híbrido - Suporta Schema Novo e Antigo)...") 

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    print("🔗 Carregando Supabase Client...")
    supabase = get_supabase_client()
    print("✅ Supabase Carregado!")
except Exception as e:
    print(f"❌ ERRO FATAL AO CARREGAR SUPABASE: {e}")
    exit(1)

def fetch_pending_briefings_old():
    """Busca briefings antigos que ainda não têm estratégia gerada."""
    try:
        # Pega IDs já processados na tabela de estratégias
        # (Para o schema antigo, salvamos o client_id no campo brand_id da tabela de estratégias)
        existing = supabase.table('leads_ai_strategies').select('brand_id').execute()
        processed_ids = [row['brand_id'] for row in existing.data if row.get('brand_id')] if existing.data else []
        
        result = supabase.table('briefings').select('*').execute()
        all_briefings = result.data or []
        
        # Filtra apenas os que não estão na lista de processados
        pending = [b for b in all_briefings if b['client_id'] not in processed_ids]
        return pending
    except Exception as e:
        logger.error(f"Erro ao buscar briefings antigos: {e}")
        return []

def fetch_pending_brands_new():
    """Busca marcas novas que ainda não têm estratégia gerada."""
    try:
        existing = supabase.table('leads_ai_strategies').select('brand_id').execute()
        processed_ids = [row['brand_id'] for row in existing.data if row.get('brand_id')] if existing.data else []
        
        query = supabase.table('leads_ai_brands').select('*')
        if processed_ids:
            query = query.not_.in_('id', processed_ids)
        result = query.execute()
        return result.data or []
    except Exception as e:
        logger.error(f"Erro ao buscar marcas novas: {e}")
        return []

def process_generic(data, is_old=False):
    """Processa tanto o formato antigo quanto o novo."""
    brand_id = data['id'] if not is_old else data['client_id']
    email = data.get('email')
    
    if is_old and not email:
        # Busca email na tabela clients
        c_res = supabase.table('clients').select('email').eq('id', brand_id).execute()
        if c_res.data:
            email = c_res.data[0]['email']

    print(f"🚀 Processando: {email} (Old Schema: {is_old})")

    try:
        # 1. Contexto de Posts
        posts_context = "Sem histórico de posts disponível."
        posts_list: list = []
        if is_old:
            p_res = supabase.table('analyzed_posts').select('*').eq('client_id', brand_id).execute()
            if p_res.data:
                posts_context = "\n".join([f"- {p.get('post_link')} | Views: {p.get('views')}" for p in p_res.data])
                posts_list = [
                    {
                        "views": p.get("views"),
                        "likes": p.get("likes"),
                        "comments": p.get("comments") or 0,
                        "shares": p.get("shares") or 0,
                        "saves": p.get("saves") or 0,
                        "media_type": "legacy",
                        "permalink": p.get("post_link"),
                    }
                    for p in p_res.data
                ]
        else:
            p_res = supabase.table('leads_ai_posts').select('*').eq('brand_id', brand_id).execute()
            if p_res.data:
                posts_list = p_res.data
                # Incluímos mais sinais além de views para a IA conseguir ajustar ganchos/estrutura com base em retenção e intenção.
                posts_context = "\n".join([
                    f"- {p.get('permalink')} | Views: {p.get('views')} | Likes: {p.get('likes')} | Comments: {p.get('comments')} | Shares: {p.get('shares')} | Saves: {p.get('saves')}"
                    for p in p_res.data
                ])

        # 2. Briefing Dict
        tone_matrix = data.get('tone_voice_matrix', {}) or {}
        if isinstance(tone_matrix, str):
            try: tone_matrix = json.loads(tone_matrix)
            except: tone_matrix = {}

        plan_hint = tone_matrix.get("plan") or data.get("plan")
        n_roteiros = expected_roteiros_for_plan(str(plan_hint) if plan_hint else None)
        post_themes_aligned = align_post_themes(tone_matrix.get("postThemes"), n_roteiros)

        briefing_dict = {
            'mission': data.get('mission') or data.get('missao', ''),
            'tone_voice': data.get('tone_voice', tone_matrix.get('toneVoice', 'Profissional')),
            'authority': data.get('authority_proof') or 'Especialista',
            'big_promise': data.get('big_promise', 'Transformação'),
            'enemy': data.get('enemy', ''),
            'pain_point': data.get('pain_point', data.get('dor_cliente', '')),
            'desire_point': data.get('desire_point', tone_matrix.get('dream', '')),
            'method_name': data.get('method_name', ''),
            'dream_client': data.get('dream_client') or tone_matrix.get('dreamClient', ''),
            'brand_values': tone_matrix.get('brandValues', ''),
            'offer_details': tone_matrix.get('offerDetails', ''),
            'differentiation': tone_matrix.get('differentiation', ''),
            'expected_roteiros': n_roteiros,
            'post_themes': post_themes_aligned,
        }

        # 3. IA (insights = resumo do cliente + sugestões de mercado anônimas)
        print(f"🧠 Gerando Estratégia para {email}...")
        if is_old:
            insights_block = (
                build_client_posts_summary(posts_list)
                + "\n\n"
                + build_anonymous_market_suggestions(supabase, exclude_brand_id=None)
            )
        else:
            insights_block = build_full_insights_block(supabase, posts_list, str(brand_id))
        strategy_json = AICouncilService.generate_strategy(briefing_dict, insights_block, posts_context)
        slug = (data.get("instagram_handle") or "").strip().lstrip("@") or str(brand_id)
        strategy_json = apply_strategy_creatives(strategy_json, briefing_dict, storage_slug=slug)

        # 4. Salva Estratégia
        strategy_id = None
        try:
            # Tenta salvar no banco de dados novo
            # Se for old schema, tentamos vincular se a marca existir. 
            # Se não existir, o insert vai falhar se brand_id for obrigatório e FK violada.
            
            payload = {
                'persona_markdown': strategy_json.get('persona', ''),
                'strategy_markdown': strategy_json.get('estrategia', ''),
                'scripts_json': strategy_json.get('roteiros', []),
            }
            
            # Se is_old, vamos tentar garantir que a brand existe ou salvar sem brand_id se permitido
            # Mas como o worker usa brand_id para filtrar pendentes, precisamos dele.
            
            target_brand_id = brand_id
            if is_old:
                # Verifica se a brand existe na tabela nova
                b_check = supabase.table('leads_ai_brands').select('id').eq('id', brand_id).execute()
                if not b_check.data:
                    # Cria um registro placeholder na tabela nova para satisfazer a FK e o filtro de processados
                    print(f"📦 Criando vínculo de marca para briefing antigo: {brand_id}")
                    supabase.table('leads_ai_brands').insert({
                        'id': brand_id,
                        'email': email,
                        'instagram_handle': data.get('instagram_handle', f"old_{brand_id[:8]}")
                    }).execute()
            
            payload['brand_id'] = target_brand_id
            
            res = supabase.table('leads_ai_strategies').insert(payload).execute()
            if res.data:
                strategy_id = res.data[0]['id']
                print(f"💾 Estratégia salva no banco! ID: {strategy_id}")
        except Exception as db_err:
            logger.warning(f"⚠️ Aviso: Não foi possível salvar estratégia no banco: {db_err}")

        # 5. E-mail
        if email:
            try:
                print(f"📧 Preparando envio de e-mail para {email}...")
                html_body = get_professional_strategy_email(
                    strategy_json.get('persona', ''),
                    strategy_json.get('estrategia', ''),
                    strategy_json.get('roteiros', [])
                )
                res_email = resend.Emails.send({
                    "from": from_addr,
                    "to": email,
                    "subject": "🎉 Sua Estratégia Leads AI está Pronta!",
                    "html": html_body
                })
                print(f"✅ E-mail enviado com sucesso para {email}! ID: {res_email}")
                print(f"📢 NOTIFICAÇÃO ADMIN: Estratégia enviada para {email} (Instagram: {data.get('instagram_handle', 'N/A')})")
            except Exception as email_err:
                logger.error(f"❌ Erro ao enviar e-mail para {email}: {email_err}")

        # Marcar como processado (Para evitar loops infinitos caso o INSERT no banco falhe)
        # TODO: Implementar coluna 'processed' ou similar se necessário.
        # Por enquanto, se for is_old, vamos apenas logar que terminamos.

    except Exception as e:
        logger.error(f"❌ Erro Crítico ao processar {email}: {e}")

def run_worker():
    while True:
        try:
            # Tenta Novo
            new_brands = fetch_pending_brands_new()
            if new_brands: print(f"🔍 Encontradas {len(new_brands)} marcas exclusivas.")
            for b in new_brands:
                process_generic(b, is_old=False)
            
            # Tenta Antigo
            old_briefings = fetch_pending_briefings_old()
            if old_briefings: print(f"🔍 Encontrados {len(old_briefings)} briefings antigos.")
            for b in old_briefings:
                process_generic(b, is_old=True)
                
            time.sleep(10)
        except KeyboardInterrupt: break
        except Exception as e:
            logger.error(f"Erro Loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    run_worker()
