
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1jA0qPWAPsQMEaj99zccaEG3S69hcUfWddD451uYlY8w"

def clean_columns():
    print("🧹 Iniciando limpeza de colunas lixo...")
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    svc = build("sheets", "v4", credentials=creds)
    
    # 1. Ler Headers atuais
    result = svc.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="BASE_DADOS!1:1").execute()
    headers = result.get('values', [[]])[0]
    
    print("Headers Encontrados:")
    keep_list = [
        "ID_Print", "Data", "URL", "Tema_Descricao", "Texto_Legenda", 
        "Duracao", "Views", "Likes", "Comentarios", "Salvamentos", "Compartilhamentos",
        "Tempo_Medio_View", "Seguidores_Novos"
    ]
    
    # Mapear índices para deletar (de trás para frente para não zoar o índice)
    cols_to_delete_indices = []
    
    for i, h in enumerate(headers):
        clean_h = str(h).strip()
        print(f"[{i}] {clean_h}")
        
        # Se não estiver na lista de manter, marca para exclusão
        # Mas cuidado: Score_Pontos e Taxa_Engajamento foram criados na migração V2.
        # Usuário disse que L-N não atualiza.
        # Vamos ver o que são L, M, N.
        
        # Mapeamento A=0, K=10, L=11.
        # Se L,M,N são 11,12,13.
        
        is_essential = False
        for k in keep_list:
            if k.lower() in clean_h.lower(): 
                is_essential = True
                
        if not is_essential:
            print(f"   ❌ Vai ser deletado: {clean_h}")
            cols_to_delete_indices.append(i)
        else:
            print(f"   ✅ Mantido: {clean_h}")

    if not cols_to_delete_indices:
        print("Nada para deletar.")
        return

    # Deletar via batchUpdate (Column Range)
    # A API exige deleteDimension. Precisamos agrupar índices contíguos ou mandar um por um (de tras pra frente).
    
    ws = svc.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheet_id = next((s['properties']['sheetId'] for s in ws['sheets'] if s['properties']['title']=="BASE_DADOS"), None)
    
    cols_to_delete_indices.sort(reverse=True)
    
    reqs = []
    for idx in cols_to_delete_indices:
        reqs.append({
            "deleteDimension": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": idx,
                    "endIndex": idx + 1
                }
            }
        })
        
    svc.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={"requests": reqs}).execute()
    print(f"✅ {len(reqs)} colunas deletadas com sucesso.")

if __name__ == "__main__":
    clean_columns()
