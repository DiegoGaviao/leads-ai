
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"

def processar_score(row):
    # Pesos Estratégicos (V2)
    P_VIEW = 1
    P_LIKE = 2
    P_COMENT = 5
    P_SAVE = 10    # Ouro
    P_SHARE = 10   # Viral
    
    # Garante inteiros
    try:
        views = int(row.get('Views', 0))
        if views == 0: views = 1 # Evita div/0
        likes = int(row.get('Likes', 0))
        coments = int(row.get('Coments', 0))
        saves = int(row.get('Salvos', 0))
        shares = int(row.get('Shares', 0))
    except:
        return pd.Series([0, 0, "N/A"])

    score_bruto = (views*P_VIEW) + (likes*P_LIKE) + (coments*P_COMENT) + (saves*P_SAVE) + (shares*P_SHARE)
    
    interacoes = likes + coments + saves + shares
    taxa_engajamento = (interacoes / views) * 100
    
    return pd.Series([score_bruto, taxa_engajamento])

def gerar_analise():
    print("🧠 Conectando ao Cérebro (Google Sheets)...")
    
    # 1. Baixar Dados
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    result = svc.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="BASE_DADOS!A:K").execute()
    values = result.get('values', [])
    
    if not values:
        print("Planilha vazia!")
        return

    df = pd.DataFrame(values[1:], columns=values[0])
    print(f"✅ Lidos {len(df)} registros.")
    
    # 2. Processar (Recalcular tudo, pois o usuário só insere dados brutos)
    print("⚙️ Processando Scores e Classificações...")
    df[['Score_Calculado', 'Engajamento_Calculado']] = df.apply(processar_score, axis=1)
    
    # Classificação Relativa (Percentis)
    # Apenas para linhas com views válidos
    df['Score_Calculado'] = pd.to_numeric(df['Score_Calculado'])
    valid_reels = df[df['Score_Calculado'] > 0].copy()
    
    if len(valid_reels) < 5:
        print("⚠️ Poucos dados para análise estatística (<5). Classificação será provisória.")
        p33, p66 = 1000, 5000 # Chute se não tiver dados
    else:
        p33 = valid_reels['Score_Calculado'].quantile(0.33)
        p66 = valid_reels['Score_Calculado'].quantile(0.66)
    
    def classificar(score):
        if score >= p66: return "🏆 BOM"
        if score <= p33: return "🔻 RUIM"
        return "🔸 MÉDIO"
        
    df['Classificacao_AI'] = df['Score_Calculado'].apply(classificar)
    
    # 3. Gerar Relatório Simples
    print("\n" + "="*40)
    print("📊 RELATÓRIO DE PERFORMANCE (V2)")
    print("="*40)
    
    top_3 = df.sort_values(by='Score_Calculado', ascending=False).head(3)
    print(f"\n🏆 TOP 3 REELS DA HISTÓRIA:")
    for i, row in top_3.iterrows():
        print(f"1. {row.get('Tema_Descricao', 'Sem Título')} | Score: {row['Score_Calculado']:.0f} | Class: {row['Classificacao_AI']}")
        
    print("\n💡 INSIGHT RÁPIDO:")
    media_views = pd.to_numeric(df['Views'], errors='coerce').mean()
    print(f"Sua média de views é: {media_views:.0f}. Todo vídeo acima disso é lucro.")
    
    # Salvar localmente para registro
    df.to_csv("backup_analise_recente.csv", index=False)
    print("\n✅ Análise concluída. Dados salvos em 'backup_analise_recente.csv'.")

if __name__ == "__main__":
    gerar_analise()
