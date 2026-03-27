
import os
import json
import logging
from typing import List, Dict
from openai import OpenAI
import requests

# Configuração do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentArtisan")

class ArtisanAgent:
    """
    Agente 06: Artisan
    Responsável por transformar roteiros e estratégias em ativos visuais de alto impacto.
    """
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_visual_prompts(self, script_text: str, brand_tone: str, audience_dna: str) -> List[str]:
        """
        Recebe um roteiro e gera 3 opções de prompts visuais otimizados para IAs de imagem.
        Foca em: Composição, Iluminação, Estilo de Marca e Psicologia das Cores.
        """
        logger.info(f"🎨 Engenharia de Prompt Visual iniciada para: {brand_tone}")
        
        system_prompt = f"""
        Você é o 'Artisan', o Diretor de Arte do Conselho Leads AI.
        Sua missão é criar prompts de imagem de ultra-realismo ou estilo premium para redes sociais.
        
        CONTEXTO DA MARCA:
        - Tom: {brand_tone}
        - Público: {audience_dna}
        
        REGRAS DE OURO:
        1. Estética: Estilo 'Editorial Photography', 'Cinematic Lighting' ou 'High-end Tech Branding'.
        2. Evite o 'olhar de IA' genérico. Busque texturas reais, profundidade de campo (bokeh) e enquadramentos modernos.
        3. Se o roteiro for técnico, use elementos de design clean e futurista.
        4. Se for lifestyle, use iluminação natural e expressões orgânicas.
        
        FORMATO DE SAÍDA (obrigatório, uma linha raiz):
        Retorne SOMENTE um objeto JSON válido neste formato exato:
        {"prompts": ["prompt 1 em inglês", "prompt 2 em inglês", "prompt 3 em inglês"]}
        Cada prompt deve ser detalhado para geração de imagem (composição, luz, textura, estilo).
        """
        
        user_msg = f"Roteiro Sugerido: {script_text}\n\nGere 3 conceitos visuais magnéticos para este post."
        
        def _call(model_name: str):
            return self.openai_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg},
                ],
                response_format={"type": "json_object"},
            )

        try:
            response = _call("gpt-4o")
            raw = response.choices[0].message.content
            result = json.loads(raw)
            if isinstance(result, list):
                return [str(x) for x in result[:3]]
            prompts = result.get("prompts")
            if isinstance(prompts, list):
                return [str(x) for x in prompts[:3] if x]
            return []
        except Exception as e:
            logger.warning("gpt-4o prompts visual falhou (%s); tentando gpt-4o-mini...", e)
            try:
                response = _call("gpt-4o-mini")
                raw = response.choices[0].message.content
                result = json.loads(raw)
                if isinstance(result, list):
                    return [str(x) for x in result[:3]]
                prompts = result.get("prompts")
                if isinstance(prompts, list):
                    return [str(x) for x in prompts[:3] if x]
                return []
            except Exception as e2:
                logger.error("❌ Erro ao gerar prompts visuais: %s", e2)
                return []

    def create_image(self, prompt: str) -> str:
        """
        Chama a API de geração de imagem (DALL-E 3 por padrão).
        Retorna a URL da imagem gerada.
        """
        logger.info(f"📸 Gerando imagem real para o prompt: {prompt[:50]}...")
        
        try:
            if self.provider == "openai":
                q = (os.getenv("LEADS_AI_IMAGE_QUALITY") or "standard").strip().lower()
                if q not in ("standard", "hd"):
                    q = "standard"
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality=q,
                    n=1,
                )
                return response.data[0].url
            
            # Placeholder para Flux/Replicate no futuro
            return "Provider not implemented yet"
            
        except Exception as e:
            logger.error(f"❌ Falha na geração da imagem: {e}")
            return ""

# Exemplo de Teste Isolado
if __name__ == "__main__":
    # Simulação de dados vindos do Report
    artisan = ArtisanAgent()
    
    test_script = "Como faturar seus primeiros 10k com SaaS sem saber programar."
    test_tone = "Autoridade, Minimalista, Dark Mode"
    test_dna = "Empreendedores iniciantes, 25-35 anos"
    
    prompts = artisan.generate_visual_prompts(test_script, test_tone, test_dna)
    print("\n🚀 PROMPTS GERADOS PELO ARTISAN:")
    for i, p in enumerate(prompts):
        print(f"{i+1}. {p}\n")
    
    # Comentado para não gastar crédito sem necessidade no backup
    # img_url = artisan.create_image(prompts[0])
    # print(f"🖼 URL DA IMAGEM: {img_url}")
