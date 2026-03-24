import html as _html
import markdown as md_render
import re


def _render_md(md_text: str) -> str:
    """Convert markdown and apply conservative inline styles for email clients."""
    raw_html = md_render.markdown(md_text or "", extensions=["extra", "sane_lists"])
    replacements = (
        (r"<h1>", '<h1 style="margin:0 0 12px 0;font-size:22px;line-height:1.3;color:#0f172a;">'),
        (r"<h2>", '<h2 style="margin:20px 0 10px 0;font-size:18px;line-height:1.35;color:#0f172a;">'),
        (r"<h3>", '<h3 style="margin:16px 0 8px 0;font-size:16px;line-height:1.4;color:#0f172a;">'),
        (r"<p>", '<p style="margin:0 0 12px 0;font-size:15px;line-height:1.7;color:#334155;">'),
        (r"<ul>", '<ul style="margin:8px 0 14px 22px;padding:0;color:#334155;">'),
        (r"<ol>", '<ol style="margin:8px 0 14px 22px;padding:0;color:#334155;">'),
        (r"<li>", '<li style="margin:0 0 8px 0;font-size:15px;line-height:1.65;">'),
        (
            r"<blockquote>",
            '<blockquote style="margin:12px 0;padding:10px 14px;border-left:3px solid #10b981;background:#ecfdf5;color:#065f46;">',
        ),
        (r"<strong>", '<strong style="color:#0f172a;font-weight:700;">'),
        (r"<em>", '<em style="color:#1e293b;">'),
        (r"<code>", '<code style="background:#f1f5f9;padding:2px 4px;border-radius:4px;color:#0f172a;">'),
        (r"<a ", '<a style="color:#0f766e;text-decoration:underline;" '),
    )
    for old, new in replacements:
        raw_html = re.sub(old, new, raw_html, flags=re.IGNORECASE)
    return raw_html


def _render_roteiros(roteiros) -> str:
    blocks = []
    safe_roteiros = roteiros or []
    for idx, r_item in enumerate(safe_roteiros, start=1):
        tema = _html.escape((r_item or {}).get("tema", "")).strip() or f"Roteiro {idx}"
        visual = _html.escape((r_item or {}).get("visual", "")).strip()
        legenda = _html.escape((r_item or {}).get("legenda", "")).strip()
        texto_html = _render_md((r_item or {}).get("texto", ""))

        visual_block = ""
        if visual:
            visual_block = f"""
            <tr>
              <td style="padding-top:12px;">
                <div style="font-size:11px;font-weight:700;letter-spacing:.08em;color:#64748b;text-transform:uppercase;margin-bottom:6px;">Visual sugerido</div>
                <div style="font-size:14px;line-height:1.6;color:#475569;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:10px 12px;">{visual}</div>
              </td>
            </tr>
            """

        legenda_block = ""
        if legenda:
            legenda_block = f"""
            <tr>
              <td style="padding-top:12px;">
                <div style="font-size:11px;font-weight:700;letter-spacing:.08em;color:#64748b;text-transform:uppercase;margin-bottom:6px;">Legenda sugerida</div>
                <div style="font-size:14px;line-height:1.6;color:#475569;font-style:italic;">{legenda}</div>
              </td>
            </tr>
            """

        blocks.append(
            f"""
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:separate;border-spacing:0;margin:0 0 18px 0;border:1px solid #dbeafe;border-radius:14px;background:#ffffff;">
              <tr>
                <td style="padding:16px 16px 14px 16px;border-bottom:1px solid #e2e8f0;background:#f8fafc;border-top-left-radius:14px;border-top-right-radius:14px;">
                  <span style="display:inline-block;background:#ecfeff;border:1px solid #99f6e4;color:#0f766e;border-radius:999px;padding:4px 10px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;">Roteiro {idx}</span>
                  <h3 style="margin:10px 0 0 0;font-size:18px;line-height:1.35;color:#0f172a;">{tema}</h3>
                </td>
              </tr>
              <tr>
                <td style="padding:14px 16px 16px 16px;">
                  <div style="font-size:11px;font-weight:700;letter-spacing:.08em;color:#64748b;text-transform:uppercase;margin-bottom:6px;">Script (o que falar)</div>
                  <div style="font-size:15px;line-height:1.7;color:#1f2937;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px;">
                    {texto_html}
                  </div>
                  {visual_block}
                  {legenda_block}
                </td>
              </tr>
            </table>
            """
        )
    return "".join(blocks) or (
        '<div style="font-size:14px;line-height:1.6;color:#64748b;border:1px dashed #cbd5e1;border-radius:12px;padding:14px;">'
        "Sem roteiros no momento. Refaça a geração para obter novas sugestões."
        "</div>"
    )


