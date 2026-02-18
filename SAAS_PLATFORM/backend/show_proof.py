
import os
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def get_latest():
    res = supabase.table('strategies').select('*').order('created_at', desc=True).limit(1).execute()
    if res.data:
        strat = res.data[0]
        content = strat.get('content_json', {})
        print(f"DEBUG: content type is {type(content)}")
        
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except:
                print("DEBUG: Failed to parse content string as JSON")
        
        print("\n--- 🤖 ESTRATÉGIA GERADA COM SUCESSO ---")
        print(f"ID Cliente: {strat['client_id']}")
        
        if isinstance(content, dict):
            persona = content.get('persona', {})
            if isinstance(persona, str):
                 try:
                     persona = json.loads(persona)
                 except:
                     pass
            
            if isinstance(persona, dict):
                print(f"👤 PERSONA: {persona.get('name', 'N/A')}")
            else:
                print(f"👤 PERSONA (Raw): {str(persona)[:100]}...")
            
            print(f"🎯 PILARES: {len(content.get('pillars', []))} pilares.")
            print(f"🎬 ROTEIROS: {len(content.get('scripts', []))} roteiros.")
        else:
            print(f"CONTEÚDO (Raw): {str(content)[:200]}...")
            
    else:
        print("Nenhuma estratégia encontrada.")

if __name__ == "__main__":
    get_latest()
