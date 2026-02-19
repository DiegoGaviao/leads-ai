
import os
import time
import json
import logging
import html as _html
from datetime import datetime
from dotenv import load_dotenv

# Database & Services
from database import get_supabase_client
from services import AICouncilService
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
        if is_old:
            p_res = supabase.table('analyzed_posts').select('*').eq('client_id', brand_id).execute()
            if p_res.data:
                posts_context = "\n".join([f"- {p.get('post_link')} | Views: {p.get('views')}" for p in p_res.data])
        else:
            p_res = supabase.table('leads_ai_posts').select('*').eq('brand_id', brand_id).execute()
            if p_res.data:
                posts_context = "\n".join([f"- {p.get('permalink')} | Views: {p.get('views')}" for p in p_res.data])

        # 2. Briefing Dict
        tone_matrix = data.get('tone_voice_matrix', {}) or {}
        if isinstance(tone_matrix, str):
            try: tone_matrix = json.loads(tone_matrix)
            except: tone_matrix = {}

        briefing_dict = {
            'mission': data.get('mission') or data.get('missao', ''),
            'tone_voice': data.get('tone_voice', 'Profissional'),
            'authority': data.get('authority_proof') or 'Especialista',
            'big_promise': data.get('big_promise', 'Transformação'),
            'enemy': data.get('enemy', ''),
            'pain_point': data.get('pain_point', data.get('dor_cliente', '')),
            'desire_point': data.get('desire_point', tone_matrix.get('dream', '')),
            'method_name': data.get('method_name', ''),
            'dream_client': data.get('dream_client') or tone_matrix.get('dreamClient', '')
        }

        # 3. IA
        print(f"🧠 Gerando Estratégia para {email}...")
        strategy_json = AICouncilService.generate_strategy(briefing_dict, "Análise de DNA", posts_context)

        # 4. Salva Estratégia (Sempre no schema novo para unificar o rastreamento)
        supabase.table('leads_ai_strategies').insert({
            'brand_id': brand_id, # Usamos este campo para marcar como "já gerado" tanto para old quanto new
            'persona_markdown': strategy_json.get('persona', ''),
            'strategy_markdown': strategy_json.get('estrategia', ''),
            'scripts_json': strategy_json.get('roteiros', []),
        }).execute()

        # 5. E-mail
        if email:
            html_body = get_professional_strategy_email(
                strategy_json.get('persona', ''),
                strategy_json.get('estrategia', ''),
                strategy_json.get('roteiros', [])
            )
            resend.Emails.send({
                "from": from_addr,
                "to": email,
                "subject": "🎉 Sua Estratégia Leads AI está Pronta!",
                "html": html_body
            })
            print(f"✅ E-mail enviado com sucesso para {email}!")
            print(f"📢 NOTIFICAÇÃO ADMIN: Estratégia gerada e enviada para {email} (Marca: {data.get('instagram_handle', 'N/A')})")

        # Marcar como notificado (Old Schema) - Omitido pois a coluna status não existe
        # if is_old:
        #     supabase.table('briefings').update({'status': 'notified'}).eq('id', data['id']).execute()

    except Exception as e:
        logger.error(f"❌ Erro ao processar {email}: {e}")

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
