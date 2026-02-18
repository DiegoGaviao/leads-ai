
import os
import resend
from dotenv import load_dotenv
from email_templates import get_professional_strategy_email

# Load Env
load_dotenv()

# Config Resend
resend.api_key = os.getenv("RESEND_API_KEY")
from_addr = os.getenv("EMAIL_FROM", "Leads AI <onboarding@resend.dev>")

def send_real_test_email(to_email):
    print(f"📧 Preparando envio para: {to_email}")
    
    # Mock de dados reais para o e-mail
    persona = (
        "Empreendedor Digital focado em SaaS e Automação.\n"
        "Busca escala através de processos otimizados e IA.\n"
        "Valoriza ferramentas que economizam tempo e aumentam a conversão."
    )
    
    estrategia = (
        "1. Posicionamento como autoridade em IA aplicada a vendas.\n"
        "2. Funil de conteúdo focado em 'Pains' de produtividade.\n"
        "3. CTA agressivo para demonstração da plataforma Leads AI."
    )
    
    roteiros = [
        {
            "tema": "Vídeo 1: O Fim das Tarefas Manuais",
            "visual": "Cena de um empreendedor frustrado na frente do computador tentando organizar planilhas e responder DMs.",
            "texto": (
                "Sério, você ainda está fazendo isso? 🤯 \n\n"
                "Em 2026, perder 4 horas por dia com CRM e resposta manual de leads não é 'trabalho duro', é falta de ferramenta. \n\n"
                "Eu já estive nesse lugar, achando que o caos era parte do crescimento. Não é. \n\n"
                "A Leads AI foi criada para quem quer escalar sem precisar de um exército de suporte. \n\n"
                "Toque no link da bio e saia da era das planilhas."
            ),
            "legenda": "O tempo é o único recurso que você não consegue recuperar. Use IA a seu favor. 🤖✨ #leadsai #automacao #produtividade"
        },
        {
            "tema": "Vídeo 2: A Verdade sobre Escala Digital",
            "visual": "Apareço com um celular na mão, mostrando o dashboard da Leads AI rodando e os leads caindo em tempo real.",
            "texto": (
                "Quer saber por que alguns SaaS escalam e outros morrem no primeiro ano? \n\n"
                "A diferença não é o produto, é a retenção do lead no momento em que ele está 'quente'. \n\n"
                "Se você demora 10 minutos para responder, você já perdeu a venda. \n\n"
                "Com o meu conselho de IAs, o lead entra, é qualificado e direcionado em segundos. \n\n"
                "Isso é escala real. Isso é Leads AI."
            ),
            "legenda": "Não deixe o dinheiro escorrer pelas mãos por falta de agilidade. 💰📈 #saas #vendas #growth"
        }
    ]
    
    html_body = get_professional_strategy_email(persona, estrategia, roteiros)
    
    print("🚀 Enviando via Resend...")
    try:
        r = resend.Emails.send({
            "from": from_addr,
            "to": to_email,
            "subject": "✨ Sua Estratégia Leads AI está Pronta (Exemplo Real)",
            "html": html_body
        })
        print(f"✅ Sucesso! Resposta: {r}")
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")

if __name__ == "__main__":
    send_real_test_email("drmgaviao@gmail.com")
