
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"

def analyze_reel_1():
    print("🔍 Consultando métricas do Reel ID 1...")
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    # Ler tudo
    result = svc.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="BASE_DADOS!A:M").execute()
    data = result.get('values', [])
    
    if not data: return
    
    # Encontrar linha com ID_Print == 1
    headers = data[0]
    found = None
    
    for row in data[1:]:
        if row and str(row[0]).strip() == "1":
            found = row
            break
            
    if found:
        # Mapear valores (pode faltar coluna se a linha for curta)
        def get_val(idx): return found[idx] if len(found) > idx else "0"
        
        # Índices esperados (A=0 ... G=Views(6), H=Likes(7), I=Coments(8), J=Saves(9))
        print(f"\n📊 DADOS DO REEL #1 (As Rosas):")
        print(f"   Views: {get_val(6)}")
        print(f"   Saves: {get_val(9)}")
        print(f"   Tema: {get_val(3)}")
    else:
        print("❌ ID 1 não encontrado na planilha. Verifique se digitou '1' na coluna A.")

if __name__ == "__main__":
    analyze_reel_1()
