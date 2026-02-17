import os
import json
import logging
import re
from openai import OpenAI
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# Configuração de Clientes
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# DeepSeek usa cliente OpenAI compatível
deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# HuggingFace
hf_client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))

class AICouncilService:
    @staticmethod
    def analyze_data(csv_data: str):
        """DeepSeek: Focado em Lógica e Padrões Numéricos."""
        try:
            response = deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Você é um Cientista de Dados Sênior focado em algoritmos de rede social."},
                    {"role": "user", "content": f"Analise estes dados CSV brutos e me dê SOMENTE os fatos numéricos: Que tipo de post tem maior retenção média? Existe correlação entre tamanho da legenda e likes? Quais os 3 posts outliers positivos?\n\nDADOS:\n{csv_data[:10000]}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Erro DeepSeek Analyst: {e}")
            return "Indisponível no momento."

    @staticmethod
    def generate_strategy(briefing: dict, insights: str, raw_data: str):
        """Gera a estrutura final JSON contendo Persona, Estratégia e Roteiros."""
        prompt = f"""
        Você é o Gerente de Conteúdo Sênior da Agência Leads AI. 
        Sua missão é criar uma Identidade de Marca PROFUNDA e ÚNICA.

        CONTEXTO DO CLIENTE:
        Missão: {briefing.get('missao')}
        Inimigo: {briefing.get('inimigo')}
        Dor do Cliente: {briefing.get('dor_cliente')}
        Método: {briefing.get('metodo_nome')}

        INSIGHTS DOS DADOS REAIS:
        {insights}

        DADOS BRUTOS (AMOSTRA):
        {raw_data[:2000]}

        ---
        ESTRUTURA OBRIGATÓRIA (JSON):
        1. "persona": Markdown rico descrevendo o Especialista, Tom de Voz (É vs Não É) e Dores.
        2. "estrategia": Markdown descrevendo o Método Único, Regras de Ouro e Pilares.
        3. "roteiros": Lista de 5 objetos {{ "index": 1, "tema": "...", "visual": "...", "texto": "..." }}.

        RESPOSTA APENAS JSON VÁLIDO.
        """
        try:
            response = deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logging.error(f"Erro DeepSeek Strategy: {e}")
            raise e
