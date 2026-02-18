#!/usr/bin/env python3
import os
import sys
import json
from dotenv import load_dotenv
from database import get_supabase_client

# ReportLab for PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm

load_dotenv()


def fetch_latest_strategy_by_email(email: str):
    supabase = get_supabase_client()
    clients = supabase.table('clients').select('id,email').eq('email', email).execute()
    if not clients.data:
        print(f"Cliente com email {email} não encontrado.")
        return None
    client_id = clients.data[0]['id']
    res = supabase.table('strategies').select('*').eq('client_id', client_id).order('created_at', desc=True).limit(1).execute()
    if not res.data:
        print(f"Nenhuma estratégia encontrada para cliente {email}.")
        return None
    return res.data[0]


def build_pdf(strategy_record, out_path):
    doc = SimpleDocTemplate(out_path, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    h1 = styles['Heading1']
    h2 = styles['Heading2']
    elements = []

    sid = strategy_record.get('id')
    client_id = strategy_record.get('client_id')
    created = strategy_record.get('created_at')
    content = strategy_record.get('content_json') or {}

    elements.append(Paragraph('Sua Estratégia Leads AI', h1))
    elements.append(Spacer(1,6))
    meta = f"Strategy ID: {sid} — Client ID: {client_id} — Created: {created}"
    elements.append(Paragraph(meta, normal))
    elements.append(Spacer(1,12))

    # Persona
    persona = content.get('persona','') if isinstance(content, dict) else ''
    elements.append(Paragraph('Persona', h2))
    elements.append(Spacer(1,4))
    for line in str(persona).split('\n'):
        elements.append(Paragraph(line.strip().replace('  ','&nbsp;'), normal))
    elements.append(Spacer(1,8))

    # Estratégia
    estrategia = content.get('estrategia','') if isinstance(content, dict) else ''
    elements.append(Paragraph('Estratégia', h2))
    elements.append(Spacer(1,4))
    for line in str(estrategia).split('\n'):
        elements.append(Paragraph(line.strip(), normal))
    elements.append(Spacer(1,8))

    # Roteiros
    roteiros = content.get('roteiros', []) if isinstance(content, dict) else []
    elements.append(Paragraph('Roteiros', h2))
    elements.append(Spacer(1,4))
    if isinstance(roteiros, list) and roteiros:
        for idx, r in enumerate(roteiros, start=1):
            tema = r.get('tema','')
            texto = r.get('texto','')
            legenda = r.get('legenda','')
            elements.append(Paragraph(f"{idx}. {tema}", styles['Heading3']))
            elements.append(Paragraph(texto.replace('\n','<br/>'), normal))
            if legenda:
                elements.append(Paragraph(f"Legenda: {legenda}", normal))
            elements.append(Spacer(1,6))
    else:
        elements.append(Paragraph('Nenhum roteiro encontrado.', normal))

    doc.build(elements)
    print(f"PDF gerado: {out_path}")


def main():
    if len(sys.argv) < 2:
        print('Uso: generate_strategy_pdf.py --email seu@email.com')
        return
    email = None
    if sys.argv[1] in ('--email','-e') and len(sys.argv)>=3:
        email = sys.argv[2]
    else:
        print('Argumento inválido. Use --email')
        return

    strategy = fetch_latest_strategy_by_email(email)
    if not strategy:
        return

    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'LOGS')
    os.makedirs(logs_dir, exist_ok=True)
    out_path = os.path.join(logs_dir, f"strategy_{strategy.get('id')}.pdf")

    build_pdf(strategy, out_path)


if __name__ == '__main__':
    main()
