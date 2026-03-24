"""
Agregados anônimos a partir de `leads_ai_posts` para enriquecer a geração de estratégia
sem expor dados identificáveis de outras marcas (apenas estatísticas agregadas).
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

MAX_SAMPLE = 2500


def _score(row: Dict[str, Any]) -> float:
    """Score simples de engajamento para ranquear posts na amostra."""
    if row.get("engagement_score") is not None:
        try:
            return float(row["engagement_score"])
        except (TypeError, ValueError):
            pass
    v = int(row.get("views") or 0)
    return float(
        int(row.get("likes") or 0)
        + int(row.get("comments") or 0) * 2
        + int(row.get("shares") or 0) * 2
        + int(row.get("saves") or 0) * 2
        + min(v, 1_000_000) / 1000.0
    )


def _avg_metrics(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    if not rows:
        return {}
    keys = ("views", "likes", "comments", "shares", "saves")
    out: Dict[str, float] = {}
    n = len(rows)
    for k in keys:
        out[k] = sum(int(r.get(k) or 0) for r in rows) / n
    return out


def build_client_posts_summary(posts: List[Dict[str, Any]]) -> str:
    """Resumo numérico dos posts do próprio cliente (sem LLM)."""
    if not posts:
        return "Posts do cliente: nenhum registro ainda — priorize o questionário e hipóteses conservadoras."

    scored = sorted(posts, key=_score, reverse=True)
    top = scored[: min(5, len(scored))]
    avg = _avg_metrics(posts)

    lines = [
        "=== Posts deste cliente (resumo interno) ===",
        f"Amostra: {len(posts)} post(s). Médias: views≈{avg.get('views', 0):.0f}, "
        f"likes≈{avg.get('likes', 0):.0f}, comentários≈{avg.get('comments', 0):.0f}, "
        f"compartilhamentos≈{avg.get('shares', 0):.0f}, salvamentos≈{avg.get('saves', 0):.0f}.",
        "Maiores desempenhos relativos (métricas agregadas, sem expor concorrentes):",
    ]
    for i, p in enumerate(top, 1):
        lines.append(
            f"  {i}) views={p.get('views')}, likes={p.get('likes')}, "
            f"comments={p.get('comments')}, shares={p.get('shares')}, saves={p.get('saves')}"
            f" | tipo={p.get('media_type') or '—'}"
        )
    return "\n".join(lines)


def build_anonymous_market_suggestions(
    supabase: Any,
    exclude_brand_id: Optional[str] = None,
) -> str:
    """
    Estatísticas agregadas sobre outras marcas na base (exclui a marca atual se informado).
    Não inclui permalink, handle ou identificadores.
    """
    try:
        q = (
            supabase.table("leads_ai_posts")
            .select("views,likes,comments,shares,saves,media_type,engagement_score,brand_id")
            .limit(MAX_SAMPLE)
        )
        res = q.execute()
        rows = res.data or []
    except Exception as e:
        logger.warning("market_insights: falha ao ler leads_ai_posts: %s", e)
        return (
            "Sugestões de mercado (referência agregada): indisponível no momento — "
            "use apenas o questionário e os posts do cliente."
        )

    if exclude_brand_id:
        rows = [r for r in rows if str(r.get("brand_id")) != str(exclude_brand_id)]

    if len(rows) < 8:
        return (
            "Sugestões de mercado (referência agregada anônima): base ainda pequena para benchmark — "
            "trate como inspiração leve; priorize sempre o DNA do questionário e os posts do cliente."
        )

    scored = sorted(rows, key=_score, reverse=True)
    n = len(scored)
    k = max(2, n // 4)
    top_q = scored[:k]
    bottom_q = scored[-k:]

    avg_top = _avg_metrics(top_q)
    avg_bot = _avg_metrics(bottom_q)

    # Por tipo de mídia (apenas contagem agregada)
    by_type: Dict[str, int] = {}
    for r in rows:
        mt = (r.get("media_type") or "unknown").strip() or "unknown"
        by_type[mt] = by_type.get(mt, 0) + 1
    top_types = sorted(by_type.items(), key=lambda x: -x[1])[:4]
    types_txt = ", ".join(f"{t} ({c})" for t, c in top_types)

    text = f"""=== Sugestões de mercado (referência agregada ANÔNIMA) ===
Estas linhas descrevem apenas padrões numéricos agregados na base Leads AI, sem identificar marcas ou posts.

Amostra analisada: {n} registros (excluída a marca atual para o benchmark cruzado).
Distribuição por tipo de mídia (contagem): {types_txt}.

Comparação quartil superior vs inferior (métricas médias):
- Quartil superior (maior score composto): views≈{avg_top.get('views', 0):.0f}, likes≈{avg_top.get('likes', 0):.0f}, comentários≈{avg_top.get('comments', 0):.0f}, compartilhamentos≈{avg_top.get('shares', 0):.0f}, salvamentos≈{avg_top.get('saves', 0):.0f}.
- Quartil inferior: views≈{avg_bot.get('views', 0):.0f}, likes≈{avg_bot.get('likes', 0):.0f}, comentários≈{avg_bot.get('comments', 0):.0f}, compartilhamentos≈{avg_bot.get('shares', 0):.0f}, salvamentos≈{avg_bot.get('saves', 0):.0f}.

INSTRUÇÃO DE USO: use isto como calibragem de mercado e hipóteses de formato — não copie conteúdo de terceiros.
A essência da marca vem do questionário e dos próprios posts do cliente acima."""

    return text


def build_full_insights_block(
    supabase: Any,
    client_posts: List[Dict[str, Any]],
    brand_id: str,
) -> str:
    """Bloco completo passado como `insights` para `generate_strategy`."""
    part_a = build_client_posts_summary(client_posts)
    part_b = build_anonymous_market_suggestions(supabase, exclude_brand_id=brand_id)
    return f"{part_a}\n\n{part_b}"
