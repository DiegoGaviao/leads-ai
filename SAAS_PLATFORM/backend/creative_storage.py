"""
Persistência de criativos gerados (OpenAI Images) no Supabase Storage.
URLs da OpenAI expiram; o bucket mantém links estáveis para e-mail e relatório.
"""
from __future__ import annotations

import logging
import os
import re
from typing import Optional, Tuple
from urllib.parse import quote

import requests

logger = logging.getLogger(__name__)


def slugify_storage_part(s: str, max_len: int = 72) -> str:
    raw = (s or "brand").strip().lower()
    raw = re.sub(r"[^\w\-]+", "-", raw, flags=re.UNICODE)
    raw = re.sub(r"-{2,}", "-", raw).strip("-") or "brand"
    return raw[:max_len]


def upload_remote_image_to_bucket(
    supabase,
    bucket: str,
    storage_path: str,
    source_url: str,
    timeout_s: int = 120,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Baixa a imagem de source_url e envia ao Storage.
    Retorna (public_url, erro_curto). public_url pode ser None se falhar.
    """
    try:
        r = requests.get(source_url, timeout=timeout_s)
        r.raise_for_status()
        content = r.content
        mime = r.headers.get("Content-Type", "").split(";")[0].strip() or "image/png"
        if "png" in mime:
            ext = "png"
        elif "jpeg" in mime or "jpg" in mime:
            ext = "jpg"
        elif "webp" in mime:
            ext = "webp"
        else:
            ext = "png"
            mime = "image/png"

        path = storage_path
        if not path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            path = f"{path}.{ext}"

        opts = {"content-type": mime, "upsert": "true"}
        supabase.storage.from_(bucket).upload(path, content, file_options=opts)

        base = os.getenv("SUPABASE_URL", "").rstrip("/")
        if not base:
            return None, "supabase_url_ausente"
        enc = quote(path, safe="/")
        public = f"{base}/storage/v1/object/public/{bucket}/{enc}"
        return public, None
    except requests.RequestException as e:
        logger.warning("Download criativo falhou: %s", e)
        return None, "download_falhou"
    except Exception as e:
        logger.warning("Upload Storage falhou (%s): %s", storage_path, e)
        return None, str(e)[:200]

