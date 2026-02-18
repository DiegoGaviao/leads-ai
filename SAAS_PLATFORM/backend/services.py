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
        """Gera a estrutura final JSON contendo Persona, Estratégia e Roteiros usando o NOVO BRIEFING RICO."""
        
        system_prompt = """
        Você é o Diretor Criativo da Leads AI. Sua missão é criar uma Identidade de Marca PROFUNDA, ÚNICA e MATEMATICAMENTE validada.
        Não use clichês de marketing. Use psicologia comportamental e dados.
        """

        user_prompt = f"""
        CONTEXTO DO CLIENTE (DNA DA MARCA):
        1. MISSÃO: {briefing.get('mission')}
        2. TOM DE VOZ: {briefing.get('tone_voice')} (Isso dita como você escreve tudo).
        3. AUTORIDADE: {briefing.get('authority')} (Use isso para gerar credibilidade).
        4. GRANDE PROMESSA (O CÉU): {briefing.get('big_promise')}
        5. O INIMIGO COMUM: {briefing.get('enemy')}
        6. A DOR PROFUNDA (O INFERNO): {briefing.get('pain_point')}
        7. O SONHO DO CLIENTE: {briefing.get('desire_point')}
        8. PRODUTO/MÉTODO: {briefing.get('method_name')}
        9. CLIENTE IDEAL: {briefing.get('dream_client')}

        INSIGHTS DOS DADOS REAIS (O QUE JÁ FUNCIONA):
        {insights}

        DADOS BRUTOS (AMOSTRA DE POSTS ANTERIORES):
        {raw_data[:2000]}

        ---
        TAREFA:
        Gere um JSON estritamente válido com a seguinte estrutura:
        {{
            "persona": "Markdown rico detalhando a Persona. Use o Tom de Voz definido. Crie uma seção 'O Que Não Somos' para diferenciar.",
            "estrategia": "Markdown explicando o 'Angulo Único' dessa marca baseada nos dados. Defina 3 Pilares de Conteúdo.",
            "roteiros": [
                {{
                    "index": 1,
                    "tema": "Título chamativo (Hook)",
                    "visual": "Descrição da cena ou imagem",
                    "texto": "Roteiro completo FALADO (Use o tom de voz: {briefing.get('tone_voice')})",
                    "legenda": "Legenda para o post"
                }},
                ... (Gere 5 roteiros variados: 1 de Quebra de Padrão, 1 de Autoridade, 1 de Conexão/História, 1 Técnico/Dica, 1 Venda Indireta)
            ]
        }}
        """

        try:
            # Tenta primeiro com DeepSeek (Mais Inteligente para Raciocínio)
            response = deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logging.warning(f"DeepSeek falhou, tentando OpenAI GPT-4o-mini... Erro: {e}")
            # Fallback para OpenAI (Mais Estável)
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e2:
                logging.error(f"Erro Crítico na Geração de Estratégia: {e2}")
                raise e2
