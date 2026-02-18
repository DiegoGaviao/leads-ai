#!/usr/bin/env python3
import sys, json
from database import get_supabase_client

def main(email):
    supabase = get_supabase_client()
    print('Procurando cliente por email:', email)
    client_res = supabase.table('clients').select('*').eq('email', email).execute()
    print('Clients found:', len(client_res.data) if client_res.data else 0)
    if client_res.data:
        client = client_res.data[0]
        print(json.dumps(client, indent=2, ensure_ascii=False))
        cid = client['id']
        brief = supabase.table('briefings').select('*').eq('client_id', cid).order('created_at', desc=True).execute()
        print('\nBriefings found:', len(brief.data) if brief.data else 0)
        if brief.data:
            for b in brief.data[:5]:
                print('---')
                print(json.dumps({k:b.get(k) for k in ['id','client_id','created_at','status']}, indent=2, ensure_ascii=False))
        strat = supabase.table('strategies').select('*').eq('client_id', cid).order('created_at', desc=True).execute()
        print('\nStrategies found:', len(strat.data) if strat.data else 0)
        if strat.data:
            for s in strat.data[:5]:
                print('---')
                print(json.dumps({k:s.get(k) for k in ['id','client_id','created_at','status','model_used']}, indent=2, ensure_ascii=False))
    else:
        print('Cliente não encontrado.')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: check_client.py email')
        sys.exit(1)
    main(sys.argv[1])
