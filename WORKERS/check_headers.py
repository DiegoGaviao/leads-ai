
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"

def check_headers():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    result = svc.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="BASE_DADOS!A1:M1").execute()
    headers = result.get('values', [])[0]
    print(f"Headers: {headers}")

if __name__ == "__main__":
    check_headers()
