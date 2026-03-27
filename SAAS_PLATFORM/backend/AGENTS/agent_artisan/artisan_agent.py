
import os
import json
import logging
from typing import List, Dict
from openai import OpenAI
import requests

# Configuração do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentArtisan")

# Síntese de DOCS/Sora prompts.md + MARKETING_ASSETS/DHAWK_BRAND_STANDARD.md (padrão Dhawk / relatório)
_SORA_STRUCTURE_RULES = """
Estruture CADA prompt de imagem em INGLÊS seguindo este método (Sora-style / relatório Leads AI):
1) Cena principal em 3–5 frases objetivas: lugar, momento, sujeitos ou objetos, ação, enquadramento.
2) Listas com hífen quando útil (variações de styling, luz, materiais).
3) Restrições negativas explícitas: no readable text, no logos, no watermarks, no subtitles, avoid symmetrical cliché framing unless intentional, avoid plastic CGI skin / wax faces.
4) Bloco técnico curto: cinematic lighting, shallow depth of field, ultra-detailed, professional color grading, believable optics (as if shot on full-frame), vertical-friendly composition for Instagram square crop.
5) Quando fizer sentido com o roteiro, incorpore sutilmente a estética Dhawk: sophisticated dark or neutral base, subtle electric emerald green (#00FF41 family) as accent light or UI glow — luxury tech, minimalist, glass-friendly reflections — SEM dominar a cena se o roteiro for lifestyle orgânico ou clínico acolhedor.
6) PROIBIDO na cena: qualquer papel, documento, planilha, gráfico, tela de computedor/celular com texto, placas com letras, livros abertos com páginas legíveis, mockups de UI, números ou palavras renderizadas (modelos de imagem inventam lixo). Se precisar de “dados”, sugira luz abstrata, textura, gesto humano ou objeto sem rótulo — NEVER typography in-frame.
"""

_DALLE_CHAR_LIMIT = 3900


class ArtisanAgent:
    """
    Agente 06: Artisan
    Responsável por transformar roteiros e estratégias em ativos visuais de alto impacto.
    """
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_visual_prompts(
        self,
        script_text: str,
        brand_tone: str,
        audience_dna: str,
        creative_theme: str | None = None,
        scene_direction_pt: str | None = None,
    ) -> List[str]:
        """
        Recebe um roteiro e gera 3 opções de prompts visuais otimizados para IAs de imagem.
        Foca em: Composição, Iluminação, Estilo de Marca e Psicologia das Cores.
        """
        logger.info(f"🎨 Engenharia de Prompt Visual iniciada para: {brand_tone}")
        
        system_prompt = f"""
        Você é o 'Artisan', o Diretor de Arte do Conselho Leads AI (Dhawk Labs).
        Sua missão é criar prompts de imagem para DALL·E / geradores similares: ultra-realismo ou editorial premium para Instagram.

        CONTEXTO DA MARCA DO CLIENTE:
        - Tom: {brand_tone}
        - Público: {audience_dna}

        {_SORA_STRUCTURE_RULES}

        REGRAS ADICIONAIS:
        - Três variações por roteiro: (A) mais íntima / humana, (B) mais gráfica / conceito, (C) mais "authority" ou produto-contexto — sempre coerente com o texto do roteiro.
        - Nunca inclua texto legível, marcas ou UI fake com palavras na imagem.

        FORMATO DE SAÍDA (obrigatório):
        Retorne SOMENTE um objeto JSON válido neste formato exato:
        {{"prompts": ["prompt 1 em inglês", "prompt 2 em inglês", "prompt 3 em inglês"]}}
        Cada string deve ser um único parágrafo denso em inglês seguindo a estrutura acima (sem perguntas ao modelo, só descrição).
        """
        
        theme_extra = ""
        if creative_theme and str(creative_theme).strip():
            theme_extra = (
                f"\nTEMA CRIATIVO PRIORITÁRIO (pedido explícito do cliente — alinhe os 3 conceitos a isto): "
                f"{creative_theme.strip()}\n"
            )
        scene_extra = ""
        sd = (scene_direction_pt or "").strip()
        if sd:
            sd = sd[:1200]
            scene_extra = (
                f"\nDIREÇÃO VISUAL DO CONSELHO (português — traduza o clima e a composição para os prompts em inglês; "
                f"esta nota deve guiar enquadramento e metáfora, não um único objeto solto do texto. "
                f"Se citar papel/recibos/planilhas/telas com texto, mostre a MESMA tensão sem superfície legível: "
                f"sombras, profundidade de campo, gestos, textura abstrata.):\n{sd}\n"
            )
        user_msg = (
            f"Roteiro Sugerido: {script_text}\n"
            f"{theme_extra}"
            f"{scene_extra}\n"
            "Gere 3 conceitos visuais magnéticos para este post. "
            "Nenhum conceito pode incluir documentos, telas com texto, ou números legíveis. "
            "Integre roteiro + direção visual do conselho numa cena única coerente (sem ignorar a direção por um detalhe aleatório do roteiro)."
        )
        
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

    @staticmethod
    def wrap_prompt_for_dalle(inner_prompt: str) -> str:
        """
        Envelope estilo Sora (geração direta) + restrições seguras para API de imagem.
        """
        inner = (inner_prompt or "").strip()
        if not inner:
            return ""
        prefix = (
            "Generate a single photorealistic editorial photograph from this description only — "
            "do not ask questions. "
            "Strict ban: NO paper, documents, charts, spreadsheets, phone or laptop screens, "
            "no posters or signage with letters, no books with readable pages, "
            "no fake UI, no numbers or words visible anywhere in the frame. "
            "If the scene would normally need 'data', show abstract light, texture, hands without props, or blurred background only. "
            "No logos or watermarks.\n\n"
        )
        suffix = (
            "\n\nTechnical: cinematic lighting, shallow depth of field, ultra-detailed, "
            "natural skin texture where people appear, professional color grading, "
            "believable full-frame photography, square crop friendly for Instagram."
        )
        out = f"{prefix}{inner}{suffix}"
        return out[:_DALLE_CHAR_LIMIT]

    def create_image(self, prompt: str) -> str:
        """
        Chama a API de geração de imagem (DALL-E 3 por padrão).
        Retorna a URL da imagem gerada.
        """
        final_prompt = self.wrap_prompt_for_dalle(prompt)
        logger.info("📸 Gerando imagem DALL·E (chars=%s): %s...", len(final_prompt), final_prompt[:50])

        try:
            if self.provider == "openai":
                q = (os.getenv("LEADS_AI_IMAGE_QUALITY") or "standard").strip().lower()
                if q not in ("standard", "hd"):
                    q = "standard"
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=final_prompt,
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
