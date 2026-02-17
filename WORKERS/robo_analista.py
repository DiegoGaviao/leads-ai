import io
import re
import time
import json
import os
import hashlib
import requests
import pandas as pd
from openai import OpenAI
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import schedule
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ==========================================
# CONFIGURAÇÃO DO CONSELHO DE IAs
# ==========================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - A.I. COUNCIL - %(message)s')
load_dotenv()

# Clientes de API
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# DeepSeek usa cliente OpenAI compatível
deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# HuggingFace
hf_client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENTS_DIR = os.path.join(BASE_DIR, "CLIENTES")
LINKS_FILE = os.path.join(CLIENTS_DIR, "banco_de_links.json")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json")

def get_file_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# --- FUNÇÕES GOOGLE SHEETS AUTH ---

def get_sheet_data_authenticated(spreadsheet_id):
    """Autentica e busca a aba correta (que tem dados de Email/Instagram)."""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        logging.error(f"❌ Arquivo de credenciais não encontrado: {SERVICE_ACCOUNT_FILE}")
        return []

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # 1. Listar todas as abas
        meta = sheet.get(spreadsheetId=spreadsheet_id).execute()
        sheets_metadata = meta.get('sheets', [])
        
        for sheet_meta in sheets_metadata:
            title = sheet_meta['properties']['title']
            logging.info(f"🔎 Verificando aba: '{title}'...")
            
            # Ler apenas o cabeçalho para validar
            header_result = sheet.values().get(spreadsheetId=spreadsheet_id, range=f"'{title}'!A1:Z1").execute()
            header_values = header_result.get('values', [])
            
            if not header_values:
                continue
                
            header_row = [str(h).lower() for h in header_values[0]]
            
            # Critério de seleção: Tem coluna de Email ou Instagram?
            if any("email" in h for h in header_row) or any("instagram" in h for h in header_row):
                logging.info(f"✅ Aba de dados encontrada: '{title}'")
                
                # Baixar dados completos dessa aba
                full_result = sheet.values().get(spreadsheetId=spreadsheet_id, range=f"'{title}'").execute()
                return full_result.get('values', [])
        
        logging.error("❌ Nenhuma aba válida encontrada (com colunas Email/Instagram).")
        return []
        
    except Exception as e:
        logging.error(f"❌ Erro de Leitura Google Sheets: {e}")
        return []

# --- FUNÇÕES DOS AGENTES ---

def call_deepseek_analyst(csv_data):
    """DeepSeek: Focado em Lógica, Matemática e Padrões."""
    logging.info("🤖 [1/3] Chamando DeepSeek (O Cientista)...")
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Você é um Cientista de Dados Sênior focado em algoritmos de rede social."},
                {"role": "user", "content": f"Analise estes dados CSV brutos e me dê SOMENTE os fatos numéricos: Que tipo de post tem maior retenção média? Existe correlação entre tamanho da legenda e likes? Quais os 3 posts outliers positivos?\n\nDADOS:\n{csv_data[:10000]}"}
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Erro DeepSeek: {e}")
        return "DeepSeek indisponível."

def call_huggingface_critic(current_persona):
    """HuggingFace (Mistral/Llama): O Crítico Técnico."""
    logging.info("⚖️ [2/3] Chamando HuggingFace (O Crítico)...")
    try:
        # Usando Mixtral-8x7B para crítica
        prompt = f"<s>[INST] Analise esta descrição de Persona de IA e aponte 3 pontos cegos ou clichês que devem ser evitados. Seja curto e grosso.\n\nPERSONA:\n{current_persona[:2000]} [/INST]"
        response = hf_client.text_generation(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            prompt=prompt,
            max_new_tokens=500
        )
        # Handle different response types (sometimes returns list of dicts)
        if isinstance(response, list) and 'generated_text' in response[0]:
            return response[0]['generated_text']
        return str(response)
    except Exception as e:
        logging.error(f"Erro HuggingFace: {e}")
        return "HuggingFace indisponível."

