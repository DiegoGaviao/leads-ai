import os
import json
from supabase import create_client

SUPABASE_URL = "https://iatbzoowdgzytolcrvbe.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlhdGJ6b293ZGd6eXRvbGNydmJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzNDM2NDksImV4cCI6MjA4NTkxOTY0OX0.uXOUZbXWQHrcYQe90Cj-XY08aqT7WDoCRJaGhaiYEn8"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def check():
    print("--- CLIENTS ---")
    c = supabase.table('clients').select('*').execute()
    print(json.dumps(c.data, indent=2))
    
    print("\n--- BRIEFINGS ---")
    b = supabase.table('briefings').select('*').execute()
    print(json.dumps(b.data, indent=2))
    
    print("\n--- STRATEGIES ---")
    s = supabase.table('strategies').select('*').execute()
    print(json.dumps(s.data, indent=2))

if __name__ == "__main__":
    check()
