import os
import json
import resend
from database import get_supabase_client
from email_templates import get_professional_strategy_email
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
from_addr = "Leads AI <onboarding@resend.dev>"
to_addr = "drmgaviao@gmail.com"
brand_id = "4f5d74a5-8e86-433e-826c-a573c921ef5f"

try:
    supabase = get_supabase_client()
    res = supabase.table('leads_ai_strategies').select('*').eq('brand_id', brand_id).execute()
    
    if res.data:
        strat = res.data[0]
        print(f"Enviando estratégia existente para {to_addr}...")
        
        # O campo scripts_json pode vir como string ou lista
        scripts = strat.get('scripts_json', [])
        if isinstance(scripts, str):
            scripts = json.loads(scripts)
            
        html_body = get_professional_strategy_email(
            strat.get('persona_markdown', ''),
            strat.get('strategy_markdown', ''),
            scripts
        )
        
        resend.Emails.send({
            "from": from_addr,
            "to": to_addr,
            "subject": "🎉 [REENVIO] Sua Estratégia Leads AI está Pronta!",
            "html": html_body
        })
        print("✅ Enviado com sucesso!")
    else:
        print("❌ Estratégia não encontrada no banco.")
except Exception as e:
    print(f"❌ Erro: {e}")
