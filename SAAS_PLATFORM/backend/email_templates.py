
import html as _html

def get_professional_strategy_email(persona, estrategia, roteiros):
    """
    Retorna o HTML formatado de um e-mail profissional para a estratégia Leads AI,
    entregando todo o conteúdo diretamente no corpo do e-mail.
    """
    
    # Formatação dos roteiros
    roteiros_html = ""
    for r_item in roteiros:
        tema = _html.escape(r_item.get('tema',''))
        visual = _html.escape(r_item.get('visual',''))
        texto = _html.escape(r_item.get('texto',''))
        legenda = _html.escape(r_item.get('legenda',''))
        
        roteiros_html += f"""
        <div style="margin-bottom: 24px; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc;">
            <h4 style="margin: 0 0 12px 0; color: #2563eb; font-size: 17px; font-weight: 800; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">{tema}</h4>
            
            {f'<div style="margin-bottom: 12px;"><strong style="font-size: 13px; color: #64748b; text-transform: uppercase;">🎬 O que mostrar visualmente:</strong><br><span style="color: #334155; font-size: 14px;">{visual}</span></div>' if visual else ''}
            
            <div style="margin-bottom: 12px;">
                <strong style="font-size: 13px; color: #64748b; text-transform: uppercase;">🎙️ Roteiro / Texto:</strong><br>
                <div style="color: #1e293b; font-size: 15px; line-height: 1.6; white-space: pre-wrap; background: #ffffff; padding: 12px; border-radius: 8px; border: 1px solid #edf2f7; margin-top: 4px;">{texto}</div>
            </div>
            
            {f'<div><strong style="font-size: 13px; color: #64748b; text-transform: uppercase;">📝 Legenda sugerida:</strong><br><div style="color: #475569; font-size: 13px; font-style: italic; margin-top: 4px;">{legenda}</div></div>' if legenda else ''}
        </div>
        """

    # Escape Persona e Estratégia
    persona_escaped = _html.escape(persona)
    estrategia_escaped = _html.escape(estrategia)

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sua Estratégia Leads AI</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f1f5f9; color: #1e293b;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table role="presentation" style="width: 100%; max-width: 600px; border-collapse: collapse; background-color: #ffffff; border-radius: 16px; overflow: hidden; shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); padding: 40px 40px 30px 40px; text-align: center;">
                            <div style="display: inline-block; background-color: rgba(255, 255, 255, 0.2); padding: 12px; border-radius: 12px; margin-bottom: 20px;">
                                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                                </svg>
                            </div>
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 800; letter-spacing: -0.025em;">Leads AI</h1>
                            <p style="margin: 8px 0 0 0; color: #bfdbfe; font-size: 16px;">Sua estratégia completa está aqui!</p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin: 0 0 24px 0; font-size: 16px; line-height: 1.6; color: #475569;">
                                Olá! Analisamos seu perfil e objetivos com nossa Inteligência Artificial e preparamos seu plano de ação completo. Você pode copiar o conteúdo abaixo para implementar hoje mesmo.
                            </p>

                            <!-- Section: Persona -->
                            <div style="margin-bottom: 32px;">
                                <h2 style="display: flex; align-items: center; margin: 0 0 16px 0; color: #1e293b; font-size: 18px; font-weight: 700;">
                                    <span style="display: inline-block; width: 4px; height: 18px; background-color: #2563eb; border-radius: 2px; margin-right: 10px;"></span>
                                    Sua Persona Ideal
                                </h2>
                                <div style="padding: 20px; background-color: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; color: #334155; font-size: 15px; line-height: 1.7; white-space: pre-wrap;">{persona_escaped}</div>
                            </div>

                            <!-- Section: Strategy -->
                            <div style="margin-bottom: 32px;">
                                <h2 style="display: flex; align-items: center; margin: 0 0 16px 0; color: #1e293b; font-size: 18px; font-weight: 700;">
                                    <span style="display: inline-block; width: 4px; height: 18px; background-color: #2563eb; border-radius: 2px; margin-right: 10px;"></span>
                                    Direcionamento Estratégico
                                </h2>
                                <div style="padding: 20px; background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; color: #334155; font-size: 15px; line-height: 1.7; white-space: pre-wrap;">{estrategia_escaped}</div>
                            </div>

                            <!-- Section: Scripts -->
                            <div style="margin-bottom: 20px;">
                                <h2 style="display: flex; align-items: center; margin: 0 0 16px 0; color: #1e293b; font-size: 18px; font-weight: 700;">
                                    <span style="display: inline-block; width: 4px; height: 18px; background-color: #2563eb; border-radius: 2px; margin-right: 10px;"></span>
                                    Roteiros de Conteúdo
                                </h2>
                                {roteiros_html}
                            </div>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px 40px; background-color: #f8fafc; border-top: 1px solid #e2e8f0; text-align: center;">
                            <p style="margin: 0; color: #64748b; font-size: 14px;">
                                &copy; 2026 Leads AI. Todos os direitos reservados.
                            </p>
                            <p style="margin: 8px 0 0 0; color: #94a3b8; font-size: 12px;">
                                Este conteúdo foi gerado exclusivamente para drmgaviao@gmail.com.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """
    return html