def generate_structure_deepseek(csv_data, deepseek_insight, briefing_data=None):
    """DeepSeek gera estrutura completa em JSON para separar arquivos."""
    logging.info("🏗️ [3/3] DeepSeek Construindo Arquivos (JSON)...")
    
    contexto_humano = ""
    if briefing_data:
        contexto_humano = f"""
    ---
    CONTEXTO HUMANO (O QUE O CLIENTE DISSE - LEI SUPREMA):
    Missão: {briefing_data.get('missao')}
    Inimigo/O que NÃO é: {briefing_data.get('inimigo')}
    Dor do Cliente: {briefing_data.get('dor_cliente')}
    Nome do Método Sugerido: {briefing_data.get('metodo_nome')}
    Palavras-Chave: {briefing_data.get('palavras_chave')}
    ---
    """
    
    prompt = f"""
    Você é o Gerente de Conteúdo Sênior da Agência. Sua missão é criar uma Identidade de Marca PROFUNDA e ÚNICA para este cliente.
    
    {contexto_humano}

    BASE DE DADOS (O que funciona na prática):
    {deepseek_insight}
    
    AMOSTRA DE DADOS REAIS: {csv_data[:3000]}

    ---
    ESTRUTURA OBRIGATÓRIA DO ARTEFATO FINAL (JSON):
    Gere um JSON com as chaves abaixo. O conteúdo deve ser Markdown rico.

    1. "persona": 
       Deve conter:
       - Quem é o especialista (Use a Missão do Briefing se houver).
       - Tabela "Tom de Voz": Colunas [❌ O que ele NÃO é] vs [✅ O que ele É] (Use o Inimigo do Briefing).
       - Arquétipo da Marca.
       - A Dor do Cliente.

    2. "estrategia":
       Deve conter:
       - O MÉTODO ÚNICO: Crie ou use o nome sugerido no briefing ({briefing_data.get('metodo_nome') if briefing_data else 'Sugerir Acrônimo'}).
       - Regras de Ouro (Do's & Don'ts).
       - Pilares Editoriais.

    3. "roteiros": 
       Lista de 5 objetos {{ "nome_arquivo": "...", "conteudo": "..." }}.
       Cada roteiro deve ser Roteirizado (Visual + Fala) e ter um gancho forte.

    ---
    RESPOSTA (APENAS JSON VÁLIDO):
    """
    
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Erro DeepSeek JSON: {e}")
        return "{}"

