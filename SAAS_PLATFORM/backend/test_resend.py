import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
from_addr = "Leads AI <onboarding@resend.dev>" # Usando dominio padrao do Resend para teste
to_addr = "drmgaviao@gmail.com"

try:
    print(f"Tentando enviar e-mail de teste para {to_addr} via Resend...")
    r = resend.Emails.send({
        "from": from_addr,
        "to": to_addr,
        "subject": "🚀 Teste de Conexão Leads AI",
        "html": "<strong>Se você recebeu isso, o Resend está funcionando!</strong>"
    })
    print(f"✅ Sucesso! ID do e-mail: {r}")
except Exception as e:
    print(f"❌ Erro ao enviar e-mail: {e}")
