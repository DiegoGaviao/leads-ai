
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
        
        if isinstance(content, str):
            content = json.loads(content)
        
        print("\n✅ SISTEMA FUNCIONANDO! ESTRATÉGIA LOCALIZADA NO BANCO DE DADOS:")
        print(f"ID Cliente: {strat['client_id']}")
        print(f"Data Geração: {strat['created_at']}")
        
        persona = content.get('persona', '')
        print(f"\n👤 [PERSONA GERADA]:\n{str(persona)[:300]}...")
        
        estrategia = content.get('estrategia', '')
        print(f"\n🎯 [ESTRATÉGIA]:\n{str(estrategia)[:300]}...")
        
        roteiros = content.get('roteiros', [])
        print(f"\n🎬 [ROTEIROS]: Foram gerados {len(roteiros)} roteiros de Reels.")
        if roteiros:
            print(f"Exemplo Roteiro 1: {roteiros[0].get('tema', 'Sem tema')}")
    else:
        print("Nenhuma estratégia encontrada.")

if __name__ == "__main__":
    get_latest()
