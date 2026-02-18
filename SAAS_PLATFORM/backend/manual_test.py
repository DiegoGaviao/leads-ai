import os
import time
import json
import logging
from dotenv import load_dotenv

# Database & Services
from database import get_supabase_client
from services import AICouncilService
import resend
from email_templates import get_professional_strategy_email

# Load Env
load_dotenv()

# Config Resend
resend.api_key = os.getenv("RESEND_API_KEY")
from_addr = os.getenv("EMAIL_FROM", "Leads AI <onboarding@resend.dev>")

print("🚀 INICIANDO MANUAL TEST WORKER...") 

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

supabase = get_supabase_client()

def force_process_all():
    """Busca briefings e gera estratégia independente de já existir."""
    try:
        # Pega todos os briefings
        result = supabase.table('briefings').select('*').execute()
        pending = result.data or []
        
        if pending:
            logger.info(f"Forçando processamento de {len(pending)} briefings.")
            for briefing in pending:
                client_id = briefing['client_id']
                logger.info(f"🚀 Processando Cliente ID: {client_id}")

                try:
                    # 1. Contexto Mockado/Rápido
                    posts_context = "Manual test run context."
                    insights = "Manual test run insights."

                    # 2. Gera a Estratégia
                    briefing_dict = {
                        'mission': briefing.get('mission', ''),
                        'tone_voice': briefing.get('tone_voice', ''),
                        'authority': briefing.get('authority_proof', ''),
                        'big_promise': briefing.get('big_promise', ''),
                        'enemy': briefing.get('enemy', ''),
                        'pain_point': briefing.get('pain_point', ''),
                        'desire_point': briefing.get('desire_point', ''),
                        'method_name': briefing.get('method_name', ''),
                        'dream_client': briefing.get('dream_client', '')
                    }

                    logger.info(f"🧠 Chamando IA...")
                    strategy_json = AICouncilService.generate_strategy(briefing_dict, insights, posts_context)

                    # 3. Salva ou Atualiza
                    logger.info(f"💾 Salvando/Atualizando Estratégia...")
                    # Deleta antiga se houver
                    supabase.table('strategies').delete().eq('client_id', client_id).execute()
                    
                    save_result = supabase.table('strategies').insert({
                        'client_id': client_id,
                        'content_json': strategy_json,
                        'status': 'completed',
                        'model_used': 'manual-test-v1'
                    }).execute()

                    logger.info(f"✅ Estratégia salva!")

                    # 4. Envia E-mail
                    client_info = supabase.table('clients').select('email').eq('id', client_id).execute()
                    if client_info.data:
                        to_email = client_info.data[0]['email']
                        logger.info(f"📧 Enviando e-mail para: {to_email}")
                        
                        # montar corpo de e-mail com conteúdo da estratégia
                        persona = strategy_json.get('persona', '')
                        estrategia = strategy_json.get('estrategia', '')
                        roteiros = strategy_json.get('roteiros', [])

                        html_body = get_professional_strategy_email(persona, estrategia, roteiros)


                        r = resend.Emails.send({
                            "from": from_addr,
                            "to": to_email,
                            "subject": "🎉 Teste Manual: Sua Estratégia está Pronta!",
                            "html": html_body
                        })
                        logger.info(f"✅ Resposta Resend: {r}")

                except Exception as e:
                    logger.error(f"❌ Erro no cliente {client_id}: {e}")
        else:
            logger.info("Nenhum briefing encontrado.")

    except Exception as e:
        logger.error(f"Erro: {e}")

if __name__ == "__main__":
    force_process_all()
