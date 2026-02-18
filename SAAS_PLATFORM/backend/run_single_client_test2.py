import os
import sys
import json
import logging
import argparse
import traceback
from datetime import datetime
from dotenv import load_dotenv

from database import get_supabase_client
from services import AICouncilService
import resend

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
from_addr = os.getenv("EMAIL_FROM", "Leads AI <onboarding@resend.dev>")
import html as _html

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def process_client(client_id: str):
    supabase = get_supabase_client()

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
            # montar corpo com a estratégia gerada (formatado)
            persona = strategy_json.get('persona','') or ''
            estrategia = strategy_json.get('estrategia','') or ''
            roteiros = strategy_json.get('roteiros', []) or []

            # formatar Persona e Estratégia como blocos (similar aos roteiros)
            persona_html = f"<div style='margin-bottom:12px'><div style='white-space:pre-wrap;font-family:Arial,Helvetica,sans-serif'>{_html.escape(persona)}</div></div>"
            estrategia_html = f"<div style='margin-bottom:12px'><div style='white-space:pre-wrap;font-family:Arial,Helvetica,sans-serif'>{_html.escape(estrategia)}</div></div>"
            roteiros_html = ''
            for r_item in roteiros:
                tema = _html.escape(r_item.get('tema',''))
                texto = _html.escape(r_item.get('texto',''))
                legenda = _html.escape(r_item.get('legenda',''))
                roteiros_html += f"<div style='margin-bottom:12px'><h3 style='margin:0 0 6px 0'>{tema}</h3><div style='white-space:pre-wrap'>{texto}</div><div style='color:#555'><em>{legenda}</em></div></div>"

            # get strategy id for link
            strategy_id = None
            try:
                sel = supabase.table('strategies').select('id').eq('client_id', client_id).order('created_at', desc=True).limit(1).execute()
                if sel.data:
                    strategy_id = sel.data[0].get('id')
            except Exception:
                strategy_id = None

            # Use index.html fallback to avoid 404 on hosts without SPA rewrite rules (Render)
            strategy_link = f"https://leads-ai-frontend.onrender.com/index.html?strategy_id={strategy_id}" if strategy_id else "https://leads-ai-frontend.onrender.com/index.html"

            # Refined HTML email with inline SVG header and cleaner layout
            html_body = f"""
<div style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; background:#f6f9fc; padding:26px 12px; color:#0f172a;">
    <div style="max-width:720px; margin:0 auto;">
        <div style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 18px 40px rgba(15,23,42,0.06);">
            <div style="padding:18px 24px; display:flex; align-items:center; gap:12px; border-bottom:1px solid #eef3fa; background:linear-gradient(90deg,#f8fbff,#ffffff);">
                <div style="display:flex;align-items:center;gap:12px">
                    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                        <rect width="48" height="48" rx="10" fill="#0b5ed7"/>
                        <text x="24" y="30" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#fff" font-weight="700">LI</text>
                    </svg>
                    <div>
                        <div style="font-size:16px; color:#0b5ed7; font-weight:800;">Leads AI</div>
                        <div style="font-size:12px; color:#6b7280;">Estratégia personalizada — resumo</div>
                    </div>
                </div>
            </div>

            <div style="padding:22px 24px;">
                <h1 style="font-size:22px; margin:0 0 8px 0; font-weight:800; color:#0f172a;">Sua Estratégia Leads AI</h1>
                <p style="margin:0 0 14px 0; color:#4b5563; font-size:15px; line-height:1.5">Geramos um plano estruturado para você — abaixo está o resumo curto e acionável. Copie e cole onde precisar.</p>

                <div style="display:block;">
                    <div style="margin-bottom:12px;">
                        <div style="font-size:13px; color:#0b5ed7; font-weight:700; margin-bottom:6px">Persona</div>
                        <div style="background:#f9fbff;border:1px solid #eef6ff;padding:12px;border-radius:8px;color:#111827;font-size:14px;white-space:pre-wrap;">{persona_html}</div>
                    </div>

                    <div style="margin-bottom:12px;">
                        <div style="font-size:13px; color:#0b5ed7; font-weight:700; margin-bottom:6px">Estratégia</div>
                        <div style="background:#fff; border:1px solid #eef3fa; padding:14px; border-radius:8px; color:#111827; font-size:14px; white-space:pre-wrap;">{estrategia_html}</div>
                    </div>

                    <div style="margin-bottom:6px;">
                        <div style="font-size:13px; color:#0b5ed7; font-weight:700; margin-bottom:6px">Roteiros</div>
                        <div style="background:#fff; border:1px solid #eef3fa; padding:12px; border-radius:8px; color:#111827; font-size:14px;">{roteiros_html}</div>
                    </div>
                </div>

                <!-- link removido: hosts sem rewrite causavam 404 -->
            </div>

            <div style="padding:14px 24px; background:#fbfdff; border-top:1px solid #eef6ff; font-size:13px; color:#6b7280;">
                <div>Se quiser, responda este e‑mail com feedback e ajustamos o plano pra você.</div>
            </div>
        </div>
    </div>
</div>
"""

            # salvar preview HTML em LOGS para revisão
            logs_dir = os.path.join(os.path.dirname(__file__), '..', 'LOGS')
            logs_dir = os.path.abspath(logs_dir)
            os.makedirs(logs_dir, exist_ok=True)
            preview_path = os.path.join(logs_dir, f"email_preview_{strategy_id or 'noid'}.html")
            try:
                with open(preview_path, 'w', encoding='utf-8') as pf:
                    pf.write(html_body)
                logger.info(f"Preview salvo: {preview_path}")
            except Exception:
                logger.exception("Erro ao salvar preview HTML")

            r = resend.Emails.send({
                "from": from_addr,
                "to": to_email,
                "subject": "🎉 Teste Individual: Sua Estratégia está Pronta!",
                "html": html_body
            })
            logger.info(f"Resposta Resend: {r}")

            # registrar resposta em log local
            try:
                log_path = os.path.join(logs_dir, "email_sends.log")
                with open(log_path, 'a', encoding='utf-8') as lf:
                    lf.write(json.dumps({
                        "timestamp": datetime.utcnow().isoformat(),
                        "strategy_id": strategy_id,
                        "to": to_email,
                        "response": r
                    }, default=str) + "\n")
                logger.info(f"Resposta registrada em: {log_path}")
            except Exception:
                logger.exception("Erro ao gravar email_sends.log")
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