def get_professional_strategy_email(persona, estrategia, roteiros):
    """Retorna HTML premium com foco em legibilidade executiva e compatibilidade de e-mail."""
    persona_html = _render_md(persona)
    estrategia_html = _render_md(estrategia)
    roteiros_html = _render_roteiros(roteiros)
    total_roteiros = len(roteiros or [])

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Leads AI - Relatorio Estrategico</title>
</head>
<body style="margin:0;padding:0;background:#f1f5f9;font-family:Inter,Segoe UI,Roboto,Arial,sans-serif;color:#0f172a;">
  <div style="display:none;font-size:1px;color:#f1f5f9;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">
    Seu relatorio estrategico Leads AI esta pronto com diagnostico e roteiros acionaveis.
  </div>

  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
    <tr>
      <td align="center" style="padding:26px 12px 34px 12px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:680px;border-collapse:separate;border-spacing:0;background:#ffffff;border-radius:20px;overflow:hidden;border:1px solid #e2e8f0;">
          <tr>
            <td style="padding:34px 26px;background:#0f172a;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td>
                    <div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#93c5fd;font-weight:700;">Leads AI | Dhawk Labs</div>
                    <h1 style="margin:10px 0 0 0;color:#ffffff;font-size:27px;line-height:1.22;">Relatorio Estrategico Profissional</h1>
                    <p style="margin:10px 0 0 0;color:#cbd5e1;font-size:14px;line-height:1.55;">
                      Diagnostico de DNA + direcionamento do conselho + roteiros prontos para gravacao.
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:20px 26px;border-bottom:1px solid #e2e8f0;background:#f8fafc;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td style="padding:0 8px 0 0;">
                    <div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-bottom:6px;">Status</div>
                    <div style="font-size:14px;color:#065f46;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:999px;padding:6px 10px;display:inline-block;font-weight:700;">Pronto para execucao</div>
                  </td>
                  <td style="padding:0 0 0 8px;" align="right">
                    <div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-bottom:6px;">Roteiros</div>
                    <div style="font-size:14px;color:#0f172a;background:#eef2ff;border:1px solid #c7d2fe;border-radius:999px;padding:6px 10px;display:inline-block;font-weight:700;">{total_roteiros} sugestoes</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:28px 26px 8px 26px;">
              <h2 style="margin:0 0 14px 0;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:#0f766e;">DNA & Persona</h2>
              <div style="border:1px solid #e2e8f0;border-radius:14px;padding:16px;background:#ffffff;">
                {persona_html}
              </div>
            </td>
          </tr>

          <tr>
            <td style="padding:22px 26px 8px 26px;">
              <h2 style="margin:0 0 14px 0;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:#0f766e;">Direcionamento Estrategico</h2>
              <div style="border:1px solid #e2e8f0;border-radius:14px;padding:16px;background:#ffffff;">
                {estrategia_html}
              </div>
            </td>
          </tr>

          <tr>
            <td style="padding:22px 26px 10px 26px;">
              <h2 style="margin:0 0 14px 0;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:#0f766e;">Roteiros de Alta Performance</h2>
              {roteiros_html}
            </td>
          </tr>

          <tr>
            <td style="padding:8px 26px 30px 26px;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:separate;border-spacing:0;background:#ecfeff;border:1px solid #99f6e4;border-radius:14px;">
                <tr>
                  <td style="padding:16px;">
                    <div style="font-size:12px;color:#0f766e;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px;">Proximo passo recomendado</div>
                    <div style="font-size:14px;line-height:1.65;color:#134e4a;">
                      Grave os dois primeiros roteiros nas proximas 48h e acompanhe desempenho para recalibrar o proximo ciclo.
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:18px 26px;background:#f8fafc;border-top:1px solid #e2e8f0;text-align:center;">
              <p style="margin:0 0 8px 0;font-size:13px;line-height:1.5;color:#64748b;">
                Gerado automaticamente pelo <strong style="color:#0f172a;">Leads AI</strong>.
              </p>
              <p style="margin:0;font-size:12px;line-height:1.5;color:#94a3b8;">
                Dhawk Labs · Estrategia de conteudo orientada por dados
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