def process_master_sheet(xlsx_url):
    logging.info(f"📥 Conectando à Planilha Google (ID via URL)...")
    
    # Extrair ID da URL
    # Padrão: /d/([a-zA-Z0-9-_]+)
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", xlsx_url)
    if not match:
        logging.error("❌ Não foi possível extrair o ID da planilha da URL fornecida.")
        return
        
    spreadsheet_id = match.group(1)
    
    # Busca autenticada
    values = get_sheet_data_authenticated(spreadsheet_id)
    
    if not values:
        logging.error("❌ Nenhum dado retornado da planilha (Verifique permissões do bot).")
        return

    try:
        # Converter para DataFrame
        # Assumindo linha 1 como cabeçalho
        header = values[0]
        rows = values[1:]
        
        # Ajuste se houver linhas vazias ou tamanhos diferentes
        padded_rows = []
        for r in rows:
            if len(r) < len(header):
                r += [''] * (len(header) - len(r))
            padded_rows.append(r[:len(header)])
            
        df = pd.DataFrame(padded_rows, columns=header)
        logging.info(f"📂 Dados carregados: {len(df)} linhas")
        
        # Iterate over rows
        for index, row in df.iterrows():
            if len(row) < 7: continue
            
            raw_email = str(row[1]).strip()
            raw_insta = str(row[2]).strip()
            try:
                raw_json = str(row[6]).strip()
            except:
                raw_json = ""
            
            if "@" not in raw_email or "{" not in raw_json:
                continue
                
            client_name = raw_insta.replace("@", "").replace(" ", "").lower()
            if not client_name or client_name == "nan": continue
            
            logging.info(f"🔍 Auditoria IA em: {client_name}")
            
            client_folder = os.path.join(CLIENTS_DIR, client_name)
            ensure_dir(client_folder)
            
            try:
                # Parse JSON
                form_data = json.loads(raw_json)
                
                briefing_data = {
                    "missao": form_data.get("missao", ""),
                    "inimigo": form_data.get("inimigo", ""),
                    "dor_cliente": form_data.get("dor_cliente", ""),
                    "metodo_nome": form_data.get("metodo_nome", ""),
                    "palavras_chave": form_data.get("palavras_chave", ""),
                    "email": raw_email,
                    "plano": form_data.get("plano", "basico")
                }
                
                # Check Hash
                json_dump = json.dumps(briefing_data, sort_keys=True)
                hash_file = os.path.join(client_folder, ".last_hash")
                current_hash = get_file_hash(json_dump)
                
                last_hash = ""
                if os.path.exists(hash_file):
                    with open(hash_file, 'r') as f: last_hash = f.read().strip()
                
                if current_hash == last_hash and not os.environ.get("FORCE_UPDATE"):
                    logging.info(f"💤 {client_name}: Nada novo.")
                    continue
                
                with open(os.path.join(client_folder, "BRIEFING.json"), 'w') as f:
                    json.dump(briefing_data, f, indent=4, ensure_ascii=False)
                    
                logging.info(f"⚡ {client_name}: GERAÇÃO DE PACOTE INICIADA...")

                # ... (restante do código igual) ...
                csv_data = "Tema,Views,Likes,Saves,Comments\n"
                
                has_stats = False
                for i in range(1, 11):
                    p_view = form_data.get(f"post{i}_views")
                    if p_view:
                        p_tema = form_data.get(f"post{i}_tema", f"Post {i}")
                        p_likes = form_data.get(f"post{i}_likes", 0)
                        p_saves = form_data.get(f"post{i}_saves", 0)
                        p_comm = form_data.get(f"post{i}_comments", 0)
                        csv_data += f"{p_tema},{p_view},{p_likes},{p_saves},{p_comm}\n"
                        has_stats = True
                
                if not has_stats:
                    csv_data += "Sem Dados,0,0,0,0\n"

                insight_numerico = "Sem dados numéricos robustos. Focando na Análise Semântica (Briefing)."
                if has_stats:
                    insight_numerico = call_deepseek_analyst(csv_data)
                
                json_str = generate_structure_deepseek(csv_data, insight_numerico, briefing_data)
                
                json_str = json_str.replace("```json", "").replace("```", "")
                match = re.search(r'(\{.*\})', json_str, re.DOTALL)
                if match: json_clean = match.group(1)
                else: json_clean = json_str
                
                data = json.loads(json_clean)
                
                with open(os.path.join(client_folder, "PERSONA_V2.md"), 'w') as f:
                    f.write(data.get("persona", ""))
                
                with open(os.path.join(client_folder, "ESTRATEGIA_CONTEUDO.md"), 'w') as f:
                    f.write(data.get("estrategia", ""))
                
                roteiros_dir = os.path.join(client_folder, "ROTEIROS_PRONTOS")
                ensure_dir(roteiros_dir)
                
                for roteiro in data.get("roteiros", []):
                    safe_name = str(roteiro["nome_arquivo"]).replace("/", "_").replace(" ", "_")
                    with open(os.path.join(roteiros_dir, safe_name), 'w') as f:
                        f.write(roteiro["conteudo"])
                
                with open(hash_file, 'w') as f: f.write(current_hash)
                logging.info(f"✅ {client_name}: PACOTE COMPLETO GERADO!")

            except json.JSONDecodeError:
                logging.warning(f"⚠️ Erro ao decodar JSON para {client_name}")
            except Exception as e:
                logging.error(f"❌ Erro Processamento ({client_name}): {e}")

    except Exception as e:
        logging.error(f"❌ Erro Geral Acesso Planilha: {e}")

def job():
    if not os.path.exists(LINKS_FILE): return
    with open(LINKS_FILE, 'r') as f: links = json.load(f)
    if "PLANILHA_MESTRA" in links: process_master_sheet(links["PLANILHA_MESTRA"])

schedule.every(30).minutes.do(job)

if __name__ == "__main__":
    print("🤖 CONSELHO DE IAs INICIADO (DeepSeek + OpenAI + HuggingFace)")
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)
