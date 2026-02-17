
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"

def add_carousel_data():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    # 1. Prepare data
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Values derived from the provided images
    row_data = [
        "C_01",                         # ID_Print (C_01 for Carrossel 01)
        today,                          # Data
        "",                             # URL
        "CARROSSEL: O luto que ninguém viu (Nevasca)", # Tema_Descricao
        "Há 7 anos nascia minha primeira filha... (Texto sobre Luto/Maternidade)", # Texto_Legenda
        "Carrossel",                    # Duração (Video)
        3501,                           # Views
        137,                            # Likes
        7,                              # Comentarios
        6,                              # Salvamentos
        3,                              # Compartilhamentos
        "",                             # Retenção (Média)
        ""                              # Tempo_Medio_View
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
    
    print(f"✅ Dados do Carrossel adicionados! (Range: {result.get('updates').get('updatedRange')})")

if __name__ == "__main__":
    add_carousel_data()
