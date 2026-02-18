import os
import sys
import json
import logging
import argparse
import traceback
from dotenv import load_dotenv

from database import get_supabase_client
from services import AICouncilService
import resend

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def process_client(client_id: str):
    supabase = get_supabase_client()
    try:
        briefing_res = supabase.table('briefings').select('*').eq('client_id', client_id).execute()
        if not briefing_res.data:
            logger.error(f"Nenhum briefing encontrado para client_id={client_id}")
            return

        briefing = briefing_res.data[0]
        logger.info(f"Processando briefing para client_id={client_id}")

        posts_context = "Manual single-client test context."
        insights = "Manual single-client test insights."

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

        try:
            logger.info("Chamando AICouncilService.generate_strategy()")
            strategy_json = AICouncilService.generate_strategy(briefing_dict, insights, posts_context)
            logger.info("Strategy generated successfully")
        except Exception:
            logger.exception("Erro ao gerar estratégia via IA")
            return

        try:
            # Remove estratégia antiga e salva nova
            supabase.table('strategies').delete().eq('client_id', client_id).execute()
            supabase.table('strategies').insert({
                'client_id': client_id,
                'content_json': strategy_json,
                'status': 'completed',
                'model_used': 'single-test-v1'
            }).execute()
            logger.info("Estratégia salva no banco.")
        except Exception:
            logger.exception("Erro ao salvar estratégia no banco")

        try:
            client_info = supabase.table('clients').select('email').eq('id', client_id).execute()
            if client_info.data:
                to_email = client_info.data[0].get('email')
                logger.info(f"Enviando e-mail para: {to_email}")
                r = resend.Emails.send({
                    "from": "Leads AI <onboarding@resend.dev>",
                    "to": to_email,
                    "subject": "🎉 Teste Individual: Sua Estratégia está Pronta!",
                    "html": "<h1>Teste individual executado com sucesso.</h1><p>Se isto foi enviado, a integração com Resend funciona.</p>"
                })
                logger.info(f"Resposta Resend: {r}")
            else:
                logger.error("Cliente sem e-mail cadastrado.")
        except Exception:
            logger.exception("Erro ao enviar e-mail via Resend")


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--client_id', required=True)
    args = p.parse_args()

    try:
        process_client(args.client_id)
    except Exception:
        logger.error("Erro não tratado:")
        traceback.print_exc()


if __name__ == '__main__':
    main()
