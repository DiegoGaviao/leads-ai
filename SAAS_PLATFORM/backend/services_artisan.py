import logging
import os
import time
import uuid

from AGENTS.agent_artisan.artisan_agent import ArtisanAgent
from creative_storage import slugify_storage_part, upload_remote_image_to_bucket
from database import get_supabase_client

logger = logging.getLogger("VisualService")


def _fallback_dalle_prompt(
    post: dict,
    brand_tone: str,
    audience_dna: str,
    creative_theme: str | None = None,
) -> str:
    """Quando o Artisan não devolve JSON de prompts, ainda tentamos 1 imagem no estilo do roteiro."""
    tema = (post.get("tema") or "").strip()
    visual = (post.get("visual") or "").strip()
    body = (post.get("texto") or "")[:1200].strip()
    parts = [
        "Premium editorial photograph for Instagram square crop, cinematic lighting, shallow depth of field.",
        f"Brand tone: {brand_tone}. Audience: {audience_dna}.",
        "No documents, no screens, no charts, no printed or digital text visible in frame.",
    ]
    if creative_theme and str(creative_theme).strip():
        parts.append(f"Client-requested creative theme (priority): {creative_theme.strip()}")
    if visual:
        parts.append(f"Scene direction: {visual}")
    if tema:
        parts.append(f"Hook topic: {tema}")
    if body and not visual:
        parts.append(f"Narrative mood only (abstract, no typography in frame): {body[:400]}")
    parts.append("Photorealistic, tasteful, no text, no logos, no watermarks, no paper props.")
    return " ".join(parts)[:3500]


def _creatives_enabled() -> bool:
    v = (os.getenv("LEADS_AI_GENERATE_CREATIVES") or "true").strip().lower()
    return v in ("1", "true", "yes", "on")


class VisualService:
    """
    Geração de criativos (imagens) por roteiro + upload estável no Supabase Storage.
    """

    @staticmethod
    def enrich_report_with_images(
        strategy_json: dict,
        brand_tone: str,
        audience_dna: str,
        *,
        storage_slug: str = "brand",
        supabase_client=None,
        post_themes: list | None = None,
    ) -> dict:
        if not _creatives_enabled():
            logger.info("Criativos automáticos desligados (LEADS_AI_GENERATE_CREATIVES).")
            return strategy_json
        if not os.getenv("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY ausente — pulando geração de criativos.")
            return strategy_json

        artisan = ArtisanAgent()
        slug = slugify_storage_part(storage_slug)
        bucket = (os.getenv("LEADS_AI_CREATIVES_BUCKET") or "leads-ai-creatives").strip()
        supabase = supabase_client or get_supabase_client()
        run_id = uuid.uuid4().hex[:10]
        base_ts = int(time.time())

        logger.info(
            "Enriquecendo relatório com criativos (bucket=%s, slug=%s, LEADS_AI_GENERATE_CREATIVES=%s)",
            bucket,
            slug,
            os.getenv("LEADS_AI_GENERATE_CREATIVES", "true"),
        )

        if "roteiros" not in strategy_json:
            return strategy_json

        themes_list = post_themes if isinstance(post_themes, list) else []

        for i, post in enumerate(strategy_json["roteiros"]):
            if not isinstance(post, dict):
                continue
            script_text = post.get("texto") or post.get("tema") or ""
            if not str(script_text).strip():
                continue

            creative_theme = None
            if i < len(themes_list) and str(themes_list[i] or "").strip():
                creative_theme = str(themes_list[i]).strip()
                post["tema_criativo_cliente"] = creative_theme

            try:
                prompts = artisan.generate_visual_prompts(
                    script_text,
                    brand_tone,
                    audience_dna,
                    creative_theme=creative_theme,
                )
            except Exception as e:
                logger.warning("Falha nos prompts visuais roteiro %s: %s", i + 1, e)
                prompts = []

            if prompts:
                post["visual_prompts"] = prompts
                post["visual_suggestion"] = prompts[0]

            primary = (prompts[0] if prompts else "").strip()
            if not primary:
                primary = _fallback_dalle_prompt(
                    post, brand_tone, audience_dna, creative_theme=creative_theme
                )
                post["visual_suggestion"] = primary
                logger.info("Roteiro %s: usando prompt visual fallback (Artisan vazio).", i + 1)

            if not primary.strip():
                logger.warning("Roteiro %s: sem texto/tema para imagem — pulando.", i + 1)
                continue

            try:
                temp_url = artisan.create_image(primary)
            except Exception as e:
                logger.warning("create_image falhou roteiro %s: %s", i + 1, e)
                continue

            if not temp_url:
                continue

            idx = post.get("index", i + 1)
            storage_path = f"{slug}/{run_id}/roteiro-{idx}-{base_ts}.png"
            stable_url, err = upload_remote_image_to_bucket(
                supabase, bucket, storage_path, temp_url
            )
            if stable_url:
                post["image_url"] = stable_url
                post["creative_storage_path"] = storage_path
                logger.info("Criativo salvo roteiro %s", idx)
            else:
                post["image_url"] = temp_url
                post["image_url_ephemeral"] = True
                logger.warning(
                    "Storage não disponível (%s); usando URL temporária OpenAI.", err
                )

        return strategy_json


def apply_strategy_creatives(strategy_json: dict, briefing_dict: dict, storage_slug: str) -> dict:
    """
    Entrada única para pipeline: deriva tom/público do briefing e aplica imagens.
    """
    tone = (briefing_dict.get("tone_voice") or "Profissional").strip()
    audience = (
        briefing_dict.get("dream_client")
        or briefing_dict.get("pain_point")
        or "Público no Instagram"
    )
    if not str(audience).strip():
        audience = "Público no Instagram"
    pt = briefing_dict.get("post_themes")
    if not isinstance(pt, list):
        pt = []
    try:
        return VisualService.enrich_report_with_images(
            strategy_json,
            tone,
            str(audience).strip(),
            storage_slug=storage_slug or "brand",
            post_themes=pt,
        )
    except Exception:
        logger.exception(
            "apply_strategy_creatives abortou; entregando relatório só com texto. "
            "Verifique logs e deploy."
        )
        return strategy_json
