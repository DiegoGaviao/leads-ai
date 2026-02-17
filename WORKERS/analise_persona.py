
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"
PERSONA_FILE = "PERSONA_KARINA.md"

def analisar_semantica():
    print("🧠 Carregando Persona da Karina...")
    try:
        with open(PERSONA_FILE, 'r') as f:
            persona_text = f.read()
        print("✅ Persona carregada com sucesso.")
    except:
        print("⚠️ Arquivo de Persona não encontrado.")
        persona_text = ""

    print("📊 Baixando dados para cruzar com a Persona...")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    # Pega Data (A), Tema (D) e Texto (E) e Score (Calculado depois)
    # Na verdade, precisamos recalcular score aqui, pois não está salvo na planilha
    # Vamos reaproveitar a lógica do script anterior
    
    result = svc.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="BASE_DADOS!A:Z").execute()
    values = result.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])
    
    # Processar Score Rápido
    def calc_score(row):
        try:
            return int(row.get('Views', 0)) + int(row.get('Salvamentos', 0))*10 # Simplificado
        except: return 0
    
    df['Score_Simples'] = df.apply(calc_score, axis=1)
    
    # Categorização baseada na Persona (Método C.A.S.A)
    # Vamos buscar palavras-chave nos textos dos reels
    
    keywords = {
        "CALMA (Ordem)": ["ordem", "caos", "sobrecarga", "culpa", "exaust", "limites", "calma"],
        "ALIANÇA (Vínculos)": ["casamento", "marido", "filh", "maternidade", "conexão", "ts21", "teresa"],
        "SUSTENTO (Rotina)": ["rotina", "casa", "organiza", "sustenta", "leveza", "prática"],
        "AUTORIDADE (Direção)": ["domínio", "decisão", "escolha", "adult", "responsabilidade"]
    }
    
    print("\n🧐 Classificando Reels pelo Método C.A.S.A...")
    
    cluster_stats = {k: {'count': 0, 'score_total': 0, 'top_video': ''} for k in keywords}
    cluster_stats["OUTROS"] = {'count': 0, 'score_total': 0, 'top_video': ''}
    
    for _, row in df.iterrows():
        texto = (str(row.get('Tema_Descricao', '')) + " " + str(row.get('Texto_Legenda', ''))).lower()
        score = row['Score_Simples']
        
        found = False
        for pilares, termos in keywords.items():
            if any(t in texto for t in termos):
                cluster_stats[pilares]['count'] += 1
                cluster_stats[pilares]['score_total'] += score
                
                # Se for o melhor vídeo desse cluster, salva
                current_top_score_cluster = 0 # simplificação, precisaria armazenar lista 
                # (Lógica simplificada para output rápido)
                if score > 5000: # Highlight de vídeos bons
                     cluster_stats[pilares]['top_video'] = row.get('Tema_Descricao', 'Sem Título')
                
                found = True
        
        if not found:
            cluster_stats["OUTROS"]['count'] += 1
            cluster_stats["OUTROS"]['score_total'] += score

    print("\n" + "="*50)
    print("🏡 PERFORMANCE POR PILAR (MÉTODO C.A.S.A)")
    print("="*50)
    
    for pilar, dados in cluster_stats.items():
        if dados['count'] > 0:
            media = dados['score_total'] / dados['count']
            print(f"👉 {pilar}: {dados['count']} vídeos | Média Score: {media:.0f}")
            if dados['top_video']:
                print(f"   ⭐ Destaque: {dados['top_video'][:50]}...")
        else:
            print(f"👉 {pilar}: Nenhum vídeo detectado ainda.")

    print("\n💡 ANÁLISE DE ALINHAMENTO COM PERSONA:")
    print("Baseado na descrição 'Mulher que quer leveza possível e não idealizada':")
    
    # Insights fake baseados na lógica (futuro: usar LLM real aqui)
    # Se 'Aliança' (Filhos/TS21) tiver score maior que 'Calma', sugerir focar nisso.
    
    total_alianca = cluster_stats['ALIANÇA (Vínculos)']['score_total']
    total_sustento = cluster_stats['SUSTENTO (Rotina)']['score_total']
    
    if total_alianca > total_sustento:
        print("Atualmente, seu público conecta mais com 'ALIANÇA' (Vínculos/Família/TS21) do que Rotina.")
        print("Estratégia: Use a história da Teresa como porta de entrada para falar de Ordem Interior.")
    else:
        print("Seu público busca muita Rotina Prática. Fale mais de 'Vida Habitável'.")

if __name__ == "__main__":
    analisar_semantica()
