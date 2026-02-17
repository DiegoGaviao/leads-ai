import os
import logging
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ ERRO CRÍTICO: Variáveis SUPABASE_URL ou SUPABASE_KEY não encontradas no .env")

logging.info(f"🔗 Conectando ao Supabase em: {SUPABASE_URL}")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logging.error(f"❌ Falha ao inicializar cliente Supabase: {e}")
    raise e

def get_supabase_client() -> Client:
    return supabase
