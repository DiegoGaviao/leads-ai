
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"

def analise_autoridade():
    print("👩‍⚕️ Caçando AUTORIDADE (Quem salva = Quem compra)...")
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    result = svc.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="BASE_DADOS!A:M").execute()
    data = result.get('values', [])
    cols = data[0]
    
    # Normalizar linhas (se faltar coluna no final, preenche com vazio)
    normalized_data = []
    for row in data[1:]:
        # Garante que a linha tenha o mesmo tamanho dos headers
        while len(row) < len(cols):
            row.append("")
        normalized_data.append(row)

    df = pd.DataFrame(normalized_data, columns=cols)
    
    # Converter para numérico
    df['Views'] = pd.to_numeric(df['Views'], errors='coerce').fillna(0)
    df['Salvamentos'] = pd.to_numeric(df['Salvamentos'], errors='coerce').fillna(0)
    
    # Criar Índice de Autoridade (Saves por 1k views)
    # Ex: 10 saves em 1000 views = 1.0%
    # É uma métrica mais justa que "Views totais" para medir PROFISSIONALISMO.
    
    df['Indice_Autoridade'] = (df['Salvamentos'] / df['Views']) * 1000
    
    # Filtrar vídeos com mín 500 views para não distorcer
    df_valid = df[df['Views'] > 500].copy()
    
    df_top = df_valid.sort_values(by='Indice_Autoridade', ascending=False).head(5)
    
    print("\n🏆 TOP 5 VÍDEOS DE AUTORIDADE (Que geram Clientes):")
    print("(Métrica: 'Salvamentos a cada 1.000 visualizações')")
    print("-" * 60)
    print(f"{'ID':<4} | {'Autoridade':<10} | {'Saves':<5} | {'Tema'}")
    print("-" * 60)
    
    for _, row in df_top.iterrows():
        score = f"{row['Indice_Autoridade']:.1f}"
        print(f"{row['ID_Print']:<4} | {score:<10} | {row['Salvamentos']:<5} | {row['Tema_Descricao']}")

    print("\n💡 INTERPRETAÇÃO:")
    print("Estes vídeos podem ter menos views, mas o público ACHOU MAIS ÚTIL.")
    print("Estes são os vídeos que vendem terapia, não apenas entretêm.")

if __name__ == "__main__":
    analise_autoridade()
