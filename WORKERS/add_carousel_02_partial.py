
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"

def add_carousel_02_partial():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    # Calcular data aproximada (6 dias atrás de 03/02)
    post_date = (datetime.now() - timedelta(days=6)).strftime("%d/%m/%Y")
    
    row_data = [
        "C_02",                         # ID_Print
        post_date,                      # Data
        "",                             # URL
        "CARROSSEL: Alívio Rápido vs Descanso Real (O Celular)", # Tema_Descricao
        "Fomos seduzidas por um alívio rápido... (Dispersão x Presença)", # Texto_Legenda
        "Carrossel",                    # Duração
        0,                              # Views (PENDENTE)
        37,                             # Likes (36 + 1 aprox. visível no print)
        4,                              # Comentarios (Visíveis no print)
        0,                              # Salvamentos (PENDENTE)
        0,                              # Compartilhamentos (PENDENTE)
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
    
    print(f"✅ Dados Parciais do Carrossel C_02 adicionados! (Range: {result.get('updates').get('updatedRange')})")

if __name__ == "__main__":
    add_carousel_02_partial()
