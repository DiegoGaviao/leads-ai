
import os
import time
import json
import logging
from dotenv import load_dotenv

# Database & Services
from database import get_supabase_client
from services import AICouncilService
import resend

# Load Env
load_dotenv()

# Config Resend
resend.api_key = os.getenv("RESEND_API_KEY") or "re_your_api_key_placeholder"

print("🚀 INICIANDO WORKER LEADS AI...") 

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

def fetch_pending_briefings():
    """Busca briefings (clientes) que ainda NÃO têm estratégia gerada."""
    try:
        # Pega todos os briefings
        # (Em produção, faríamos um JOIN para filtrar, mas Supabase JS client é limitado em joins complexos 'not in')
        # Workaround: Pegar IDs de estratégias existentes e excluir.
        
        # 1. Pega IDs de clientes já processados
        existing_strategies = supabase.table('strategies').select('client_id').execute()
        processed_ids = [row['client_id'] for row in existing_strategies.data] if existing_strategies.data else []

        # 2. Pega briefings de clientes NÃO processados
        query = supabase.table('briefings').select('*')
        
        if processed_ids:
            # Filtra clientes que NÃO estão na lista de processados
            # Nota: Supabase postgrest-js filter 'not.in' usa parenteses -> .not('client_id', 'in', (1,2,3))
            query = query.not_.in_('client_id', processed_ids)
            
        result = query.execute()
        return result.data or []

    except Exception as e:
        logger.error(f"Erro ao buscar briefings pendentes: {e}")
        return []

def process_briefing(briefing):
    client_id = briefing['client_id']
    logger.info(f"🚀 Iniciando processamento para Cliente ID: {client_id}")

    try:
        # 1. Buscar Contexto (Posts Antigos) se houver
        posts_data = supabase.table('analyzed_posts').select('*').eq('client_id', client_id).execute()
        raw_posts = posts_data.data or []
        
        # Formata posts para string simples (Contexto para IA)
        posts_context = "\n".join([
            f"- {p.get('post_link', 'Sem Link')} | Views: {p.get('views',0)} | Likes: {p.get('likes',0)}"
            for p in raw_posts
        ]) if raw_posts else "Cliente novo, sem histórico de posts importado."

        # 2. Gera Insights Rápidos (Mock por enquanto, ou chamar DeepSeek Analyze)
        insights = "Análise preliminar indica foco em crescimento de audiência."

        # 3. Gera a Estratégia Completa (Persona, Pilares, Roteiros)
        # Mapeia campos do banco (snake_case) para o esperado pelo Service (chaves do dict)
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

        logger.info(f"🧠 Enviando para IA... (Modelos: DeepSeek / GPT-4o Mini)")
        strategy_json = AICouncilService.generate_strategy(briefing_dict, insights, posts_context)

        # 4. Salva o Resultado
        logger.info(f"💾 Salvando Estratégia Gerada...")
        save_result = supabase.table('strategies').insert({
            'client_id': client_id,
            'content_json': strategy_json,
            'status': 'completed',
            'model_used': 'hybrid-v2'
        }).execute()

        logger.info(f"✅ Sucesso! Estratégia salva para {client_id}")

        # 5. Enviar E-mail para o cliente
        try:
            # Buscar e-mail do cliente na tabela 'clients'
            client_info = supabase.table('clients').select('email').eq('id', client_id).execute()
            if client_info.data:
                to_email = client_info.data[0]['email']
                logger.info(f"📧 Enviando e-mail para: {to_email}")
                
                resend.emails.send({
                    "from": "Leads AI <onboarding@resend.dev>",
                    "to": to_email,
                    "subject": "🎉 Sua Estratégia Leads AI está Pronta!",
                    "html": f"""
                        <h1>Parabéns! O Conselho de IAs terminou seu trabalho.</h1>
                        <p>Sua estratégia de conteúdo personalizada baseada no DNA da sua marca e dados do Instagram já está disponível.</p>
                        <p><strong>Acesse agora o seu Dashboard para ver:</strong></p>
                        <ul>
                            <li>Sua Nova Persona</li>
                            <li>3 Pilares de Conteúdo Únicos</li>
                            <li>5 Roteiros de Reels Prontos para Gravar</li>
                        </ul>
                        <br>
                        <a href="https://leads-ai-frontend.onrender.com/dashboard" style="background:#007bff; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">Ver Minha Estratégia</a>
                    """
                })
                logger.info("✅ E-mail enviado com sucesso!")
        except Exception as mail_err:
            logger.error(f"⚠️ Falha ao enviar e-mail: {mail_err}")

    except Exception as e:
        logger.error(f"❌ Falha ao processar cliente {client_id}: {e}")
        # Opcional: Marcar flag de erro no banco para não tentar infinitamente

def run_worker():
    logger.info("🤖 Leads AI Worker Iniciado. Aguardando jobs...")
    while True:
        try:
            pending = fetch_pending_briefings()
            
            if pending:
                logger.info(f"Encontrados {len(pending)} briefings pendentes.")
                for briefing in pending:
                    process_briefing(briefing)
            else:
                pass 
                # logger.debug("Nenhum job pendente.")

            # Espera 10 segundos antes da próxima verificação
            time.sleep(10)

        except KeyboardInterrupt:
            logger.info("🛑 Worker interrompido pelo usuário.")
            break
        except Exception as e:
            logger.error(f"⚠️ Erro no loop principal: {e}")
            time.sleep(30) # Espera mais se der erro grave

if __name__ == "__main__":
    run_worker()
