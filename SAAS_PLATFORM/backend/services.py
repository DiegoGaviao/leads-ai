import os
import json
import logging
import re
from typing import List, Optional
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


def expected_roteiros_for_plan(plan: Optional[str]) -> int:
    """Roteiros pedidos ao conselho conforme o plano (free/starter 3, pro 5, master 10)."""
    p = (plan or "").strip().lower()
    if p == "master":
        return 10
    if p == "pro":
        return 5
    return 3


def align_post_themes(post_themes: Optional[list], n: int) -> List[str]:
    """Garante lista de N strings (vazias = cliente não pediu tema naquele índice)."""
    raw = post_themes if isinstance(post_themes, list) else []
    out: List[str] = []
    for i in range(n):
        if i < len(raw) and raw[i] is not None:
            out.append(str(raw[i]).strip())
        else:
            out.append("")
    return out


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
        Prioridade absoluta: DNA do questionário + posts do próprio cliente. Sugestões de mercado agregadas são só calibragem — nunca substituem a essência da marca.
        No campo "visual" de cada roteiro, descreva apenas cenas fotográficas ou metáforas visuais SEM papel, telas, gráficos ou textos legíveis no quadro.
        """

        try:
            n = int(briefing.get("expected_roteiros") or 5)
        except (TypeError, ValueError):
            n = 5
        n = max(1, min(n, 15))

        post_themes = briefing.get("post_themes") or []
        themes_lines = []
        if isinstance(post_themes, list):
            for idx, t in enumerate(post_themes[:n], start=1):
                ts = str(t).strip() if t is not None else ""
                if ts:
                    themes_lines.append(f"  - Roteiro índice {idx}: {ts}")
        themes_block = ""
        if themes_lines:
            themes_block = (
                "TEMAS CRIATIVOS OPCIONAIS (pedido do cliente — alinhe o roteiro do mesmo índice; "
                "se um índice não estiver listado, gere normalmente a partir do DNA e dos dados):\n"
                + "\n".join(themes_lines)
                + "\n\n"
            )

        if n <= 5:
            variety_hint = (
                "Varie os roteiros entre: quebra de padrão, autoridade, conexão/história, técnico/dica, venda indireta "
                "(use o mix que couber em "
                + str(n)
                + " itens)."
            )
        else:
            variety_hint = (
                "Mantenha alternância de formatos (história, autoridade, objeção, prova social, dica rápida, oferta suave, etc.) ao longo dos "
                + str(n)
                + " roteiros."
            )

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

        INSIGHTS E REFERÊNCIAS (resumo do cliente + sugestões de mercado anônimas):
        {insights}

        DADOS BRUTOS (POSTS DO CLIENTE — permalink e métricas; use como evidência principal):
        {raw_data[:8000]}

        {themes_block}---
        TAREFA:
        Gere um JSON estritamente válido com a seguinte estrutura:
        {{
            "persona": "Markdown rico detalhando a Persona. Use o Tom de Voz definido. Crie uma seção 'O Que Não Somos' para diferenciar.",
            "estrategia": "Markdown explicando o 'Angulo Único' dessa marca baseada nos dados. Defina 3 Pilares de Conteúdo.",
            "roteiros": [
                {{
                    "index": 1,
                    "tema": "Título chamativo (Hook)",
                    "visual": "Descrição da cena — somente elementos filmáveis; zero documentos, telas ou textos legíveis na imagem.",
                    "texto": "Roteiro completo FALADO (Use o tom de voz: {briefing.get('tone_voice')})",
                    "legenda": "Legenda para o post"
                }}
            ]
        }}

        Exija EXATAMENTE {n} objetos dentro de "roteiros", com "index" de 1 até {n}, sem duplicar índices.
        {variety_hint}
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
