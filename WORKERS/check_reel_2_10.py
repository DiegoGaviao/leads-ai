
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"


def analyze_reels_range():
    print("🔍 Consultando métricas dos Reels ID 2 a 10...")
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    # Ler tudo
    result = svc.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="BASE_DADOS!A:M").execute()
    data = result.get('values', [])
    
    if not data: return
    
    print(f"\n{'ID':<5} | {'Views':<8} | {'Likes':<6} | {'Tema':<30}")
    print("-" * 60)

    for i in range(2, 11): # 2 a 10
        found = None
        target_id = str(i)
        
        for row in data[1:]:
            if row and str(row[0]).strip() == target_id:
                found = row
                break
        
        if found:
            # Mapear valores (A=0, G=6(Views), H=7(Likes), D=3(Tema))
            def get_val(idx): return found[idx] if len(found) > idx else "0"
            print(f"{target_id:<5} | {get_val(6):<8} | {get_val(7):<6} | {get_val(3)[:28]}")
        else:
            print(f"{target_id:<5} | ID não encontrado.")

if __name__ == "__main__":
    analyze_reels_range()
