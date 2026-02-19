import html as _html
import markdown as md_render

def get_professional_strategy_email(persona, estrategia, roteiros):
    """
    Retorna o HTML formatado com design PREMIMUM e suporte a Markdown.
    """
    # Converter Markdown para HTML
    persona_html = md_render.markdown(persona)
    estrategia_html = md_render.markdown(estrategia)
    
    # Formatação dos roteiros
    roteiros_html = ""
    for r_item in roteiros:
        tema = _html.escape(r_item.get('tema',''))
        visual = _html.escape(r_item.get('visual',''))
        texto = r_item.get('texto','')
        texto_html = md_render.markdown(texto)
        legenda = _html.escape(r_item.get('legenda',''))
        
        roteiros_html += f"""
        <div style="margin-bottom: 24px; padding: 24px; border-radius: 16px; border: 1px solid #e5e7eb; background-color: #ffffff; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);">
            <div style="display: flex; align-items: center; margin-bottom: 16px;">
                <span style="background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Roteiro Sugerido</span>
            </div>
            <h4 style="margin: 0 0 16px 0; color: #111827; font-size: 18px; font-weight: 800; line-height: 1.3;">{tema}</h4>
            
            {f'<div style="margin-bottom: 20px;"><div style="font-size: 11px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">Visual</div><div style="color: #4b5563; font-size: 14px; line-height: 1.5; padding-left: 12px; border-left: 2px solid #e5e7eb;">{visual}</div></div>' if visual else ''}
            
            <div style="margin-bottom: 20px;">
                <div style="font-size: 11px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">O que falar (Script)</div>
                <div style="color: #1f2937; font-size: 15px; line-height: 1.6; background-color: #f9fafb; padding: 16px; border-radius: 12px; border: 1px solid #f3f4f6;">{texto_html}</div>
            </div>
            
            {f'<div><div style="font-size: 11px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">Legenda</div><div style="color: #6b7280; font-size: 14px; font-style: italic;">{legenda}</div></div>' if legenda else ''}
        </div>
        """

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; font-family: 'Inter', Helvetica, Arial, sans-serif; background-color: #f3f4f6; color: #1f2937;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 16px;">
                <table role="presentation" style="width: 100%; max-width: 640px; border-collapse: collapse; background-color: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #000000; padding: 48px 40px; text-align: center;">
                            <div style="margin-bottom: 24px; display: inline-block;">
                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                                    </svg>
                                </div>
                            </div>
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 800; letter-spacing: -0.02em;">LEADS AI STRATEGY</h1>
                            <div style="margin-top: 12px; height: 1px; width: 40px; background-color: #3b82f6; margin-left: auto; margin-right: auto;"></div>
                        </td>
                    </tr>

                    <!-- Main content -->
                    <tr>
                        <td style="padding: 48px 40px;">
                            <p style="margin: 0 0 32px 0; font-size: 16px; line-height: 1.6; color: #4b5563;">
                                Olá, seu relatório de inteligência estratégica está pronto. Nossa IA consolidou seu DNA de marca com as métricas de performance para criar o seguinte plano:
                            </p>

                            <!-- Section: Persona -->
                            <div style="margin-bottom: 48px;">
                                <h2 style="margin: 0 0 20px 0; color: #111827; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; display: flex; align-items: center;">
                                    <span style="color: #2563eb; margin-right: 8px;">◈</span> DNA & Persona
                                </h2>
                                <div style="color: #374151; font-size: 15px; line-height: 1.8; padding: 24px; background-color: #f9fafb; border-radius: 16px; border: 1px solid #f3f4f6;">
                                    {persona_html}
                                </div>
                            </div>

                            <!-- Section: Strategy -->
                            <div style="margin-bottom: 48px;">
                                <h2 style="margin: 0 0 20px 0; color: #111827; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; display: flex; align-items: center;">
                                    <span style="color: #2563eb; margin-right: 8px;">◈</span> Direcionamento do Conselho
                                </h2>
                                <div style="color: #374151; font-size: 15px; line-height: 1.8;">
                                    {estrategia_html}
                                </div>
                            </div>

                            <!-- Section: Scripts -->
                            <div style="margin-bottom: 0;">
                                <h2 style="margin: 0 0 24px 0; color: #111827; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; display: flex; align-items: center;">
                                    <span style="color: #2563eb; margin-right: 8px;">◈</span> Roteiros de Alta Performance
                                </h2>
                                {roteiros_html}
                            </div>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="padding: 40px; background-color: #f9fafb; border-top: 1px solid #f3f4f6; text-align: center;">
                            <p style="margin: 0 0 16px 0; color: #9ca3af; font-size: 13px;">
                                Gerado por Inteligência Artificial — Leads AI v2
                            </p>
                            <div style="display: flex; justify-content: center; gap: 16px;">
                                <span style="color: #d1d5db;">•</span>
                                <span style="color: #6b7280; font-size: 12px; font-weight: 600;">dhawk.com.br</span>
                                <span style="color: #d1d5db;">•</span>
                            </div>
                        </td>
                    </tr>
                </table>
                <p style="margin-top: 24px; color: #9ca3af; font-size: 12px; text-align: center;">
                    Este e-mail é um produto exclusivo para uso estratégico.
                </p>
            </td>
        </tr>
    </table>
</body>
</html>
    """
    return html
