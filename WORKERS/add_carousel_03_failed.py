
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"

def add_carousel_03_failed():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    # Data aproximada (6 dias atrás)
    today = (datetime.now() - timedelta(days=6)).strftime("%d/%m/%Y")
    
    # Dados extraídos dos prints do "Fracasso" (Home Office/Celular)
    row_data = [
        "C_03",                         # ID_Print
        today,                          # Data
        "",                             # URL
        "CARROSSEL: Fomos Seduzidas (Capa Home Office)", # Tema_Descricao
        "Fomos seduzidas por um alívio rápido... (Legenda igual, Capa Ruim)", # Texto_Legenda
        "Carrossel",                    # Duração
        1091,                           # Views (Baixo)
        37,                             # Likes (Baixo)
        5,                              # Comentarios
        1,                              # Salvamentos (Pífio)
        0,                              # Compartilhamentos
        "",                             # Retenção
        ""                              # Tempo_Medio
    ]
    
    body = {
        'values': [row_data]
    }
    
    result = svc.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="BASE_DADOS!A:M",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    
    print(f"✅ Dados Anti-Exemplo (C_03) adicionados! (Range: {result.get('updates').get('updatedRange')})")

if __name__ == "__main__":
    add_carousel_03_failed()
